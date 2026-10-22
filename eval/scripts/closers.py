# usage: closers.py owner/repo outprefix -> <o>_closers.tsv (number, closer, closer_type, base) and <o>_mergedby.tsv (number, base, merged_by, author)
import sys, json, subprocess
repo,o=sys.argv[1],sys.argv[2]; owner,name=repo.split('/')
def nums(fn): return [l.split('\t')[0] for l in open(fn) if l.strip()]
def gql(q):
    for _ in range(4):
        r=subprocess.run(['gh','api','graphql','-f','query='+q],capture_output=True,text=True)
        try:
            d=json.loads(r.stdout)
            if 'data' in d and d['data']: return d
        except Exception: pass
    return {}
def run(ns, frag):
    out={}
    for i in range(0,len(ns),40):
        ch=ns[i:i+40]
        q='{repository(owner:"%s",name:"%s"){'%(owner,name)+' '.join('p%s:pullRequest(number:%s){%s}'%(n,n,frag) for n in ch)+'}}'
        d=gql(q); rep=(d.get('data') or {}).get('repository') or {}
        for n in ch: out[n]=rep.get('p'+n)
    return out
U=run(nums(f'{o}_unmerged.tsv'),'baseRefName author{login} timelineItems(itemTypes:[CLOSED_EVENT],last:1){nodes{... on ClosedEvent{actor{login __typename}}}}')
with open(f'{o}_closers.tsv','w') as f:
    for n,v in U.items():
        if not v: f.write(f'{n}\t\t\t\n'); continue
        nodes=v['timelineItems']['nodes']; a=(nodes[-1].get('actor') if nodes else None) or {}
        f.write(f"{n}\t{a.get('login','')}\t{a.get('__typename','')}\t{v['baseRefName']}\n")
M=run(nums(f'{o}_merged.tsv'),'baseRefName author{login} mergedBy{login}')
with open(f'{o}_mergedby.tsv','w') as f:
    for n,v in M.items():
        if not v: f.write(f'{n}\t\t\t\n'); continue
        f.write(f"{n}\t{v['baseRefName']}\t{(v.get('mergedBy') or {}).get('login','')}\t{(v.get('author') or {}).get('login','')}\n")
print(o,'closers',len(U),'missing',sum(1 for v in U.values() if not v),'mergedby',len(M),'missing',sum(1 for v in M.values() if not v))
