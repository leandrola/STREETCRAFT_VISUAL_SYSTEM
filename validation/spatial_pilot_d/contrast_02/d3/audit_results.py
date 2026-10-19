"""Post-execution integrity checks; no OCR or changes to frozen predictions."""
import contextlib
import io
import json
import sys
from pathlib import Path
from PIL import Image
import run_injections as task


def main():
    root=task.HERE/'execution'
    freezes=task.verify(Path('/tmp/contrast02-ocr.5L2pPS/vision_ocr'))
    manifest=json.loads((root/'OUTPUT_HASHES.json').read_text())
    for name,digest in manifest.items():assert task.ocr.sha(root/name)==digest,name
    entry=json.loads((task.HERE/'INPUT.json').read_text())
    assert task.ocr.sha(Path(entry['path']))==entry['sha256']==task.ocr.sha(root/'D3_original.png')
    summary=json.loads((root/'SUMMARY.json').read_text())
    records=[json.loads(p.read_text()) for p in sorted(root.glob('*/result.json'))]
    assert len(records)==19
    assert all(not r['tile_errors'] and not r['core_violations'] for r in records)
    with Image.open(root/'D3_original.png') as im:
        base=Image.alpha_composite(Image.new('RGBA',im.size,'white'),im.convert('RGBA')).convert('RGB')
        base=base.resize((1600,900),Image.Resampling.LANCZOS)
    free=[];controls=[]
    for row in summary['cases']:
        if row['status']!='RENDERED':continue
        with Image.open(root/'synthetic'/(row['case']+'.png')) as im:
            exact=im.crop((453,61,1147,839)).tobytes()==base.crop((453,61,1147,839)).tobytes()
            assert exact==row['core_identical_to_base']
            if row['zone']=='free':assert exact;free.append(row['case'])
            else:assert not exact;controls.append(row['case'])
    # Re-run unchanged checks, capturing their JSON in memory instead of rewriting frozen files.
    sys.path.insert(0,str(task.HERE.parent))
    import check_runner,check_injections
    captured={};writer=task.ocr.write_json
    try:
        task.ocr.write_json=lambda path,value:captured.update({Path(path).name:value})
        with contextlib.redirect_stdout(io.StringIO()):
            check_runner.main();check_injections.main()
    finally:task.ocr.write_json=writer
    assert captured['RUNNER_CHECKS.json']['passed']==22
    assert captured['CHECKS.json']['passed']==22
    task.verify(Path('/tmp/contrast02-ocr.5L2pPS/vision_ocr'))
    report={'status':'PASS_INTEGRITY_NOT_SENSITIVITY_ACCEPTANCE','freezes':freezes,
            'output_hashes_verified':len(manifest),'input_bytes_unchanged':True,
            'ocr_images':len(records),'tiles':sum(len(r['tiles']) for r in records),
            'raw_findings':sum(len(r['findings']) for r in records),
            'unique_findings':sum(sum(r['unique_counts'].values()) for r in records),
            'engine_errors':0,'core_violations':0,'free_injections_core_exact':free,
            'intentional_core_control_copies':controls,
            'unit_checks':{k:v['passed'] for k,v in captured.items()},
            'sensitivity_acceptance':False,'reason':'80px coverage absent; report classification failures separately'}
    writer(task.HERE/'VALIDATION.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
