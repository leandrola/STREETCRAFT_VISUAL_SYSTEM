"""Geometry/rendering checks on blank pixels, no OCR and no D3 image rendering."""
import json
from PIL import Image, ImageChops
import run_injections as task


def main():
    p=json.loads((task.HERE.parent/'PROTOCOL.json').read_text())
    base=Image.new('RGB',(1600,900),(70,80,90));checks=[]
    for family,f in zip(('sans','serif'),p['planned_injection']['font_files_and_hashes']):
        for height in (8,12,20,40,80):
            for variant in ('sharp','blur'):
                im,truth=task.render(base,'NOVA DEPOT',height,task.Path(f['path']),variant,[0,0,453,900])
                name=f'{family}_{height}_{variant}'
                if height==80:
                    ok=im is None and truth['status']=='SKIPPED_DOES_NOT_FIT_FROZEN_ZONE'
                else:
                    changed=ImageChops.difference(im,base).getbbox()
                    patch=truth['patch_box']
                    ok=truth['actual_unblurred_mask_ink_height']==height and changed==tuple(patch)
                    ok &= im.crop((453,61,1147,839)).tobytes()==base.crop((453,61,1147,839)).tobytes()
                checks.append({'case':name,'pass':bool(ok),'render_status':truth['status'],'geometry':truth})
                assert ok,name
    for zone,box in (('free',[0,0,453,900]),('core',[453,61,1147,839])):
        im,t=task.render(base,'TERMINAL DINER',20,task.Path(p['planned_injection']['font_files_and_hashes'][0]['path']),'sharp',box)
        o=task.ocr.overlap(t['box_normalized'],p['geometry']['spatial_D_core'])
        label=task.ocr.classify('TERMINAL DINER',1,t['box_normalized'],base.size,p['geometry']['spatial_D_core'],p['whitelist'])['classification']
        ok=(o==0 and label=='ADVERTENCIA_DUPLICADO') if zone=='free' else (o==1 and label=='IGNORADO_POR_SOLAPE')
        checks.append({'case':zone+'_control','pass':ok});assert ok,zone
    task.ocr.write_json(task.HERE/'CHECKS.json',{'scope':'BLANK_PIXEL_RENDERING_AND_METADATA_ONLY_NO_OCR','passed':len(checks),'checks':checks})
    print('PASS',len(checks),'checks; 80px known non-fitting cases remain skipped, not sensitivity PASS')


if __name__=='__main__':main()
