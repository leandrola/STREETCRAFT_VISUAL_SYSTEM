#!/usr/bin/env python3
"""Read-only inventory; writes only sibling report annexes. No Git mutation."""
from __future__ import annotations
import ast
import collections
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'development/cleanup'
ENV_DIRS = {'.venv', '.venv-sc', 'venv', '.tox', '.nox'}
CACHE_DIRS = {'__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.cache'}
IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.tiff', '.tif', '.bmp', '.ico', '.heic'}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write_json(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')

def write_csv(name, rows, fields=None):
    rows = list(rows)
    with (OUT/name).open('w', newline='') as f:
        writer = csv.DictWriter(f, fields or list(rows[0]) if rows else fields or ['path'])
        writer.writeheader()
        writer.writerows(rows)

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode()

def main():
    tracked = set(git('ls-files', '-z').strip('\0').split('\0'))
    ignored = set(git('ls-files', '--others', '--ignored', '--exclude-standard', '-z').strip('\0').split('\0'))
    head = git('rev-parse', 'HEAD').strip()
    rows, texts, jsons, errors = {}, {}, {}, []
    git_stats = {'files': 0, 'bytes': 0}
    for directory, dirs, files in os.walk(ROOT, followlinks=False):
        rel_dir = Path(directory).relative_to(ROOT).as_posix()
        if rel_dir == 'development':
            dirs[:] = [d for d in dirs if d != 'cleanup']
        for name in files:
            p = Path(directory)/name
            rel = p.relative_to(ROOT).as_posix()
            try:
                stat = p.lstat()
                if rel.startswith('.git/'):
                    git_stats['files'] += 1
                    git_stats['bytes'] += stat.st_size
                    continue
                parts = Path(rel).parts
                browser = parts[0] == '.browser-profile'
                is_env = parts[0] in ENV_DIRS
                is_cache = any(x in CACHE_DIRS for x in parts) or p.suffix == '.pyc'
                link = p.is_symlink()
                # Browser profile is measured without reading potentially private session contents.
                data = b'' if browser else (os.readlink(p).encode() if link else p.read_bytes())
                text = None
                if not browser and not link and b'\0' not in data:
                    try:
                        text = data.decode('utf-8-sig')
                    except UnicodeError:
                        pass
                image = p.suffix.lower() in IMAGE_EXT or data[:8] == b'\x89PNG\r\n\x1a\n' or data[:3] == b'\xff\xd8\xff'
                kind = 'symlink' if link else 'image' if image else 'private_unread' if browser else 'text' if text is not None else 'binary'
                rows[rel] = dict(path=rel, bytes=stat.st_size, kind=kind,
                    text_lines=(len(text.splitlines()) if text is not None else ''),
                    markdown_lines=(len(text.splitlines()) if text is not None and p.suffix.lower()=='.md' else 0),
                    json_lines=(len(text.splitlines()) if text is not None and p.suffix.lower() in {'.json','.jsonl'} else 0),
                    sha256=('NOT_READ_PRIVATE_PROFILE' if browser else sha(data)),
                    git_state='tracked' if rel in tracked else 'ignored' if rel in ignored else 'untracked',
                    local_environment=is_env, cache=is_cache, symlink_target=os.readlink(p) if link else '')
                if text is not None and not is_env and not is_cache:
                    texts[rel] = text
                    if p.suffix == '.json':
                        try:
                            jsons[rel] = json.loads(text)
                        except ValueError as exc:
                            errors.append({'path':rel,'operation':'parse_json','error':str(exc)})
            except OSError as exc:
                errors.append({'path':rel,'operation':'read','error':str(exc)})
    project = set(texts) | {p for p,r in rows.items() if not r['local_environment'] and not p.startswith('.browser-profile/') and not r['cache']}
    dirs = {str(Path(p).parent) for p in project}
    for p in list(dirs):
        dirs.update(str(x) for x in Path(p).parents if str(x)!='.')
    basenames = collections.defaultdict(list)
    for p in project:
        basenames[Path(p).name].append(p)
    edges, unresolved, protected_references = set(), [], []

    def resolve(source, token):
        token = token.split('#')[0].removeprefix('file://').strip('`<> ')
        if not token or '://' in token:
            return [], 'nonlocal'
        if token.startswith(str(ROOT)+'/'):
            token = token[len(str(ROOT))+1:]
        elif token.startswith('/'):
            return [], 'external'
        token = token.rstrip('/')
        options = [os.path.normpath(token), os.path.normpath(str(Path(source).parent/token))]
        for option in options:
            if option in project:
                return [option], 'file'
            if option in dirs:
                return sorted(p for p in project if p.startswith(option+'/')), 'directory'
        if '/' not in token and len(basenames.get(token, [])) == 1:
            return basenames[token], 'unique_basename_inference'
        return [], 'missing_or_dynamic'

    # String candidates include full relative paths, Markdown targets, backticks,
    # JSON leaf/key values, and quoted Python path components. Exact existing-path
    # matching supplements the parser (including names with spaces).
    path_rx = re.compile(r'(?:/Users/[^\s`"<>]+|(?:\.?\.?/)?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.@+ -]+)+\.[A-Za-z0-9]+|[A-Za-z0-9_.-]+\.(?:md|json|jsonl|py|toml|png|jpg|jpeg|csv|diff|patch|txt|sh))')
    manifest_sources = set()
    for source, obj in jsons.items():
        content = texts[source]
        if any(x in Path(source).name.lower() for x in ('manifest','sha256','provenance')) or re.search(r'"[^"\n]*(?:sha256|sha1|git_blob_sha|provenance)[^"\n]*"\s*:', content, re.I):
            manifest_sources.add(source)
    manifest_sources.add('development/coordination/CHECKPOINT.json')
    for source, content in texts.items():
        if Path(source).suffix == '.md' and any(x in Path(source).name.lower() for x in ('manifest','provenance')):
            manifest_sources.add(source)
        candidates = set(path_rx.findall(content))
        candidates.update(re.findall(r'`([^`\n]+)`',content))
        candidates.update(re.findall(r'\]\(([^)\n]+)\)',content))
        for token in sorted(candidates):
            targets, how = resolve(source, token)
            for target in targets:
                edges.add((source, target, 'text_reference', how))
        if source in manifest_sources:
            def walk(obj, pointer='$'):
                if isinstance(obj, dict):
                    for k,v in obj.items():
                        yield pointer+'/'+str(k)+' [key]', str(k)
                        yield from walk(v,pointer+'/'+str(k))
                elif isinstance(obj,list):
                    for i,v in enumerate(obj):
                        yield from walk(v,pointer+'/'+str(i))
                elif isinstance(obj,str):
                    yield pointer,obj
            leaves = list(walk(jsons[source])) if source in jsons else [('text',content)]
            for pointer, value in leaves:
                tokens = set(path_rx.findall(value))
                if value.startswith('/') and '\n' not in value and len(value)<1000:
                    tokens.add(value)
                if re.fullmatch(r'[^\n]+\.(?:md|json|jsonl|py|toml|png|jpg|jpeg|csv|diff|patch|txt|sh)',value) or value.rstrip('/') in dirs:
                    tokens.add(value)
                for token in sorted(tokens):
                    targets, how = resolve(source,token)
                    record = {'source':source,'pointer':pointer,'reference':token,'resolution':how,'targets':targets}
                    protected_references.append(record)
                    for target in targets:
                        edges.add((source,target,'protected_reference',how))
                    if not targets:
                        unresolved.append(record)

    modules = collections.defaultdict(list)
    for p in project:
        if p.endswith('.py'):
            modules[Path(p).stem].append(p)
    for source, content in texts.items():
        if not source.endswith('.py'):
            continue
        try:
            tree = ast.parse(content)
        except SyntaxError as exc:
            errors.append({'path':source,'operation':'ast_parse','error':str(exc)})
            continue
        for node in ast.walk(tree):
            names = []
            if isinstance(node,ast.Import):
                names = [n.name for n in node.names]
            elif isinstance(node,ast.ImportFrom):
                if node.module:
                    names = [node.module]
            for name in names:
                full = name.replace('.','/')+'.py'
                targets = [full] if full in project else modules.get(name.split('.')[-1],[])
                for target in targets:
                    edges.add((source,target,'python_import',f'AST line {node.lineno}'))
            if isinstance(node,ast.Constant) and isinstance(node.value,str):
                targets, how = resolve(source,node.value)
                for target in targets:
                    # Literal references are conservative; only direct runtime reads
                    # below are used in executable closure.
                    edges.add((source,target,'python_directory_literal' if how=='directory' else 'python_literal',how))
    for source,target in [('command_invocation/resolve_commands.py','command_invocation/COMMANDS.json'),('command_invocation/backdrop_presets.py','command_invocation/BACKDROP_PRESETS.json')]:
        edges.add((source,target,'runtime_read','Path(__file__).with_name(...).read_text()'))

    def closure(seeds, kinds=None):
        seen=set(seeds); pending=list(seeds)
        graph=collections.defaultdict(set)
        for a,b,k,h in edges:
            if kinds is None or k in kinds:
                graph[a].add(b)
        while pending:
            for target in graph[pending.pop()]-seen:
                seen.add(target); pending.append(target)
        return seen & project

    runtime_seeds={'integration/run_streetcraft_orchestration.py','integration/streetcraft_orchestrator.py','command_invocation/resolve_commands.py','reference_runtime/reference_reasoning.py','reference_runtime/run_reference_archive.py'}
    executable=closure(runtime_seeds,{'python_import','runtime_read'})
    entry_seeds=runtime_seeds|{'README.md','STREETCRAFT.md','AGENTS.md','PACKAGE_MANIFEST.json','agent/AGENT_PROTOCOL.md'}
    all_reachable=closure(entry_seeds)
    tests={p for p in project if p.startswith(('tests/','command_invocation/test_','hardening/test_','reference_runtime/test_','scene_intelligence/test_','integration/test_'))}
    tests|={'validation/test_patch_1_9_1.py','validation/test_single_client_1_10_0.py','benchmark/check_r2_baseline.py','validation/camera_routing/validate_matrix.py','validation/camera_routing/validate_l3.py'}
    test_dependencies=closure(tests,{'python_import','python_literal'})
    fixture_manifests={'benchmark/baselines/R2_VISUAL_BASELINE_1_8_1.json','benchmark/fixtures/GOLDEN_FIXTURES.json','benchmark/fixtures/REMOTE_BINARY_FIXTURES.json','RECONSTRUCTION_PROVENANCE.json'}
    # Existing baseline/integrity loops read the path fields dynamically.
    # These data edges are explicit input dependencies, unlike sys.path directories.
    for rec in protected_references:
        if rec['source'] in fixture_manifests and (rec['source']!='RECONSTRUCTION_PROVENANCE.json' or '/exact_embedded_assets/' in rec['pointer']):
            test_dependencies.update(rec['targets'])
            for target in rec['targets']:
                edges.add((rec['source'],target,'test_fixture_manifest','Existing integrity runner iterates fixture path fields'))
    protected_by=collections.defaultdict(set)
    for rec in protected_references:
        for target in rec['targets']:
            protected_by[target].add(rec['source'])
    # A provenance manifest's own bytes and containing evidence files are not disposable.
    for source in manifest_sources:
        protected_by[source].add('MANIFEST_SELF_PRESERVATION')

    bindings=[]
    def find_bindings(source,obj,pointer='$'):
        if isinstance(obj,dict):
            path_value=next((obj[k] for k in ('path','file','relative_path','evidence_path') if isinstance(obj.get(k),str)),None)
            digest=next((obj[k] for k in ('sha256','file_sha256','evidence_sha256','git_blob_sha') if isinstance(obj.get(k),str)),None)
            pairs=[]
            if path_value and digest:
                pairs.append((path_value,digest,'git_blob_sha' if 'git_blob_sha' in obj else 'sha256'))
            for key,value in obj.items():
                if isinstance(value,str) and re.fullmatch('[0-9a-fA-F]{64}',value) and (('/' in key) or re.search(r'\.[A-Za-z0-9]+$',key)):
                    pairs.append((key,value,'sha256'))
                find_bindings(source,value,pointer+'/'+str(key))
            for token,digest,algorithm in pairs:
                targets,how=resolve(source,token)
                for target in targets or ['']:
                    actual=rows[target]['sha256'] if target else ''
                    if target and algorithm=='git_blob_sha':
                        blob=(ROOT/target).read_bytes()
                        actual=hashlib.sha1(f'blob {len(blob)}\0'.encode()+blob).hexdigest()
                    bindings.append({'source':source,'pointer':pointer,'reference':token,'resolved_path':target,'resolution':how,'algorithm':algorithm,'recorded':digest,'current':actual,'comparison':'MATCH' if actual==digest else 'DIFF_HISTORICAL_OR_CHANGED' if actual else 'UNRESOLVED'})
        elif isinstance(obj,list):
            for i,value in enumerate(obj):
                find_bindings(source,value,pointer+'/'+str(i))
    for source in sorted(manifest_sources):
        if source in jsons:
            find_bindings(source,jsons[source])
    write_csv('hash_bindings.csv',bindings)

    runtime_dirs=('core/','transform/','agent/','intelligence/','critic/','self_correction/','hardening/','patch/','scene_intelligence/','command_invocation/','reference_runtime/','adapters/')
    governance={'AGENTS.md','README.md','STREETCRAFT.md','ROADMAP.md','.gitignore','PACKAGE_MANIFEST.json','docs/README.md','docs/repository/VERIFICATION.md'}
    runtime_docs={'CHEAT_SHEET.md','IMAGE_EXPORT_FORMATS.md','REFERENCE_REASONING_ARCHIVE_INTEGRATION.md','integration/PATCH_HOOKS_1_9_1.md','fear_city/FEAR_CITY_VISION.md','reference/CANONICAL_REFERENCE_SPEC.md','reference/VISUAL_CANON.md','reference/DOCUMENTARY_EVIDENCE.md','reference/manifest.json','reference/manifest.schema.json'}
    for p,r in rows.items():
        if r['cache'] or Path(p).name=='.DS_Store' or Path(p).name.startswith('._') or p.endswith(('.swp','.swo','~')):
            category,reason='DELETE_REGENERABLE','Caché de intérprete/herramienta o metadata local; no código fuente.'
        elif r['local_environment']:
            category,reason='DELETE_REGENERABLE','Paquete instalado/entorno virtual local; registrar versiones antes de reconstruir, no vendorizado.'
        elif p.startswith('.browser-profile/'):
            category,reason='DECISION_USER','Perfil persistente del navegador; mezcla caché y sesión, contenido privado no leído.'
        elif p in executable:
            category,reason='KEEP_RUNTIME','Alcanzable por import AST o lectura explícita desde CLI/orquestador/RR2.'
        elif p in tests:
            category,reason='KEEP_TESTS','Runner activo o dependencia literal/import de pruebas del runtime/supervisor.'
        elif p in governance or p.startswith(('.codex/','specs/SC_MULTIAGENT_','development/coordination/','scripts/')) or p in {'specs/STREETCRAFT_CODEX_MASTER_PLAN_v1.md','specs/STREETCRAFT_v12.md'}:
            category,reason='KEEP_GOVERNANCE','Entrada o contrato del multiagente/estado único; no acredita ejecución ni cierre.'
        elif p.startswith('validation/sc_multiagent/'):
            if '/visual_campaigns/' in p:
                category,reason='ARCHIVE','Campaña visual cerrada por instrucción actual; evidencia de SC02, conservar vínculos y hashes.'
            else:
                category,reason='KEEP_GOVERNANCE','Evidencia de equipo, revisión y procedencia de hitos SC01–06 aún necesaria.'
        elif p.startswith('docs/SC_'):
            category,reason='KEEP_GOVERNANCE','Quickstart vigente del equipo, campañas o continuidad; requiere futura conciliación de alcance.'
        elif p in runtime_docs or (p.startswith(runtime_dirs) and Path(p).suffix in {'.md','.json','.py'}):
            category,reason='KEEP_RUNTIME','Contrato de generación/CIL/SAR2/RR2/hardening o catálogo auxiliar de esas capas; uso documental por el host.'
        elif p.startswith('schemas/') and not Path(p).name.startswith('vsg-') and 'visual-scene-graph' not in p:
            category,reason='KEEP_RUNTIME','Esquema público del contrato visual/analítico; validación y lectura del host, no carga automática demostrada.'
        elif p in test_dependencies:
            category,reason='KEEP_TESTS','Dependencia de archivo literal o import de runner activo; no expansión de directorios sys.path.'
        elif p.startswith(('reference/assets/','benchmark/r2b_1_9_1/sources/')) or p=='reference/CANON_CANDIDATES.md' or p.startswith('outputs/'):
            category,reason='DECISION_USER','Fuente visual/candidato o salida local con posible valor y procedencia; regenerabilidad no demostrada.'
        elif p.startswith(('benchmark/fixtures/','benchmark/baselines/')) or p in {'benchmark/run_regression_suite.py','benchmark/BENCHMARK_CASES.json'}:
            category,reason='KEEP_TESTS','Infraestructura/fixture/baseline de regresión; runner unificado incluye también suites cerradas.'
        elif p.startswith(('visual_scene_graph/','validation/','docs/history/','docs/releases/','docs/provenance/','docs/milestones/','legacy/','release_decisions/')) or p in {'CHANGELOG.md','RELEASE_NOTES_1_10_0.md','SVS_1_10_0_SHA256SUMS.json','RECONSTRUCTION_PROVENANCE.json'} or (p.startswith('schemas/') and ('vsg-' in p or 'visual-scene-graph' in p)):
            category,reason='ARCHIVE','Evidencia/implementación de línea cerrada o instantánea histórica; retención sujeta a referencias entrantes y protección.'
        else:
            category,reason='DECISION_USER','Sin dependencia operativa concluyente; no se infiere prescindibilidad por nombre o fecha.'
        r.update(category=category,reason=reason,protected=bool(protected_by[p]),protection_sources=' | '.join(sorted(protected_by[p])),
                 reachable_from_entries=p in all_reachable,executable_runtime=p in executable)
    ordered=[rows[p] for p in sorted(rows)]
    write_csv('classification.csv',ordered)
    write_csv('references.csv',({'source':a,'target':b,'kind':k,'evidence':h,'source_category':rows[a]['category'],'target_category':rows[b]['category']} for a,b,k,h in sorted(edges)))
    write_json('protected_references.json',{'method':'JSON keys and leaves, Markdown targets, exact/local/unique basename resolution; unresolved retained without asserting existence','manifest_sources':sorted(manifest_sources),'references':protected_references,'unresolved':unresolved})
    write_csv('protected_paths.csv',({'path':p,'category':rows[p]['category'],'sha256':rows[p]['sha256'],'protected_by':' | '.join(sorted(v))} for p,v in sorted(protected_by.items()) if v))
    write_json('reachability.json',{'entry_seeds':sorted(entry_seeds),'executable_runtime':sorted(executable),'all_reference_reachable':sorted(all_reachable),'test_seeds':sorted(tests),'test_dependencies':sorted(test_dependencies),
        'dynamic_inputs':['CLI --archive-root (external runtime/retrieval/query_planner.py; runtime/integration/evidence_bundle.py; runtime/integration/negative_evidence.py and transitive imports)','CLI --request JSON (operator supplied)','CLI --evidence JSON (operator supplied)','CLI --output writable destination (not an input)','scripts/sc_supervisor.py: .git/sc-supervisor state; checkpoint envelope paths and executor command are dynamic'],
        'limits':'Reference reachability includes historical links and is not a runtime allowlist. Python AST resolves local imports conservatively; static strings are potential dependencies, not proof of execution. Browser profile not inspected; external targets not traversed.'})
    groups=collections.defaultdict(list)
    for r in ordered:
        parts=Path(r['path']).parts
        if len(parts)==1:
            groups[('0','. (root files)')].append(r)
        else:
            groups[('1',parts[0])].append(r)
            if len(parts)>2:
                groups[('2','/'.join(parts[:2]))].append(r)
    aggregates=[]
    for (depth,path), members in sorted(groups.items()):
        aggregates.append({'depth':depth,'path':path,'files':len(members),'bytes':sum(x['bytes'] for x in members),
            'text_lines':sum(x['text_lines'] or 0 for x in members),'markdown_lines':sum(x['markdown_lines'] for x in members),'json_lines':sum(x['json_lines'] for x in members),
            'binary_files':sum(x['kind'] in {'binary','image'} for x in members),'binary_bytes':sum(x['bytes'] for x in members if x['kind'] in {'binary','image'}),
            'unread_private_files':sum(x['kind']=='private_unread' for x in members)})
    write_csv('directory_metrics.csv',aggregates)
    write_csv('largest_50.csv',sorted(ordered,key=lambda x:(-x['bytes'],x['path']))[:50])
    write_csv('binary_files.csv',[r for r in ordered if r['kind'] in {'binary','image','private_unread'}])
    write_csv('local_generated.csv',[r for r in ordered if r['local_environment'] or r['cache'] or r['path'].startswith(('outputs/','.browser-profile/')) or Path(r['path']).name=='.DS_Store'])
    dup=collections.defaultdict(list)
    for p,r in rows.items():
        if r['sha256']!='NOT_READ_PRIVATE_PROFILE' and r['kind']!='symlink':
            dup[r['sha256']].append(p)
    write_json('exact_duplicates.json',[{'sha256':h,'bytes_each':rows[ps[0]]['bytes'],'paths':ps,'potential_duplicate_bytes':(len(ps)-1)*rows[ps[0]]['bytes'],'protected_paths':[p for p in ps if rows[p]['protected']], 'deletion_authorized':False} for h,ps in dup.items() if len(ps)>1])
    archive_groups=collections.defaultdict(list)
    for p,r in rows.items():
        if r['category']=='ARCHIVE':
            parent=str(Path(p).parent)
            archive_groups[parent].append(p)
    risks=[]
    for folder, members in sorted(archive_groups.items()):
        incoming=[{'source':a,'target':b,'kind':k,'evidence':h} for a,b,k,h in sorted(edges) if b in members and rows[a]['category'].startswith('KEEP_') and a not in members]
        risks.append({'folder':folder,'scope':'Only ARCHIVE members listed; never blanket-delete parent folder','archive_files':members,'files':len(members),'bytes':sum(rows[p]['bytes'] for p in members),'protected_files':sum(rows[p]['protected'] for p in members),'keep_incoming':incoming,'risk':'Breaks imports/readers/tests if incoming executable; documentary links/manifests lose resolution. Frozen provenance prevents removal even without KEEP incoming. No incoming found is not proof of no dynamic use.'})
    write_json('archive_risks.json',risks)
    write_json('initial_snapshot.json',{'head':head,'branch':git('branch','--show-current').strip(),'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':git('status','--porcelain=v1'),'checkpoint_sha256':rows['development/coordination/CHECKPOINT.json']['sha256'],'files':{p:r['sha256'] for p,r in rows.items() if r['sha256']!='NOT_READ_PRIVATE_PROFILE'},'tracked_paths':sorted(tracked),'git_metadata':git_stats,'errors':errors})
    categories={c:{'files':sum(r['category']==c for r in ordered),'bytes':sum(r['bytes'] for r in ordered if r['category']==c),'protected':sum(r['protected'] for r in ordered if r['category']==c)} for c in sorted({r['category'] for r in ordered})}
    summary={'head':head,'files':len(rows),'bytes':sum(r['bytes'] for r in ordered),'tracked':sum(r['git_state']=='tracked' for r in ordered),'ignored':sum(r['git_state']=='ignored' for r in ordered),'untracked':sum(r['git_state']=='untracked' for r in ordered),'categories':categories,'executable_files':len(executable),'reference_reachable_files':len(all_reachable),'protected_files':sum(r['protected'] for r in ordered),'manifest_sources':len(manifest_sources),'protected_references':len(protected_references),'unresolved_references':len(unresolved),'text_lines':sum(r['text_lines'] or 0 for r in ordered),'images':sum(r['kind']=='image' for r in ordered),'image_bytes':sum(r['bytes'] for r in ordered if r['kind']=='image'),'binary_files':sum(r['kind'] in {'binary','image'} for r in ordered),'binary_bytes':sum(r['bytes'] for r in ordered if r['kind'] in {'binary','image'}),'git_metadata':git_stats,'errors':errors}
    write_json('inventory_summary.json',summary)
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
