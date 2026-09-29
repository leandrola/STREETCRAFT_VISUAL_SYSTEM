"""Inventory original sources; historical candidates never become new outputs."""
import json
from pathlib import Path
from .harness import ROOT, sha


def audit():
    specs = [('KENNYS-ROOFTOP', None, ['topology','Geometry Lock']),
             ('R2B-191-C','jpg',['Reference Isolation','authored geography']),
             ('R2B-191-D','jpg',['Semantic Text Lock']),
             ('R2B-191-E','jpg',['Occlusion Lock']),
             ('R2B-191-F','png',['CG-F camera'])]
    rows = []
    for ident, ext, phenomena in specs:
        source = ROOT/'benchmark/r2b_1_9_1/evidence_2026_09_21'/f'{ident}_source.{ext}' if ext else None
        rows.append({'fixture_id':ident, 'critical':True, 'conditional':ident=='R2B-191-F',
                     'phenomena':phenomena, 'status':'BLOCKED',
                     'source':{'path':str(source.relative_to(ROOT)), 'sha256':sha(source.read_bytes())} if source and source.exists() else None,
                     'reason':'MISSING_SOURCE_IMAGE_BINDING' if ext is None else 'MISSING_FROZEN_REQUEST_SAR2_RR2_CGC_BINDING',
                     'substitution':None, 'fresh_pairs':0})
    return {'status':'BLOCKED','reason':'MISSING_FROZEN_SOURCE_BINDINGS','fixtures':rows,
            'initial_image_budget':8,'conditional_fifth_pair':'Requires a versioned budget change after coverage review',
            'generator_capability':'Session image generation exists; corpus gate prevents its use. No local provider bridge configured.',
            'user_confirmation':'User confirmed no additional snapshots or Kenny source image on 2026-09-29.'}


if __name__ == '__main__':
    print(json.dumps(audit(),indent=2))
