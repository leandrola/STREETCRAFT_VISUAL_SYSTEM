"""D3 follow-up using frozen OCR unchanged; deterministic non-AI injection."""
import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import run_ocr as ocr


def ink(text, height, fontpath):
    # Choose font by ink height, never fit/shrink to available scene width.
    for size in range(1,4*height+1):
        font=ImageFont.truetype(str(fontpath),size)
        box=font.getbbox(text)
        if box[3]-box[1]>=height:break
    mask=Image.new('L',(box[2]-box[0]+8,box[3]-box[1]+8))
    ImageDraw.Draw(mask).text((4-box[0],4-box[1]),text,font=font,fill=255)
    mask=mask.crop(mask.getbbox())
    rawsize=mask.size
    width=round(mask.width*height/mask.height)
    if mask.height!=height:mask=mask.resize((width,height),Image.Resampling.LANCZOS)
    return mask,{'font_size':size,'raw_ink_size':rawsize,'target_ink_size':mask.size,
                 'height_resampling':'LANCZOS' if rawsize[1]!=height else 'NONE'}


def render(base, text, height, fontpath, variant, zone):
    mask,rendering=ink(text,height,fontpath)
    pad=4;w,h=mask.size;pw,ph=w+2*pad,h+2*pad
    x0,y0,x1,y1=zone
    if pw>x1-x0 or ph>y1-y0:
        return None,{'status':'SKIPPED_DOES_NOT_FIT_FROZEN_ZONE','text':text,
                     'height':height,'required_patch_size':[pw,ph],'available_zone':zone,'rendering':rendering}
    x=x0+(x1-x0-pw)//2;y=y0+(y1-y0-ph)//2
    layer=Image.new('L',(pw,ph));layer.paste(mask,(pad,pad))
    if variant=='blur':layer=layer.filter(ImageFilter.GaussianBlur(.6))
    patch=Image.new('RGB',(pw,ph),'white');patch.paste((0,0,0),(0,0,pw,ph),layer)
    image=base.copy();image.paste(patch,(x,y))
    truth={'status':'RENDERED','text':text,'height':height,'variant':variant,
           'patch_box':[x,y,x+pw,y+ph],'ink_box':[x+pad,y+pad,x+pad+w,y+pad+h],
           'box_normalized':[(x+pad)/base.width,(y+pad)/base.height,(x+pad+w)/base.width,(y+pad+h)/base.height],
           'rendering':rendering,'font_path':str(fontpath),'font_sha256':ocr.sha(fontpath),
           'actual_unblurred_mask_ink_height':mask.getbbox()[3]-mask.getbbox()[1]}
    return image,truth


def score(result, truth, expected):
    findings=[d for d in result['findings'] if not d['deduplicated_into']]
    matches=[d for d in findings if ocr.iou(d['box_normalized'],truth['box_normalized'])>=.30
             and ocr.similarity(d['text'],truth['text'])>=.80]
    return {'recognized':bool(matches),'matched_ids':[d['id'] for d in matches],
            'expected_class':expected,'expected_class_detected':any(d['classification']==expected for d in matches),
            'matched_classes':dict(Counter(d['classification'] for d in matches)),
            'matched_confidences':[d['confidence'] for d in matches],
            'core_violation_count':len(result['core_violations'])}


