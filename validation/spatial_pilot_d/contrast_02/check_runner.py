"""Pre-freeze unit checks on metadata only; not OCR sensitivity or image injection."""
import json
from pathlib import Path
import run_ocr as r


def main():
    whitelist=json.loads((r.HERE/'PROTOCOL_CANDIDATE.json').read_text())['whitelist']
    checks=[]
    def check(name, result):
        checks.append({'case':name,'pass':bool(result)})
        assert result,name
    def label(text='NOVA DEPOT',confidence=.60,box=(0,0,.1,.01),core=(.2,0,.89,.94)):
        return r.classify(text,confidence,box,(1600,1600),core,whitelist)['classification']
    check('violation_at_confidence_boundary',label()=='VIOLACION')
    check('low_confidence_warning',label(confidence=.599)=='ADVERTENCIA')
    check('short_string_warning',label(text='AB')=='ADVERTENCIA')
    check('height_below_10_warning',label(box=(0,0,.1,9/1600))=='ADVERTENCIA')
    check('height_10_inclusive',label(box=(0,0,.1,10/1600))=='VIOLACION')
    check('legitimate_core_ignored',label(text='TERMINAL DINER',box=(.3,.2,.5,.3))=='IGNORADO_POR_SOLAPE')
    check('invented_core_ignored',label(box=(.3,.2,.5,.3))=='IGNORADO_POR_SOLAPE')
    check('whitelist_duplicate_warning',label(text='TERMINAL DINER')=='ADVERTENCIA_DUPLICADO')
    check('whitelist_case_punctuation',label(text='l. katzenstein & co.')=='ADVERTENCIA_DUPLICADO')
    check('whitelist_plural',label(text='Business Loan Centers')=='ADVERTENCIA_DUPLICADO')
    check('whitelist_approximate',label(text='TERMINAL D1NER')=='ADVERTENCIA_DUPLICADO')
    check('undefined_zone_raw_only',label(core=None)=='RAW_UNREVIEWED')
    check('overlap_exact_30_not_ignored',label(box=(0,0,1,.01),core=(0,0,.3,1))=='VIOLACION')
    check('overlap_over_30_ignored',label(box=(0,0,1,.01),core=(0,0,.31,1))=='IGNORADO_POR_SOLAPE')
    check('whole_core_no_tiles',r.tile_plan((1600,900),(0,0,1,1))==[])
    check('tile_overlap_and_edge',r.origins(1600)==[0,640,800] and r.origins(901)==[0,101])
    check('small_image_tile',r.tile_plan((500,300),None)==[[0,0,500,300]])
    n,p=r.map_box([0,0,1,1],[800,101,1600,901],(1672,941),(1600,901))
    check('tile_inverse_coordinates',n==[.5,101/901,1,1] and p[0]==836 and p[2:]==[1672,941])
    lines=[{'id':'a','text':'JOHNSON','confidence':.9,'box_normalized':[0,0,.2,.1]},
           {'id':'b','text':'WAREHOUSE','confidence':.8,'box_normalized':[0,.12,.2,.22]}]
    group=r.groups(lines)[0]
    check('line_group_text_and_conservative_confidence',group['text']=='JOHNSON WAREHOUSE' and group['confidence']==.8)
    check('line_group_preserves_constituents',group['constituents']==['a','b'])
    data=[{'id':'a','text':'TEST','confidence':.8,'box_normalized':[0,0,.2,.1],'classification':'VIOLACION'},
          {'id':'b','text':'Test','confidence':.9,'box_normalized':[0,0,.2,.1],'classification':'VIOLACION'},
          {'id':'c','text':'Test','confidence':.95,'box_normalized':[0,0,.2,.1],'classification':'IGNORADO_POR_SOLAPE'}]
    reps=r.deduplicate(data)
    check('duplicate_preserves_strongest_and_raw',len(reps)==2 and data[0]['deduplicated_into']=='b' and len(data)==3)
    check('no_cross_classification_dedup',any(d['classification']=='VIOLACION' for d in reps))
    report={'scope':'METADATA_ONLY_UNIT_TESTS_NO_OCR','passed':len(checks),'checks':checks,
            'does_not_validate':'OCR sensitivity, real good-image specificity or synthetic image recall'}
    r.write_json(r.HERE/'RUNNER_CHECKS.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
