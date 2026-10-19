"""Build contact sheets of immutable OCR crops; never alter predictions."""
import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from run_ocr import HERE, sha, write_json


def main():
    run=HERE/'runs'/'contrast02_20261019'
    out=HERE/'review_20261019';out.mkdir(exist_ok=False)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',16)
    small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
    manifest={'scope':'VISUAL_REVIEW_SHEETS_ONLY_NO_PREDICTION_EDITS','pages':[]}
    for case in ('v1_D_2','v1_D_1','legacy_191_D'):
        result=json.loads((run/case/'result.json').read_text())
        findings=[f for f in result['findings'] if not f['deduplicated_into']]
        # Groups are included; only tile duplicates collapse in the presentation.
        for page in range(math.ceil(len(findings)/16)):
            selected=findings[page*16:(page+1)*16]
            sheet=Image.new('RGB',(1600,960),'#dddddd');draw=ImageDraw.Draw(sheet)
            for i,d in enumerate(selected):
                x=(i%4)*400;y=(i//4)*240
                with Image.open(run/d['crop']) as im:
                    crop=im.copy();crop.thumbnail((384,158),Image.Resampling.LANCZOS)
                    sheet.paste(crop,(x+8,y+6))
                draw.text((x+8,y+166),d['id'],font=small,fill='black')
                draw.text((x+8,y+184),d['text'][:45],font=font,fill='black')
                draw.text((x+8,y+207),f"{d['classification']} conf={d['confidence']:.3f}",font=small,fill='black')
            path=out/f'{case}_page_{page+1:02d}.png';sheet.save(path)
            manifest['pages'].append({'file':path.name,'case':case,'sha256':sha(path),
                                     'finding_ids':[d['id'] for d in selected]})
    write_json(out/'SHEETS.json',manifest)
    print(json.dumps(manifest,indent=2))


if __name__=='__main__':
    main()
