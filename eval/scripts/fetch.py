# usage: fetch.py owner/repo number outdir
# Writes the blinded material a scorer reads (<number>.txt) and metadata scorers never see (<number>.json).
import json, subprocess, sys, re, os
from datetime import datetime, timedelta
REPO=sys.argv[1]; N=sys.argv[2]; OUT=sys.argv[3]
def api(path, paginate=False):
    cmd=['gh','api',path]+(['--paginate'] if paginate else [])
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: return None
    t=r.stdout.strip()
    if paginate and t.startswith('[') and '][' in t: t=t.replace('][',',')
    try: return json.loads(t)
    except Exception: return None
def gql(q):
    r=subprocess.run(['gh','api','graphql','-f','query='+q],capture_output=True,text=True)
    try: return json.loads(r.stdout)
    except Exception: return {}
ts=lambda s: datetime.strptime(s,'%Y-%m-%dT%H:%M:%SZ')
pr=api(f'repos/{REPO}/pulls/{N}')
files=api(f'repos/{REPO}/pulls/{N}/files?per_page=100',True) or []
ic=api(f'repos/{REPO}/issues/{N}/comments?per_page=100',True) or []
rc=api(f'repos/{REPO}/pulls/{N}/comments?per_page=100',True) or []
rv=api(f'repos/{REPO}/pulls/{N}/reviews?per_page=100',True) or []
ev=api(f'repos/{REPO}/issues/{N}/events?per_page=100',True) or []
closed=[e for e in ev if e.get('event')=='closed']
closer=(closed[-1]['actor'] or {}).get('login','') if closed else ''
closed_commit=(closed[-1].get('commit_id') or '') if closed else ''  # recorded in the metadata only, never shown to scorers
owner,name=REPO.split('/')
g=gql('{repository(owner:"%s",name:"%s"){pullRequest(number:%s){closingIssuesReferences(first:5){nodes{number title body}}}}}'%(owner,name,N))
linked=[]
try: linked=g['data']['repository']['pullRequest']['closingIssuesReferences']['nodes']
except Exception: pass
sha=pr['head']['sha']
cr=api(f'repos/{REPO}/commits/{sha}/check-runs?per_page=100') or {}
st=api(f'repos/{REPO}/commits/{sha}/status') or {}
concl={}
for c in cr.get('check_runs',[]):
    k=c.get('conclusion') or c.get('status'); concl[k]=concl.get(k,0)+1
for s in st.get('statuses',[]):
    k='status:'+s.get('state',''); concl[k]=concl.get(k,0)+1
failed=[c['name'] for c in cr.get('check_runs',[]) if c.get('conclusion') in ('failure','cancelled','timed_out')][:6]
close_t=ts(pr['closed_at']) if pr.get('closed_at') else datetime(2026,10,22,7,0)
def keep(user, created):
    t=ts(created)
    if t>close_t: return False
    if user==closer and close_t-t<=timedelta(hours=24): return False
    return True
disc=[]
for c in ic:
    u=(c.get('user') or {}).get('login','')
    if keep(u,c['created_at']): disc.append((c['created_at'],u,'comment',c.get('body') or ''))
for c in rv:
    u=(c.get('user') or {}).get('login','')
    if c.get('submitted_at') and (c.get('body') or '').strip() and keep(u,c['submitted_at']): disc.append((c['submitted_at'],u,'review',c['body']))
for c in rc:
    u=(c.get('user') or {}).get('login','')
    if keep(u,c['created_at']): disc.append((c['created_at'],u,'inline on '+c.get('path',''),c.get('body') or ''))
disc.sort()
author=pr['user']['login']
# refs for supersession check (all comments, including the closing ones)
allbodies=' '.join([c.get('body') or '' for c in ic+rc+rv])
refs=sorted(set(re.findall(r'#(\d{3,7})',allbodies)))
super_hits=[]
for r_ in (refs[:15] if os.environ.get('SUPER')=='1' else []):
    if r_==str(N): continue
    p=api(f'repos/{REPO}/pulls/{r_}')
    if p and p.get('merged_at') and p['user']['login']==author: super_hits.append(r_)
add=sum(f['additions'] for f in files); dele=sum(f['deletions'] for f in files)
def clip(s,n): s=(s or '').strip(); return s if len(s)<=n else s[:n]+' [...truncated]'
lines=[]
lines.append(f"TITLE: {pr['title']}")
lines.append(f"OPENED: {pr['created_at'][:10]}   BASE BRANCH: {pr['base']['ref']}   COMMITS: {pr['commits']}")
lines.append(f"SIZE: {len(files)} files, +{add} -{dele}")
lines.append("BODY:\n"+(clip(pr.get('body'),2500) or '(empty)'))
if linked:
    for li in linked[:2]:
        lines.append(f"LINKED ISSUE #{li['number']}: {li['title']}\n  {clip(li.get('body'),500)}")
else: lines.append("LINKED ISSUE (closing reference): none")
lines.append("FILES:")
for f in files[:25]: lines.append(f"  {f['status']:9} +{f['additions']:<5} -{f['deletions']:<5} {f['filename']}")
if len(files)>25: lines.append(f"  ... and {len(files)-25} more files")
if add+dele<=200:
    patch='\n'.join(f"--- {f['filename']}\n{f.get('patch','(binary or no patch)')}" for f in files)
    lines.append("DIFF:\n"+clip(patch,3000))
else: lines.append("DIFF: (omitted, over 200 changed lines)")
lines.append(f"CI ON FINAL HEAD: {json.dumps(concl) if concl else 'no checks reported'}" + (f"; failed: {', '.join(failed)}" if failed else ''))
lines.append(f"DISCUSSION BEFORE CLOSE ({len(disc)} items, author is A, others by role-neutral initials):")
alias={author:'A'}
def al(u):
    if u not in alias: alias[u]='R%d'%len(alias)
    return alias[u]
for t,u,kind,b in disc[:10]:
    tag=al(u)+(' [bot]' if u.endswith('[bot]') else '')
    lines.append(f"  [{t[:10]}] {tag} ({kind}): {clip(b,500)}")
if len(disc)>10: lines.append(f"  ... {len(disc)-10} more items not shown")
meta=dict(n=int(N), author=author, closer=closer, merged=bool(pr.get('merged_at')), merged_by=(pr.get('merged_by') or {}).get('login',''), draft=pr.get('draft'), add=add, dele=dele, files=len(files), super_hits=super_hits, ndisc=len(disc), base=pr['base']['ref'], linked=[li['number'] for li in linked], checks=concl, closed_commit=closed_commit)
os.makedirs(OUT,exist_ok=True)
open(f'{OUT}/{N}.txt','w').write('\n'.join(lines)+'\n')
open(f'{OUT}/{N}.json','w').write(json.dumps(meta)+'\n')
