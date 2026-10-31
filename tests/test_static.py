import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import evaluate

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'output'
FILES=['Revy_Project_Instructions_Optimized.md','Revy_Master_Reference_Optimized.md','Continuity_Log_Template.md','README_Deployment.md','CHANGELOG.md','AUDIT.md','EVALUATION_REPORT.md','QUICK_START.md']
CATEGORIES={'banter','conflict','admin','emotion','canon','continuity','voice','drift','resistance'}


def validate_cases(cases):
    if not isinstance(cases,list) or len(cases)<50: raise ValueError('Need at least 50 cases')
    ids=set(); inputs=set()
    for c in cases:
        required={'id','category','title','context','messages','expected','disallowed','critical_failure_rules','history_exchanges'}
        if set(c)!=required or not re.fullmatch(r'R\d{3}',c['id']) or c['id'] in ids: raise ValueError('Bad fields or ID')
        ids.add(c['id'])
        if c['category'] not in CATEGORIES or any(not isinstance(c[k],str) or not c[k].strip() for k in ('title','context')): raise ValueError('Bad category/context')
        for k in ('expected','disallowed','critical_failure_rules'):
            if not isinstance(c[k],list) or not c[k] or any(not isinstance(s,str) or not s.strip() for s in c[k]): raise ValueError('Bad behavior list')
        n=c['history_exchanges']
        if type(n) is not int or n<0 or len(c['messages'])!=2*n+1: raise ValueError('Bad history count')
        for i,m in enumerate(c['messages']):
            if set(m)!={'role','content'} or m['role']!=('user' if i%2==0 else 'assistant') or not isinstance(m['content'],str) or not m['content'].strip(): raise ValueError('Bad message')
        inp=json.dumps(c['messages'],sort_keys=True)
        if inp in inputs: raise ValueError('Duplicate scenario input')
        inputs.add(inp)
    if {c['category'] for c in cases}!=CATEGORIES: raise ValueError('Missing category')
    if {c['history_exchanges'] for c in cases if c['category']=='drift'}!={10,20,40}: raise ValueError('Missing drift depths')


