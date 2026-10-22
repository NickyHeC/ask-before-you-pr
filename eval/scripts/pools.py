# usage: pools.py outprefix
# Builds the rejected and merged pools (external authors, not drafts, based on main or master),
# the core-team set, and each pool in its seeded random order.
import sys, re, json, random
o = sys.argv[1]
def rows(fn): return [l.rstrip('\n').split('\t') for l in open(fn) if l.strip()]
U=rows(f'{o}_unmerged.tsv'); M=rows(f'{o}_merged.tsv')
CL={r[0]:(r+['']*4)[1:4] for r in rows(f'{o}_closers.tsv')}   # closer, type, base
MB={r[0]:(r+['']*4)[1:4] for r in rows(f'{o}_mergedby.tsv')}  # base, merged_by, author
isbot=lambda login,typ: typ=='Bot' or login.endswith('[bot]') or login in ('dependabot','renovate','github-actions')
core=set()
for r in U:
    c,t,_=CL.get(r[0],('','',''))
    if c and c!=r[1] and not isbot(c,t): core.add(c)
for r in MB.values():
    if r[1]: core.add(r[1])
for r in U+M:
    if r[3] in ('MEMBER','OWNER','COLLABORATOR'): core.add(r[1])
core.discard('')
json.dump(sorted(core),open(f'{o}_core.json','w'))
ext=lambda r: not isbot(r[1],r[2]) and r[1] not in core
st={}; inc=lambda k: st.__setitem__(k,st.get(k,0)+1)
rej=[]
for r in U:
    c,t,base=CL.get(r[0],('','',''))
    if not ext(r): inc('u_core_or_bot'); continue
    if r[6]=='true': inc('u_draft'); continue
    if c==r[1]: inc('u_self_closed'); continue
    if not c or isbot(c,t): inc('u_bot_or_unknown_closer'); continue
    if base not in ('main','master'): inc('u_base_not_main'); continue
    rej.append(r+[c])
dep=re.compile(r'\b(bump|deps?|dependabot|renovate)\b',re.I)
mer=[]
for r in M:
    if not ext(r): inc('m_core_or_bot'); continue
    if dep.search(r[7]): inc('m_dep_title'); continue
    if MB.get(r[0],('',))[0] not in ('main','master'): inc('m_base_not_main'); continue
    mer.append(r)
st['rejected_pool']=len(rej); st['merged_pool']=len(mer)
for name,L in (('rej',rej),('mer',mer)):
    L.sort(key=lambda r:int(r[0])); random.Random(20261022).shuffle(L)
    with open(f'{o}_{name}_order.tsv','w') as f:
        for r in L: f.write('\t'.join(r)+'\n')
print(o, st, 'core', len(core))
