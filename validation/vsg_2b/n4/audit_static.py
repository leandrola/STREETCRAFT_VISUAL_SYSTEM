"""N4 bounded tokenizer audit. No network, model imports, weights or forwards.

Usage: python audit_static.py --assets /tmp/vsg_n4 --repo . --output /tmp/audit.json
Assets must match INPUT_MANIFEST sources. This implements CLIPTokenizer's pinned
BasicTokenizer fallback for ASCII inputs without embedded reserved tokens only.
Non-ASCII and embedded reserved tokens fail closed; not a general tokenizer.
"""
import argparse
import ast
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from types import SimpleNamespace
from typing import List, Optional
import unicodedata


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=False, allow_nan=False)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def reference_tokenizer(assets):
    sources = json.loads((assets / 'sources.json').read_text())
    for item in sources:
        assert sha(Path(item['local_path']).read_bytes()) == item['sha256']
    code = assets / 'transformers/src/transformers/models/clip/tokenization_clip.py'
    helpers = assets / 'transformers/src/transformers/tokenization_utils.py'
    tree = ast.parse(code.read_text())
    helper_tree = ast.parse(helpers.read_text())
    names = {'bytes_to_unicode', 'get_pairs', 'whitespace_clean',
             'whitespace_tokenize', 'BasicTokenizer'}
    nodes = [n for n in tree.body if getattr(n, 'name', None) in names]
    nodes += [n for n in helper_tree.body if getattr(n, 'name', None) in
              {'_is_whitespace', '_is_control', '_is_punctuation'}]
    clip = next(n for n in tree.body if getattr(n, 'name', None) == 'CLIPTokenizer')
    methods = {'bpe', '_tokenize', 'build_inputs_with_special_tokens'}
    nodes += [n for n in clip.body if getattr(n, 'name', None) in methods]
    env = dict(re=re, unicodedata=unicodedata, lru_cache=lru_cache,
               List=List, Optional=Optional)
    # Execute only reviewed tokenizer functions/classes, never package imports.
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(code), 'exec'), env)
    pattern = next(n.value for n in ast.walk(clip) if isinstance(n, ast.Constant)
                   and isinstance(n.value, str) and '[\\p{L}]' in n.value)
    # Exact character classes on the explicitly checked ASCII input domain.
    pattern = pattern.replace('\\p{L}', 'A-Za-z').replace('\\p{N}', '0-9')
    vocab = json.loads((assets / 'tokenizer/vocab.json').read_text())
    merges = (assets / 'tokenizer/merges.txt').read_text().strip().split('\n')[1:49152-256-2+1]
    ranks = {tuple(row.split()): i for i, row in enumerate(merges)}
    obj = SimpleNamespace(encoder=vocab, byte_encoder=env['bytes_to_unicode'](),
                          bpe_ranks=ranks, cache={}, fix_text=None,
                          nlp=env['BasicTokenizer'](strip_accents=False, do_split_on_punc=False),
                          pat=re.compile(pattern, re.IGNORECASE),
                          bos_token_id=vocab['<|startoftext|>'],
                          eos_token_id=vocab['<|endoftext|>'])
    obj.bpe = lambda token: env['bpe'](obj, token)

    def tokenize(text):
        if not text.isascii() or any(ord(c) < 32 and c not in '\t\r\n' for c in text) or '\x7f' in text:
            raise ValueError('OUTSIDE_VERIFIED_ASCII_DOMAIN')
        if '<|startoftext|>' in text.lower() or '<|endoftext|>' in text.lower():
            raise ValueError('EMBEDDED_RESERVED_TOKEN_NOT_SUPPORTED')
        pieces = env['_tokenize'](obj, text)
        assert all(t in vocab for t in pieces), 'UNKNOWN_TOKEN'
        return [vocab[t] for t in pieces]

    return obj, tokenize, env


