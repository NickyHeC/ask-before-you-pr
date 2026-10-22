# usage: blind.py outprefix idletter outdir
# Takes the first 50 valid PRs of each pool, shuffles them together and copies their material under blind IDs.
import sys, json, random, shutil, os
o,pre,R=sys.argv[1],sys.argv[2],sys.argv[3]
def meta(n): return json.load(open(f'raw_{o}/{n}.json'))
excl=[]
def take(fn, k, check_super):
    out=[]
    for l in open(fn):
        n=l.split('\t')[0]
        if not os.path.exists(f'raw_{o}/{n}.json'): excl.append((n,'not fetched')); continue
        m=meta(n)
        if m['base'] not in ('main','master'): excl.append((n,'base '+m['base'])); continue
        if check_super and m['super_hits']: excl.append((n,'superseded by same-author merged PR')); continue
        out.append(n)
        if len(out)>=k: break
    return out
rej=take(f'{o}_rej_order.tsv',50,True); mer=take(f'{o}_mer_order.tsv',50,False)
allp=[(n,'rejected') for n in rej]+[(n,'merged') for n in mer]
allp.sort(key=lambda x:int(x[0])); random.Random(5353).shuffle(allp)
d=os.path.join(R,o); os.makedirs(f'{d}/material',exist_ok=True); os.makedirs(f'{d}/meta',exist_ok=True)
with open(f'{d}/blind_key.tsv','w') as f:
    f.write('id\tpr\tgroup\n')
    for i,(n,g) in enumerate(allp,1):
        idd=f'{pre}{i:03d}'
        f.write(f'{idd}\t{n}\t{g}\n')
        shutil.copy(f'raw_{o}/{n}.txt',f'{d}/material/{idd}.txt'); shutil.copy(f'raw_{o}/{n}.json',f'{d}/meta/{n}.json')
for g,L in (('rejected',rej),('merged',mer)):
    open(f'{d}/sample_{g}.txt','w').write('\n'.join(L)+'\n')
open(f'{d}/draw_exclusions.txt','w').write(''.join(f'{n}\t{why}\n' for n,why in excl))
print(o,'rejected',len(rej),'merged',len(mer),'exclusions',excl)