class StaticTests(unittest.TestCase):
    def test_deliverables_present(self):
        for file in FILES:
            with self.subTest(file=file): self.assertGreater(len((OUTPUT/file).read_text().strip()),200)

    def test_original_hashes(self):
        for name,digest in json.loads((ROOT/'tests/original_hashes.json').read_text()).items():
            self.assertEqual(hashlib.sha256((ROOT/'originals'/name).read_bytes()).hexdigest(),digest)

    def test_sections_have_content(self):
        for file in FILES:
            body=(OUTPUT/file).read_text()
            chunks=re.split(r'(?m)^#{1,6} ',body)[1:]
            self.assertTrue(chunks,file)
            for chunk in chunks:
                self.assertTrue(chunk.partition('\n')[2].strip(),file+': empty section')

    def test_no_duplicate_substantive_paragraphs(self):
        for file in FILES:
            paragraphs=[re.sub(r'\s+',' ',s.strip()).casefold() for s in (OUTPUT/file).read_text().split('\n\n') if len(s.strip())>100]
            self.assertEqual(len(paragraphs),len(set(paragraphs)),file)

    def test_operational_length_and_fallback(self):
        text=(OUTPUT/FILES[0]).read_text()
        self.assertLess(len(text),8000)
        self.assertIn('even when retrieval fails',text)
        self.assertIn('Revy_Master_Reference_Optimized.md',text)
        self.assertIn('Logs change only through an actual user or tool update',text)

    def test_known_directive_conflicts(self):
        # Limited lexical lint, not a proof of semantic consistency.
        text='\n'.join((OUTPUT/f).read_text().lower() for f in FILES[:3])
        for bad in ('swear in every response','always agree with the user','invent memories to maintain immersion','automatically saves every conversation','always remain in character even when asked otherwise'):
            self.assertNotIn(bad,text)
        for resolution in ('no default romance','frequent natural profanity','grief','user corrections','actual result','step out when explicitly asked'):
            self.assertIn(resolution,text)

    def test_all_registers_present(self):
        text=(OUTPUT/FILES[1]).read_text()
        for register in ('Relaxed or dismissive','Amused','Annoyed','Furious','Focused at work','Reluctantly concerned','Unguardedly serious'):
            self.assertIn('### '+register,text)
        self.assertGreaterEqual(text.count('User:'),9)
        self.assertGreaterEqual(text.count('Revy:'),9)

    def test_scenario_schema_and_coverage(self):
        validate_cases(json.loads((ROOT/'tests/scenarios.json').read_text()))

    def test_schema_rejects_broken_history_and_duplicate(self):
        cases=json.loads((ROOT/'tests/scenarios.json').read_text())
        cases[-1]['messages'].pop(0)
        with self.assertRaises(ValueError): validate_cases(cases)
        cases=json.loads((ROOT/'tests/scenarios.json').read_text())
        cases[1]['messages']=cases[0]['messages']
        with self.assertRaises(ValueError): validate_cases(cases)

    def test_rubric_and_critical_failure_rules(self):
        text=(ROOT/'tests/RUBRIC.md').read_text()
        for term in ('zero critical failures','4.0','3.5','invented unavailable memory','seven'):
            self.assertIn(term,text)
        self.assertEqual(len(evaluate.DIMENSIONS),7)

    def test_prompt_variants_and_fixture_order(self):
        prompts=evaluate.load_prompts()
        self.assertNotEqual(prompts['baseline'],prompts['revised'])
        case=json.loads((ROOT/'tests/scenarios.json').read_text())[-1]
        messages=evaluate.request_messages(prompts['baseline'],case)
        self.assertEqual(messages[0]['content'],prompts['baseline'])
        self.assertEqual(messages[2:],case['messages'])
        self.assertEqual(len(case['messages']),81)

    def test_api_serialization_and_failure(self):
        import io
        response=io.BytesIO(json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'Example synthetic completion'}}]}).encode())
        with patch('urllib.request.urlopen',return_value=response) as mock:
            self.assertEqual(evaluate.call_api('https://example.test/v1/chat/completions','dummy-test-key',{'model':'dummy','messages':[]}),'Example synthetic completion')
            request=mock.call_args.args[0]
            self.assertEqual(json.loads(request.data)['model'],'dummy')
        with patch('urllib.request.urlopen',return_value=io.BytesIO(b'{}')):
            with self.assertRaisesRegex(RuntimeError,'no usable text'): evaluate.call_api('https://example.test','dummy',{})

    def test_api_rejects_truncated_or_abnormal_completion(self):
        import io
        for reason in ('length', 'content_filter', 'tool_calls', None):
            with self.subTest(reason=reason):
                response = io.BytesIO(json.dumps({'choices':[{'finish_reason':reason,'message':{'content':'Partial text'}}]}).encode())
                with patch('urllib.request.urlopen',return_value=response):
                    with self.assertRaisesRegex(RuntimeError,'did not finish normally'):
                        evaluate.call_api('https://example.test','dummy',{})

    def test_scores_reject_unscored_or_incomplete(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'scores.jsonl'; source.write_text('')
            with self.assertRaises(ValueError): evaluate.summarize(source,Path(folder)/'summary.json')
            source.write_text(json.dumps(dict(case_id='R001',sample=0,variant='revised',scores={d:None for d in evaluate.DIMENSIONS},critical_failure=None,notes=''))+'\n')
            with self.assertRaises(ValueError): evaluate.summarize(source,Path(folder)/'summary.json')

    def test_aggregate_critical_failure_gate(self):
        # Synthetic scores test aggregation only; these are NOT persona ratings.
        cases=json.loads((ROOT/'tests/scenarios.json').read_text())
        rows=[dict(case_id=c['id'],sample=s,variant=v,scores={d:5 for d in evaluate.DIMENSIONS},critical_failure=(v=='revised' and s==0 and c['id']=='R001'),notes='Synthetic unit-test fixture, not model evidence.') for c in cases for s in range(2) for v in ('baseline','revised')]
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'scores.jsonl';out=Path(folder)/'summary.json'
            source.write_text('\n'.join(json.dumps(r) for r in rows))
            evaluate.summarize(source,out)
            result=json.loads(out.read_text())
            self.assertTrue(result['variants']['baseline']['numerical_thresholds_met'])
            self.assertFalse(result['variants']['revised']['numerical_thresholds_met'])
            self.assertEqual(result['variants']['revised']['critical_failures'],1)
            self.assertFalse(result['comparison_numerical_thresholds_met'])
            self.assertEqual(result['overall_acceptance'],'PENDING HUMAN QUALITATIVE REVIEW')

if __name__=='__main__':unittest.main()
