"""Frozen local OCR contrast. No generators, network, alignment or source writes."""
import argparse
import difflib
import hashlib
import json
import math
import platform
import re
import subprocess
import tempfile
import unicodedata
from collections import Counter
from pathlib import Path

import PIL
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def norm(text):
    return re.sub('[^A-Z0-9]', '', unicodedata.normalize('NFKD', text).upper())


def similarity(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b), autojunk=False).ratio()


def area(box):
    return max(0, box[2]-box[0])*max(0, box[3]-box[1])


def intersection(a,b):
    return area([max(a[0],b[0]),max(a[1],b[1]),min(a[2],b[2]),min(a[3],b[3])])


def overlap(box, core):
    return intersection(box,core)/area(box) if core and area(box)>0 else 0


def iou(a,b):
    inter=intersection(a,b)
    return inter/(area(a)+area(b)-inter) if area(a)+area(b)>inter else 0


def classify(text, confidence, box, size, core, whitelist):
    w,h=size
    height=(box[3]-box[1])*h*1600/w
    matched=max(whitelist, key=lambda s:similarity(text,s))
    sim=similarity(text,matched)
    o=overlap(box,core)
    if core is None:
        label='RAW_UNREVIEWED'
    elif o>.30:
        label='IGNORADO_POR_SOLAPE'
    elif sim>=.80:
        label='ADVERTENCIA_DUPLICADO'
    elif confidence>=.60 and sum(c.isalnum() for c in text)>=3 and height>=10-1e-9:
        label='VIOLACION'
    else:
        label='ADVERTENCIA'
    return {'classification':label,'core_overlap':o,'height_at_width_1600':height,
            'alphanumeric_count':sum(c.isalnum() for c in text),
            'whitelist_best':matched,'whitelist_similarity':sim}


def origins(length):
    return sorted(set(list(range(0,max(1,length-800+1),640))+[max(0,length-800)]))


def tile_plan(size, core):
    w,h=size; result=[]
    for y in origins(h):
        for x in origins(w):
            box=[x,y,min(x+800,w),min(y+800,h)]
            n=[box[0]/w,box[1]/h,box[2]/w,box[3]/h]
            if core is not None and overlap(n,core)>=1-1e-12:
                continue
            result.append(box)
    return result


def map_box(box, tile, original, canonical):
    x,y,r,b=tile; cw,ch=canonical; ow,oh=original
    n=[(x+box[0]*(r-x))/cw,(y+box[1]*(b-y))/ch,
       (x+box[2]*(r-x))/cw,(y+box[3]*(b-y))/ch]
    return n,[n[0]*ow,n[1]*oh,n[2]*ow,n[3]*oh]


def groups(detections):
    """Contiguous vertical line groups; keep raw constituents even when matched."""
    lines=sorted(detections,key=lambda d:(d['box_normalized'][1],d['box_normalized'][0]))
    added=[]
    for start in range(len(lines)):
        group=[lines[start]]
        for pos in range(start+1,min(start+3,len(lines))):
            prev=group[-1]['box_normalized']; cur=lines[pos]['box_normalized']
            hor=max(0,min(prev[2],cur[2])-max(prev[0],cur[0]))
            width=min(prev[2]-prev[0],cur[2]-cur[0])
            gap=cur[1]-prev[3]
            if width<=0 or hor/width<.5 or gap<0 or gap>1.5*max(prev[3]-prev[1],cur[3]-cur[1]):
                break
            group.append(lines[pos])
            boxes=[g['box_normalized'] for g in group]
            added.append({'text':' '.join(g['text'] for g in group),
                          'confidence':min(g['confidence'] for g in group),
                          'box_normalized':[min(b[0] for b in boxes),min(b[1] for b in boxes),
                                            max(b[2] for b in boxes),max(b[3] for b in boxes)],
                          'constituents':[g['id'] for g in group], 'kind':'LINE_GROUP'})
    return added


def deduplicate(findings):
    reps=[]
    for finding in sorted(findings,key=lambda d:(-d['confidence'],d['id'])):
        same=next((r for r in reps if norm(r['text'])==norm(finding['text'])
                   and r['classification']==finding['classification']
                   and iou(r['box_normalized'],finding['box_normalized'])>=.50),None)
        if same is None:
            finding['deduplicated_into']=None
            reps.append(finding)
        else:
            finding['deduplicated_into']=same['id']
    return reps


