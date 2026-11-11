"""Check reproducibility metadata and summarize student experiment observations."""
import json

import statistics
def analyze(data):
    metadata=data.get('metadata',{})
    required=['question','method','dataset','limitations','seed']
    missing=[k for k in required if k not in metadata or metadata[k] is None or metadata[k]=='']
    runs=data.get('runs',[])
    if len({r['id'] for r in runs})!=len(runs): raise ValueError('Duplicate run ids')
    groups={}
    for run in runs:
        groups.setdefault(run['group'],[]).append(run['value'])
    summary=[]
    for name,values in sorted(groups.items()):
        summary.append({'group':name,'n':len(values),'mean':sum(values)/len(values),'min':min(values),'max':max(values), 'sample_sd':statistics.stdev(values) if len(values)>1 else None})
    return {'missing_metadata':missing,'summary':summary,'reproducibility_status':'incomplete' if missing else 'metadata-present-not-independently-verified'}

if __name__ == '__main__':
    import argparse, sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', help='Path to a JSON scenario')
    args = parser.parse_args()
    try:
        with open(args.input, encoding='utf-8') as source:
            data = json.load(source)
        if not isinstance(data, dict):
            raise ValueError('Input must be a JSON object')
        print(json.dumps(analyze(data), indent=2, sort_keys=True))
    except (ValueError, TypeError, KeyError, OSError) as error:
        print('Input error: '+str(error), file=sys.stderr)
        sys.exit(2)