def verify(binary):
    parent_commit,parent_hash=ocr.verify_freeze(binary)
    p=HERE/'FREEZE.json';rel=p.relative_to(ocr.ROOT).as_posix()
    commit=subprocess.check_output(['git','log','-1','--format=%H','--',rel],cwd=ocr.ROOT).decode().strip()
    assert commit and subprocess.check_output(['git','show',f'{commit}:{rel}'],cwd=ocr.ROOT)==p.read_bytes()
    f=json.loads(p.read_text())
    for name,digest in f['files_sha256'].items():assert ocr.sha(HERE/name)==digest,name
    return {'parent_freeze_commit':parent_commit,'parent_freeze_sha256':parent_hash,
            'd3_freeze_commit':commit,'d3_freeze_sha256':ocr.sha(p)}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--binary',type=Path,required=True)
    args=parser.parse_args();binary=args.binary.resolve();freezes=verify(binary)
    entry=json.loads((HERE/'INPUT.json').read_text());source=Path(entry['path'])
    assert ocr.sha(source)==entry['sha256']
    protocol=json.loads((HERE.parent/'PROTOCOL.json').read_text())
    plan=protocol['planned_injection'];fonts=plan['font_files_and_hashes']
    for f in fonts:assert ocr.sha(Path(f['path']))==f['sha256']
    run=HERE/'execution';run.mkdir(exist_ok=False)
    # Preserve exact submitted bytes as ingestion evidence; never mutate source.
    original=run/'D3_original.png';original.write_bytes(source.read_bytes())
    entry=entry|{'path':str(original.resolve())}
    summary={**freezes,'input':entry,'status':'STARTED','cases':[],'ai_generations':0,
             'thresholds_changed':False,'annotation_note':'ground truth here/INPUT.json; generic raw runner annotation field remains unchanged'}
    ocr.write_json(run/'SUMMARY.json',summary)
    try:
        baseline=ocr.run_case('D3_baseline',entry,entry['core_box_normalized'],binary,run,protocol['whitelist'])
        if baseline['tile_errors']:raise RuntimeError('BASELINE_OCR_ERROR')
        summary['baseline']={'status':baseline['status'],'counts':baseline['unique_counts'],
                             'expected_violations':0,'pass':baseline['unique_counts'].get('VIOLACION',0)==0,
                             'core_violations':baseline['core_violations']}
        ocr.write_json(run/'SUMMARY.json',summary)
        print('BASELINE',summary['baseline'],flush=True)
        # Only after baseline OCR is complete do we render experimental images.
        with Image.open(original) as im:
            rgba=im.convert('RGBA');flat=Image.alpha_composite(Image.new('RGBA',im.size,'white'),rgba).convert('RGB')
            base=flat.resize((1600,round(flat.height*1600/flat.width)),Image.Resampling.LANCZOS)
        boxes={'free':[0,0,453,base.height],'core':[453,61,1147,839]}
        jobs=[(f'{family}_{height}_{variant}',plan['text'],height,Path(f['path']),variant,'free',
               'VIOLACION' if height>=10 else 'ADVERTENCIA')
              for family,f in zip(('sans','serif'),fonts) for height in (8,12,20,40,80) for variant in ('sharp','blur')]
        jobs += [('duplicate','TERMINAL DINER',20,Path(fonts[0]['path']),'sharp','free','ADVERTENCIA_DUPLICADO'),
                 ('core_control','TERMINAL DINER',20,Path(fonts[0]['path']),'sharp','core','IGNORADO_POR_SOLAPE')]
        images=run/'synthetic';images.mkdir()
        for case,text,height,font,variant,zone,expected in jobs:
            image,truth=render(base,text,height,font,variant,boxes[zone])
            truth.update(case=case,zone=zone,expected_class=expected)
            if image is None:
                summary['cases'].append(truth);ocr.write_json(images/(case+'.json'),truth)
                ocr.write_json(run/'SUMMARY.json',summary);print(case,truth['status'],flush=True);continue
            truth['core_identical_to_base']=image.crop((453,61,1147,839)).tobytes()==base.crop((453,61,1147,839)).tobytes()
            if zone=='free':assert truth['core_identical_to_base']
            path=images/(case+'.png');image.save(path);truth['sha256']=ocr.sha(path)
            ocr.write_json(images/(case+'.json'),truth) # known truth BEFORE recognition
            record=ocr.run_case(case,{'path':str(path.resolve()),'sha256':truth['sha256']},
                                entry['core_box_normalized'],binary,run,protocol['whitelist'])
            if record['tile_errors']:raise RuntimeError('OCR_TILE_ERROR:'+case)
            evaluation=score(record,truth,expected)
            summary['cases'].append(truth|{'evaluation':evaluation})
            ocr.write_json(run/'SUMMARY.json',summary);print(case,evaluation,flush=True)
        summary['by_height']={}
        for height in (8,12,20,40,80):
            rows=[c for c in summary['cases'] if c['case'].startswith(('sans_','serif_')) and c['height']==height]
            evaluated=[c for c in rows if 'evaluation' in c]
            detected=sum(c['evaluation']['recognized'] for c in evaluated)
            summary['by_height'][str(height)]={'planned':len(rows),'rendered_evaluated':len(evaluated),
                'detected':detected,'skipped':len(rows)-len(evaluated),
                'recognition_rate_evaluated':detected/len(evaluated) if evaluated else None,
                'expected_class_detected':sum(c['evaluation']['expected_class_detected'] for c in evaluated)}
        target=[c for c in summary['cases'] if c['case'].startswith(('sans_','serif_')) and c['height']>=20]
        summary['recall_100_percent_ge20_established']=all(c.get('evaluation',{}).get('recognized',False) for c in target)
        summary['status']='EXECUTION_COMPLETE_WITH_SKIPPED_CASES' if any('evaluation' not in c for c in summary['cases']) else 'EXECUTION_COMPLETE'
        assert ocr.sha(source)==entry['sha256']
    except Exception as exc:
        summary['status']='BLOCKED_EXECUTION_ERROR';summary['error']=repr(exc)
        ocr.write_json(run/'SUMMARY.json',summary);raise
    ocr.write_json(run/'SUMMARY.json',summary)
    ocr.write_json(run/'OUTPUT_HASHES.json',{str(p.relative_to(run)):ocr.sha(p) for p in sorted(run.rglob('*')) if p.is_file()})


if __name__=='__main__':main()
