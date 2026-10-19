"""Post-run presentation of immutable D3 OCR and synthetic truth; no retuning."""
import json
import math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from run_injections import HERE,ocr


def main():
    root=HERE/'execution';summary=json.loads((root/'SUMMARY.json').read_text())
    if summary['status']=='STARTED':raise ValueError('Run not finished')
    review=HERE/'review';review.mkdir(exist_ok=False)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
    small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
    baseline=json.loads((root/'D3_baseline/result.json').read_text())
    unique=[d for d in baseline['findings'] if not d['deduplicated_into']]
    manifest={'baseline_pages':[],'injection_pages':[]}
    for page in range(math.ceil(len(unique)/16)):
        selected=unique[page*16:(page+1)*16];sheet=Image.new('RGB',(1600,960),'#dddddd');draw=ImageDraw.Draw(sheet)
        for index,d in enumerate(selected):
            x=(index%4)*400;y=(index//4)*240
            with Image.open(root/d['crop']) as im:
                crop=im.copy();crop.thumbnail((384,155),Image.Resampling.LANCZOS);sheet.paste(crop,(x+8,y+6))
            draw.text((x+8,y+165),d['id'],font=small,fill='black')
            draw.text((x+8,y+184),d['text'][:45],font=font,fill='black')
            draw.text((x+8,y+210),f"{d['classification']} {d['confidence']:.2f}",font=small,fill='black')
        name=f'baseline_{page+1:02d}.png';sheet.save(review/name)
        manifest['baseline_pages'].append({'file':name,'sha256':ocr.sha(review/name),'ids':[d['id'] for d in selected]})
    rendered=[c for c in summary['cases'] if c['status']=='RENDERED']
    for page in range(math.ceil(len(rendered)/8)):
        selected=rendered[page*8:(page+1)*8];sheet=Image.new('RGB',(1200,960),'#dddddd');draw=ImageDraw.Draw(sheet)
        for index,c in enumerate(selected):
            x=(index%2)*600;y=(index//2)*240
            with Image.open(root/'synthetic'/(c['case']+'.png')) as im:
                b=c['patch_box'];crop=im.crop((b[0]-6,b[1]-6,b[2]+6,b[3]+6))
                # Review zoom only, not OCR input; same magnification for tiny glyphs.
                crop=crop.resize((crop.width*2,crop.height*2),Image.Resampling.NEAREST)
                crop.thumbnail((580,150),Image.Resampling.LANCZOS);sheet.paste(crop,(x+10,y+8))
            draw.text((x+10,y+165),c['case']+' / review zoom only',font=font,fill='black')
            draw.text((x+10,y+190),str(c['evaluation']['matched_classes']),font=small,fill='black')
            draw.text((x+10,y+213),'recognized='+str(c['evaluation']['recognized']),font=small,fill='black')
        name=f'injections_{page+1:02d}.png';sheet.save(review/name)
        manifest['injection_pages'].append({'file':name,'sha256':ocr.sha(review/name),'cases':[c['case'] for c in selected]})
    extras=[]
    for c in rendered:
        result=json.loads((root/c['case']/'result.json').read_text())
        for d in result['findings']:
            if not d['deduplicated_into'] and d['classification']!='IGNORADO_POR_SOLAPE':
                extras.append((c['case'],d))
    manifest['noncore_detection_pages']=[]
    for page in range(math.ceil(len(extras)/16)):
        selected=extras[page*16:(page+1)*16];sheet=Image.new('RGB',(1600,960),'#dddddd');draw=ImageDraw.Draw(sheet)
        for index,(case,d) in enumerate(selected):
            x=(index%4)*400;y=(index//4)*240
            with Image.open(root/d['crop']) as im:
                crop=im.copy();crop.thumbnail((384,150),Image.Resampling.LANCZOS);sheet.paste(crop,(x+8,y+6))
            draw.text((x+8,y+160),case+' / '+d['id'],font=small,fill='black')
            draw.text((x+8,y+184),d['text'][:45],font=font,fill='black')
            draw.text((x+8,y+210),f"{d['classification']} {d['confidence']:.2f}",font=small,fill='black')
        name=f'noncore_detections_{page+1:02d}.png';sheet.save(review/name)
        manifest['noncore_detection_pages'].append({'file':name,'sha256':ocr.sha(review/name),
            'ids':[case+'/'+d['id'] for case,d in selected]})
    ocr.write_json(review/'SHEETS.json',manifest)
    lines=['# D3 — all planned injection outcomes','',
           '| Case | Ink height | Expected | Rendered | Recognized | Classes obtained | Image / truth |',
           '| --- | --- | --- | --- | --- | --- | --- |']
    for c in summary['cases']:
        ev=c.get('evaluation');case=c['case']
        image=f'[image](execution/synthetic/{case}.png)' if ev else 'No image: frozen zone too narrow'
        lines.append(f"| {case} | {c['height']} | {c['expected_class']} | {bool(ev)} | {ev['recognized'] if ev else 'NOT_EVALUATED'} | {ev['matched_classes'] if ev else c['status']} | {image} / [truth](execution/synthetic/{case}.json) |")
    lines+=['','## D3 baseline findings','',
            '| Crop | OCR text | Confidence | Normalized xyxy | Class |',
            '| --- | --- | --- | --- | --- |']
    for d in unique:
        box=', '.join(f'{v:.5f}' for v in d['box_normalized'])
        text=d['text'].replace('|','\\|')
        lines.append(f"| [{d['id']}](execution/{d['crop']}) | {text} | {d['confidence']:.3f} | {box} | {d['classification']} |")
    (HERE/'FINDINGS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':main()