def independent_ids(text, obj):
    """Independent ASCII scanner + adjacent-rank BPE for equivalence checks."""
    text = ' '.join(text.lower().split())
    pieces = []
    pos = 0
    contractions = ["'s", "'t", "'re", "'ve", "'m", "'ll", "'d"]
    while pos < len(text):
        if text[pos].isspace():
            pos += 1
            continue
        matched = next((s for s in contractions if text.startswith(s, pos)), None)
        if matched:
            token = matched
        elif text[pos].isdigit():
            token = text[pos]
        else:
            is_letter = text[pos].isalpha()
            end = pos + 1
            while end < len(text) and (text[end].isalpha() if is_letter else
                                      not (text[end].isspace() or text[end].isalnum())):
                end += 1
            token = text[pos:end]
        pos += len(token)
        word = [obj.byte_encoder[b] for b in token.encode()]
        word[-1] += '</w>'
        while len(word) > 1:
            candidates = [(obj.bpe_ranks.get(tuple(word[i:i+2]), float('inf')), i)
                          for i in range(len(word)-1)]
            rank, index = min(candidates)
            if rank == float('inf'):
                break
            pair = tuple(word[index:index+2])
            merged = []
            i = 0
            while i < len(word):
                if tuple(word[i:i+2]) == pair:
                    merged.append(word[i] + word[i+1])
                    i += 2
                else:
                    merged.append(word[i])
                    i += 1
            word = merged
        pieces.extend(obj.encoder[t] for t in word)
    return pieces


def audit(repo, assets):
    obj, tokenize, env = reference_tokenizer(assets)
    run = repo / 'validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f'
    payload = json.loads((run / 'payloads.json').read_text())
    assert sha((run / 'payloads.json').read_bytes()) == '7b995c02541b831524236cf36c9e8e834a8ddbcaea43da6a1f6669918f8a586d'
    common = payload['A']['common']
    assert common == payload['B']['common']
    a = payload['A']['relations_and_locks']
    assert [json.loads(x) for x in a.splitlines()] == payload['B']['relations_and_locks']
    rows = [('common', canonical(common), 'A/B proposed canonical textual rendering'),
            ('common.stable_cgc', canonical(common['stable_cgc']), 'diagnostic component; not separately encoded'),
            ('common.approved_source_restrictions', canonical(common['approved_source_restrictions']), 'diagnostic component; not separately encoded'),
            ('A.JSONL', a, 'exact persisted string'),
            ('A.prompt', canonical(common) + '\n' + a, 'proposed assembly; no production bridge exists'),
            ('B.prompt', canonical(common), 'proposed assembly; B array never serialized to prompt'),
            ('negative_prompt', '', 'proposed identical empty negative for both branches')]
    nodes = [r for r in common['approved_source_restrictions'] if r['id'].startswith('node:')]
    rows += [('shared_phrase.' + n['id'], n['value']['label'], 'shared source association, never edit authority') for n in nodes]
    controls = ['', 'hello world!', 'TERMINAL DINER', "it's we're I've I'd he'll", 'LEFT_OF ABOVE 0123456789',
                '\t A\nB\r C  ', '{"id":"topology:fascia_01","value":[],"x":0.945}',
                ''.join(chr(i) for i in range(32, 127))]
    control_results = []
    for value in controls:
        ids = tokenize(value)
        assert ids == independent_ids(value, obj)
        control_results.append(dict(text=value, token_ids=ids, status='PASS'))
    assert tokenize('hello world!') == [3306, 1002, 256]
    rejected = []
    for value in ['caf\u00e9', '<|startoftext|>', 'a\x00b']:
        try:
            tokenize(value)
        except ValueError:
            rejected.append(value)
        else:
            raise AssertionError('Domain guard failed')
    results = []
    for name, value, role in rows:
        ids = tokenize(value)
        assert ids == independent_ids(value, obj), name
        with_special = env['build_inputs_with_special_tokens'](obj, ids)
        chunks = [ids[i:i+75] for i in range(0, len(ids), 75)] or [[]]
        assert [token for chunk in chunks for token in chunk] == ids
        results.append(dict(name=name, role=role, text=value, utf8_bytes=len(value.encode()),
                            characters=len(value), sha256=sha(value.encode()), ascii=True,
                            content_tokens=len(ids), special_tokens=2, tokens_with_special=len(with_special),
                            tokenizer_capacity=77, encoder_capacity=77,
                            overflow=max(0, len(with_special)-77),
                            token_ids_sha256=sha(canonical(ids).encode()),
                            blocks_75=len(chunks), last_block_content_tokens=len(chunks[-1]),
                            equivalence='PASS_ASCII_DOMAIN', chunk_coverage='PASS_TOKEN_SEQUENCE_IDENTITY'))
    return dict(strings=results, controls=control_results, domain_rejections=rejected,
                unique_measured_strings=len(rows), control_strings=len(controls),
                tokenizer_invocations=2*(len(rows)+len(controls)), rejected_invocations=len(rejected),
                pretrained_model_forwards=0, encoder_forwards=0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, required=True)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.repo, args.assets)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({row['name']: row['tokens_with_special'] for row in result['strings']}))
