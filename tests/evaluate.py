#!/usr/bin/env python3
"""Optional paired Chat Completions evaluation; Python standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import random
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ['character_fidelity', 'speech_naturalness', 'appropriate_profanity', 'emotional_credibility', 'administrative_usefulness', 'continuity_integrity', 'factual_action_honesty']


def load_prompts():
    baseline = (ROOT/'originals/Revy_Project_Instructions.md').read_text() + '\n\n' + (ROOT/'originals/Revy_Master_Personality_and_Operating_Reference.md').read_text()
    revised = (ROOT/'output/Revy_Project_Instructions_Optimized.md').read_text() + '\n\n' + (ROOT/'output/Revy_Master_Reference_Optimized.md').read_text()
    return {'baseline': baseline, 'revised': revised}


def request_messages(prompt, case):
    return [dict(role='system', content=prompt), dict(role='system', content='Evaluation fixture facts (not additional character guidance):\n'+case['context'])] + case['messages']


def call_api(endpoint, key, payload):
    request = urllib.request.Request(endpoint, data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer '+key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.load(response)
    except (urllib.error.URLError, TimeoutError):
        # Never include provider response bodies or authorization data in logs.
        raise RuntimeError('API request failed; inspect provider/network settings securely.') from None
    try:
        choice = data['choices'][0]
        if choice.get('finish_reason') != 'stop':
            raise RuntimeError('Completion was truncated or did not finish normally; run is incomplete.')
        text = choice['message']['content']
        if not isinstance(text, str) or not text.strip():
            raise ValueError()
        return text
    except (KeyError, IndexError, TypeError, ValueError):
        raise RuntimeError('API returned no usable text completion.') from None


def generate(args):
    cases = json.loads((ROOT/'tests/scenarios.json').read_text())
    prompts = load_prompts()
    if args.samples < 2:
        raise ValueError('At least two samples are required for comparison.')
    jobs = [(case, sample, variant) for case in cases for sample in range(args.samples) for variant in prompts]
    random.Random(args.order_seed).shuffle(jobs)
    endpoint = os.environ.get('REVY_EVAL_ENDPOINT', '')
    key = os.environ.get('REVY_EVAL_API_KEY', '')
    if not args.dry_run:
        u = urllib.parse.urlsplit(endpoint)
        if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment:
            raise ValueError('Set a credential-free HTTPS REVY_EVAL_ENDPOINT and REVY_EVAL_API_KEY securely.')
        if not key:
            raise ValueError('REVY_EVAL_API_KEY is missing; no calls made.')
    args.out.mkdir(parents=True, exist_ok=False)
    manifest = dict(status='DRY RUN' if args.dry_run else 'IN PROGRESS', model=args.model, samples=args.samples, order_seed=args.order_seed, temperature=args.temperature, max_tokens=args.max_tokens, planned_requests=len(jobs), completed_requests=0, prompt_sha256={k:hashlib.sha256(v.encode()).hexdigest() for k,v in prompts.items()}, dataset_sha256=hashlib.sha256((ROOT/'tests/scenarios.json').read_bytes()).hexdigest(), endpoint_host=urllib.parse.urlsplit(endpoint).hostname if endpoint else None, limitations='Full master text supplied; no ChatGPT retrieval, voice audio, or memory persistence tested. Synthetic fixtures only.')
    manifest_path = args.out/'manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2)+'\n')
    try:
        with (args.out/'responses.jsonl').open('x') as responses, (args.out/'scores_template.jsonl').open('x') as scores:
            for case,sample,variant in jobs:
                payload = dict(model=args.model, temperature=args.temperature, max_tokens=args.max_tokens, messages=request_messages(prompts[variant],case))
                if args.dry_run:
                    continue
                response = call_api(endpoint,key,payload)
                record = dict(case_id=case['id'], sample=sample, variant=variant, response=response)
                responses.write(json.dumps(record,ensure_ascii=False)+'\n'); responses.flush()
                scores.write(json.dumps(dict(case_id=case['id'],sample=sample,variant=variant,scores={d:None for d in DIMENSIONS},critical_failure=None,notes=''))+'\n'); scores.flush()
                manifest['completed_requests'] += 1
        manifest['status'] = 'DRY RUN' if args.dry_run else 'GENERATED — UNSCORED'
    except Exception:
        manifest['status'] = 'FAILED — PARTIAL RESULTS, NOT A COMPLETE COMPARISON'
        raise
    finally:
        manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(f"{manifest['status']}: {manifest['completed_requests']}/{len(jobs)} requests executed")


def summarize(scores_path, out):
    rows = [json.loads(line) for line in scores_path.read_text().splitlines() if line.strip()]
    cases = {x['id']:x for x in json.loads((ROOT/'tests/scenarios.json').read_text())}
    seen=set(); variants={v:[] for v in ('baseline','revised')}
    for r in rows:
        key=(r['case_id'],r['sample'],r['variant'])
        if r['case_id'] not in cases or r['variant'] not in variants or type(r['sample']) is not int or r['sample']<0 or key in seen:
            raise ValueError('Invalid or duplicate score record')
        seen.add(key)
        if set(r['scores'])!=set(DIMENSIONS) or any(type(v) is not int or not 1<=v<=5 for v in r['scores'].values()):
            raise ValueError('Every dimension needs an integer score 1–5')
        if type(r['critical_failure']) is not bool or not r['notes'].strip():
            raise ValueError('Critical-failure boolean and scoring evidence are required')
        variants[r['variant']].append(r)
    samples={r['sample'] for r in rows}
    if len(samples)<2 or samples!=set(range(len(samples))) or seen!={(c,s,v) for c in cases for s in samples for v in variants}:
        raise ValueError('Require complete matched baseline/revised scores for every case and at least two samples')
    report={'status':'HUMAN-SCORED; subjective behavioral assessment', 'samples':len(samples),'variants':{}}
    for variant, group in variants.items():
        means={d:sum(r['scores'][d] for r in group)/len(group) for d in DIMENSIONS}
        failed=[r for r in group if r['critical_failure']]
        categories={cat:{d:sum(r['scores'][d] for r in group if cases[r['case_id']]['category']==cat)/sum(cases[r['case_id']]['category']==cat for r in group) for d in DIMENSIONS} for cat in sorted({c['category'] for c in cases.values()})}
        accepted=not failed and all(x>=4 for x in means.values()) and all(x>=3.5 for ds in categories.values() for x in ds.values())
        report['variants'][variant]=dict(means=means,critical_failures=len(failed),category_means=categories,numerical_thresholds_met=accepted)
    report['revised_minus_baseline']={d:report['variants']['revised']['means'][d]-report['variants']['baseline']['means'][d] for d in DIMENSIONS}
    report['no_dimension_regression']=all(x>=0 for x in report['revised_minus_baseline'].values())
    report['overall_acceptance'] = 'PENDING HUMAN QUALITATIVE REVIEW'
    report['comparison_numerical_thresholds_met'] = report['variants']['revised']['numerical_thresholds_met'] and report['no_dimension_regression']
    out.write_text(json.dumps(report,indent=2)+'\n')
    print('Wrote scored comparison')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    g=sub.add_parser('generate'); g.add_argument('--model',required=True);g.add_argument('--samples',type=int,default=3);g.add_argument('--temperature',type=float,default=.7);g.add_argument('--max-tokens',type=int,default=600);g.add_argument('--order-seed',type=int,default=20261031);g.add_argument('--dry-run',action='store_true');g.add_argument('--out',type=Path,required=True)
    s=sub.add_parser('summarize');s.add_argument('--scores',type=Path,required=True);s.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    if args.command=='generate':generate(args)
    else:summarize(args.scores,args.out)

if __name__=='__main__':main()
