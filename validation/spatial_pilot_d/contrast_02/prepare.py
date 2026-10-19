"""Local input inventory, geometric matching and review overlays; NEVER OCR."""
import hashlib
import json
import math
from pathlib import Path

import PIL
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DESKTOP = Path('/Users/macbookpro/Desktop/untitled folder')
SOURCE = ROOT / 'benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg'
MATCH = {
    'sample': [24, 27], 'coarse_width_fraction': [.20, .90, .025],
    'coarse_xy_step_fraction': .025, 'refine_step_fraction': .005,
    'min_ncc': .80, 'min_quadrant_ncc': .50,
    'distinct_iou_below': .70, 'min_alternative_margin': .03,
    'model': 'full_source_uniform_scale_translation_no_crop_no_rotation',
}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def vector(im, box=None):
    return tuple((im.crop(box) if box else im).resize((24, 27), Image.Resampling.BILINEAR).tobytes())


def ncc(a, b):
    sa, sb, n = sum(a), sum(b), len(a)
    va = sum(x*x for x in a)-sa*sa/n
    vb = sum(x*x for x in b)-sb*sb/n
    return (sum(x*y for x,y in zip(a,b))-sa*sb/n)/math.sqrt(va*vb) if min(va,vb)>0 else -1.0


def iou(a,b):
    inter=max(0,min(a[2],b[2])-max(a[0],b[0]))*max(0,min(a[3],b[3])-max(a[1],b[1]))
    return inter/((a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter)


def match(source, target):
    ref=source.convert('L'); im=target.convert('L'); v=vector(ref)
    w,h=im.size; aspect=source.height/source.width; candidates=[]
    # Parameters fixed above before the first search; unrelated to drift gates.
    for index in range(29):
        bw=round(w*(.20+.025*index)); bh=round(bw*aspect)
        if bh>h: continue
        step=max(1,round(w*.025))
        for y in range(0,h-bh+1,step):
            for x in range(0,w-bw+1,step):
                box=(x,y,x+bw,y+bh)
                candidates.append((ncc(v,vector(im,box)),box))
    if not candidates:
        return {'status':'ZONA NO DEFINIDA','reason':'NO_FITTING_SCALE','parameters':MATCH}
    coarse=max(candidates); _,b=coarse; bw0=b[2]-b[0]
    for dw in range(-5,6):
        bw=round(bw0+dw*w*.005); bh=round(bw*aspect)
        for iy in range(-5,6):
            y=round(b[1]+iy*w*.005)
            for ix in range(-5,6):
                x=round(b[0]+ix*w*.005); box=(x,y,x+bw,y+bh)
                if x<0 or y<0 or x+bw>w or y+bh>h: continue
                candidates.append((ncc(v,vector(im,box)),box))
    score,box=max(candidates)
    other=max((s for s,b in candidates if iou(b,box)<.70),default=-1)
    patch=im.crop(box); quadrants=[]
    for x0,y0,x1,y1 in ((0,0,.5,.5),(.5,0,1,.5),(0,.5,.5,1),(.5,.5,1,1)):
        rb=tuple(round(v*(ref.width if i%2==0 else ref.height)) for i,v in enumerate((x0,y0,x1,y1)))
        pb=tuple(round(v*(patch.width if i%2==0 else patch.height)) for i,v in enumerate((x0,y0,x1,y1)))
        quadrants.append(ncc(vector(ref,rb),vector(patch,pb)))
    reasons=[]
    if score<.80: reasons.append('LOW_NCC')
    if min(quadrants)<.50: reasons.append('LOW_QUADRANT_NCC')
    if score-other<.03: reasons.append('AMBIGUOUS_MATCH')
    return {'status':'ZONA NO DEFINIDA' if reasons else 'MATCHED_GEOMETRIC_ESTIMATE',
            'parameters':MATCH,'best_candidate_box_px':box,
            'core_box_normalized':None if reasons else [box[0]/w,box[1]/h,box[2]/w,box[3]/h],
            'ncc':score,'quadrant_ncc':quadrants,'alternative_margin':score-other,'reasons':reasons,
            'visual_or_pixel_preservation_claim':False}


def overlay(im, box, path):
    base=im.convert('RGBA'); layer=Image.new('RGBA',im.size,(0,160,80,45))
    d=ImageDraw.Draw(layer)
    px=[round(v*(im.width if i%2==0 else im.height)) for i,v in enumerate(box)]
    d.rectangle((px[0],px[1],px[2]-1,px[3]-1),fill=(40,100,255,35),outline=(255,30,0,255),width=4)
    out=Image.new('RGB',(im.width,im.height+64),'white')
    out.paste(Image.alpha_composite(base,layer).convert('RGB'))
    d=ImageDraw.Draw(out)
    d.text((12,im.height+8),'CORE = BLUE / FREE ZONE = GREEN / BOUNDARY = RED',fill='black')
    d.text((12,im.height+30),f'NORMALIZED BOX {box} - PENDING USER REVIEW - NOT OCR INPUT',fill='black')
    out.save(path)


def main():
    paths={'v1_D_1':DESKTOP/'R2B-191-D_source_corrida_1.png',
           'v1_D_2':DESKTOP/'R2B-191-D_source_corrida_2.png',
           'source_D':SOURCE,
           'legacy_191_D':SOURCE.parent/'R2B-191-D_candidate_PASS.png'}
    inventory={}
    for key,p in paths.items():
        with Image.open(p) as im:
            inventory[key]={'path':str(p),'location':'WORKSPACE' if p.is_relative_to(ROOT) else 'EXTERNAL_AVAILABLE',
                            'sha256':digest(p),'size':im.size,'mode':im.mode}
    with Image.open(paths['v1_D_2']) as im:
        overlay(im,[.20,0,.89,.94],HERE/'v1_D_2_zone_review.png')
    with Image.open(SOURCE) as source, Image.open(paths['v1_D_1']) as target:
        geometry=match(source,target)
        if geometry['core_box_normalized'] is not None:
            overlay(target,geometry['core_box_normalized'],HERE/'v1_D_1_zone_review.png')
    result={'kind':'PRE_OCR_PREPARATION_ONLY','pillow':PIL.__version__,'inputs':inventory,
            'missing':['spatial_D_001','spatial_D_002','spatial_D_003_good'],
            'missing_inputs_block_available_cases':False,
            'spatial_core_normalized':[453/1600,61/900,1147/1600,839/900],
            'v1_D_2_zone':{'box':[.20,0,.89,.94],'status':'PENDING_USER_OVERLAY_APPROVAL'},
            'v1_D_1_matching':geometry,'ocr_executed':False,
            'overlays_sha256':{p.name:digest(p) for p in sorted(HERE.glob('*_zone_review.png'))}}
    (HERE/'PREPARATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
