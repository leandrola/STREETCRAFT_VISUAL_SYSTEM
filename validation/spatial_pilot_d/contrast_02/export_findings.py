"""Human-readable export of persisted predictions, without reclassification."""
import json
from pathlib import Path
from run_ocr import HERE


def main():
    root=HERE/'runs'/'contrast02_20261019'
    lines=['# OCR findings · immutable prediction export','',
           'All raw tile detections and groups are retained in each result.json. ',
           'This table collapses only recorded same-class tile duplicates; crop links show original pixels.',
           'RAW_UNREVIEWED has no spatial verdict. No thresholds were changed.','']
    for case in ('v1_D_2','v1_D_1','source_D','legacy_191_D'):
        result=json.loads((root/case/'result.json').read_text())
        lines += [f'## {case}','',f"Status: {result['status']}. Raw findings: {len(result['findings'])}.",'',
                  '| ID / crop | Text | Confidence | Box xyxy normalized | Class |',
                  '| --- | --- | --- | --- | --- |']
        for d in result['findings']:
            if d['deduplicated_into']:continue
            box=', '.join(f'{v:.5f}' for v in d['box_normalized'])
            text=d['text'].replace('|','\\|')
            lines.append(f"| [{d['id']}](runs/contrast02_20261019/{d['crop']}) | {text} | {d['confidence']:.3f} | {box} | {d['classification']} |")
        lines.append('')
    (HERE/'FINDINGS.md').write_text('\n'.join(lines)+'\n')


if __name__=='__main__':
    main()