def verify_freeze(binary):
    path=HERE/'FREEZE.json'; rel=path.relative_to(ROOT).as_posix()
    commit=subprocess.check_output(['git','log','-1','--format=%H','--',rel],cwd=ROOT).decode().strip()
    if not commit or subprocess.check_output(['git','show',f'{commit}:{rel}'],cwd=ROOT)!=path.read_bytes():
        raise ValueError('FREEZE_NOT_COMMITTED_OR_CHANGED')
    frozen=json.loads(path.read_text())
    for name,digest in frozen['files_sha256'].items():
        if sha(HERE/name)!=digest: raise ValueError('FROZEN_FILE_CHANGED:'+name)
    if sha(binary)!=frozen['binary_sha256']: raise ValueError('OCR_BINARY_CHANGED')
    build=subprocess.check_output(['/usr/bin/sw_vers','-buildVersion']).decode().strip()
    if PIL.__version__!='12.3.0' or build!='24G830': raise ValueError('ENVIRONMENT_CHANGED')
    return commit,sha(path)


def run_case(case, entry, core, binary, run, whitelist):
    folder=run/case; folder.mkdir()
    source=Path(entry['path'])
    if sha(source)!=entry['sha256']: raise ValueError('INPUT_HASH_CHANGED:'+case)
    with Image.open(source) as image:
        if image.getexif().get(274,1)!=1: raise ValueError('EXIF_ORIENTATION_NOT_IDENTITY')
        original_mode=image.mode
        if 'A' in image.getbands():
            rgba=image.convert('RGBA'); original=Image.new('RGBA',image.size,'white')
            original=Image.alpha_composite(original,rgba).convert('RGB')
        else:
            original=image.convert('RGB')
    canonical=original.resize((1600,round(original.height*1600/original.width)),Image.Resampling.LANCZOS)
    tiles=tile_plan(canonical.size,core)
    record={'case':case,'input':entry,'original_mode':original_mode,
            'normalization':{'size':canonical.size,'scale_x':1600/original.width,
                             'scale_y':canonical.height/original.height,'interpolation':'LANCZOS',
                             'rgb_sha256':hashlib.sha256(canonical.tobytes()).hexdigest()},
            'core_box_normalized':core,'raw_only':core is None,'tiles':[],
            'annotation':'KNOWN_POSITIVE_OPERATOR' if case=='v1_D_2' else 'PENDING_USER',
            'status':'STARTED','findings':[]}
    write_json(folder/'result.json',record)
    with tempfile.TemporaryDirectory(prefix='contrast02-tiles-') as tmp:
        temp=Path(tmp); jobs=[]; tile_by_id={}
        for index,box in enumerate(tiles):
            tid=f'tile_{index:03d}'; path=temp/(tid+'.png')
            tile=canonical.crop(box); tile=tile.resize((tile.width*2,tile.height*2),Image.Resampling.LANCZOS); tile.save(path)
            jobs.append({'id':tid,'path':str(path)})
            record['tiles'].append({'id':tid,'canonical_box':box,'size_upscaled':tile.size,'sha256':sha(path)})
            tile_by_id[tid]=box
        write_json(temp/'jobs.json',jobs)
        if jobs:
            completed=subprocess.run([str(binary),str(temp/'jobs.json')],capture_output=True,timeout=300)
            (folder/'vision_stdout.json').write_bytes(completed.stdout)
            if completed.stderr: (folder/'vision_stderr.txt').write_bytes(completed.stderr)
            if completed.returncode: raise RuntimeError('VISION_PROCESS_FAILED:'+str(completed.returncode))
            raw=json.loads(completed.stdout)
            if sorted(r['id'] for r in raw)!=sorted(tile_by_id): raise ValueError('INCOMPLETE_TILE_RESULTS')
        else:
            raw=[]; write_json(folder/'vision_stdout.json',raw)
        errors=[r for r in raw if r.get('error')]
        for tile_result in raw:
            tid=tile_result['id']; local=[]
            for index,d in enumerate(tile_result['detections']):
                n,px=map_box(d['box'],tile_by_id[tid],original.size,canonical.size)
                local.append({'id':f'{tid}_line_{index:03d}','tile':tid,'text':d['text'],
                              'confidence':d['confidence'],'box_normalized':n,'box_original_px':px,'kind':'OCR_LINE'})
            combined=groups(local)
            for index,g in enumerate(combined):
                g.update(id=f'{tid}_group_{index:03d}',tile=tid)
                b=g['box_normalized']; g['box_original_px']=[b[0]*original.width,b[1]*original.height,b[2]*original.width,b[3]*original.height]
            for d in local+combined:
                d.update(classify(d['text'],d['confidence'],d['box_normalized'],original.size,core,whitelist))
                d['review']='UNREVIEWED'
                record['findings'].append(d)
        record['tile_errors']=errors
    cropdir=folder/'crops'; cropdir.mkdir()
    for d in record['findings']:
        b=d['box_original_px']; margin=8*original.width/1600
        cropbox=[max(0,math.floor(b[0]-margin)),max(0,math.floor(b[1]-margin)),
                 min(original.width,math.ceil(b[2]+margin)),min(original.height,math.ceil(b[3]+margin))]
        path=cropdir/(d['id']+'.png'); original.crop(cropbox).save(path)
        d['crop']=str(path.relative_to(run));d['crop_sha256']=sha(path)
    reps=deduplicate(record['findings'])
    record['unique_counts']=dict(Counter(d['classification'] for d in reps))
    record['raw_finding_count']=len(record['findings'])
    record['status']='OCR_PARTIAL_ERROR' if record['tile_errors'] else ('NO_FREE_ZONE' if not tiles else 'OCR_COMPLETE')
    record['core_violations']=[d['id'] for d in reps if d['core_overlap']>.30 and d['classification']=='VIOLACION']
    if case=='v1_D_2':
        record['known_positive_results']=[]
        for phrase in ('JOHNSON WAREHOUSE','STORAGE MOVING'):
            hits=[d['id'] for d in reps if d['classification']=='VIOLACION' and similarity(d['text'],phrase)>=.80]
            recognized=[d['id'] for d in reps if similarity(d['text'],phrase)>=.80]
            record['known_positive_results'].append({'text':phrase,'expected':'VIOLACION','detected':bool(hits),
                                                      'violation_ids':hits,'recognized_ids':recognized})
    record['input_sha256_after']=sha(source)
    assert record['input_sha256_after']==entry['sha256']
    write_json(folder/'result.json',record)
    return record


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binary',type=Path,required=True)
    parser.add_argument('--run-id',required=True)
    args=parser.parse_args()
    if not re.fullmatch('[A-Za-z0-9_-]+',args.run_id): parser.error('Invalid run ID')
    binary=args.binary.resolve(); commit,digest=verify_freeze(binary)
    run=HERE/'runs'/args.run_id;run.mkdir(parents=True,exist_ok=False)
    protocol=json.loads((HERE/'PROTOCOL.json').read_text())
    inputs=json.loads((HERE/'PREPARATION.json').read_text())['inputs']
    cores={'v1_D_2':[.20,0,.89,.94],'v1_D_1':None,'source_D':[0,0,1,1],'legacy_191_D':None}
    summary={'freeze_commit':commit,'freeze_sha256':digest,'binary_sha256':sha(binary),
             'python':platform.python_version(),'pillow':PIL.__version__,'os':platform.platform(),
             'scope':'LOCAL_OCR_CONTRAST_ONLY','ai_generations':0,'cases':{},
             'missing_inputs':['spatial_D_001','spatial_D_002','spatial_D_003_good'],
             'synthetic_injection':'NOT_RUN_MISSING_GOOD_BASE','overall_acceptance':'NOT_ESTABLISHED',
             'false_positive_review':'PENDING_VISUAL_REVIEW'}
    write_json(run/'SUMMARY.json',summary)
    for case in ('v1_D_2','v1_D_1','source_D','legacy_191_D'):
        try:
            result=run_case(case,inputs[case],cores[case],binary,run,protocol['whitelist'])
            summary['cases'][case]={'status':result['status'],'unique_counts':result['unique_counts'],
                                    'core_violations':result['core_violations'],
                                    'known_positive_results':result.get('known_positive_results')}
            if result['tile_errors']: raise RuntimeError('OCR_TILE_ERROR')
        except Exception as exc:
            summary['execution_error']={'case':case,'error':repr(exc)}
            write_json(run/'SUMMARY.json',summary)
            raise
        write_json(run/'SUMMARY.json',summary)
        print(case,result['status'],result['unique_counts'],flush=True)
    outputs={str(p.relative_to(run)):sha(p) for p in sorted(run.rglob('*')) if p.is_file()}
    write_json(run/'OUTPUT_HASHES.json',outputs)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
