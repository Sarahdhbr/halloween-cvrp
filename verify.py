"""Independent consistency checks of saved data, recomputed algorithms and media."""
from common import *
import importlib.util,hashlib
count=0

def require(condition,label):
 global count
 count+=1
 if not condition:raise AssertionError(label)

cw_routes,merges,decisions=cw();require(cw_routes==DATA['initial']['routes'],'CW exact route sequence');require(len(merges)==23 and len(decisions)==171,'CW merge decisions');require(abs(total(cw_routes)-673.0424007707024)<1e-8,'CW reference cost')
reference=ROOT/'data/original-instance.json'
if reference.exists():
 original=json.loads(reference.read_text());require(original['nodes']==DATA['nodes'],'Coordinates and demands unchanged');require(original['Q']==Q and original['k']==K,'Capacity and fleet unchanged');require(original['initial']==DATA['initial']['routes'],'Original CW unchanged');require(original['final']==DATA['final'],'Original method unchanged')
for label,rs,value,exact in [('CW',cw_routes,673.0424007707024,True),('Method',DATA['final'],663.1603652052456,True),('Exactly-seven MILP',EXACT['routes'],EXACT['cost'],True),('At-most-seven MILP',ATMOST['routes'],ATMOST['cost'],False)]:
 for test,ok in check(rs,exact_fleet=exact).items():require(ok,label+': '+test)
 require(abs(total(rs)-value)<1e-8,label+': distance')
 for r in rs:
  length=0
  for i,j in zip(r,r[1:]):
   for f in [.01,.5,.99]:
    pos,travel,q,fr,to=state(r,length+f*DIST[i,j]);require(np.allclose(pos,(1-f)*XY[i]+f*XY[j],atol=1e-10),'Position is on calculated arc');require(fr==i and to==j,'Actual edge endpoints');require(abs(travel-length-f*DIST[i,j])<1e-8,'Animated distance')
   length+=DIST[i,j]
current=cw_routes
for h in DATA['history']:
 require(current==h['before'],'History chain');require(select_subproblem(current,h['iteration'])==h['selected'],'Centroid selection recomputed');value,chosen=partition(h['ids'],h['pool'],len(h['selected']));require(list(chosen)==h['chosen'],'Exact pool DP matches existing result');require(abs(value-h['newCost'])<1e-8,'Pool objective')
 for r in h['pool']:
  require(load(r)<=Q and r[0]==r[-1]==0,'Candidate capacity and returns');require(len(r[1:-1])==len(set(r[1:-1])) and set(r[1:-1])<=set(h['ids']),'Candidate subset coverage')
 chosen_rs=[h['pool'][p] for p in chosen]
 for key,ok in check(chosen_rs,h['ids'],exact_fleet=True,limit=len(h['selected'])).items():require(ok,'Selected partition '+key)
 require(h['accepted']==(value<h['oldCost']-1e-7),'Unchanged acceptance rule')
 if h['accepted']:
  current=[r[:] for r in current]
  for slot,r in zip(h['selected'],chosen_rs):current[slot]=r
 require(current==h['after'],'Assembled full solution')
require(current==DATA['final'],'Final unchanged solution');require(EXACT['certifiedOptimal'] and EXACT['statusCode']==0,'Seven-route certificate');require(not ATMOST['certifiedOptimal'] and ATMOST['statusCode']==1,'At-most-seven no certificate');require(abs((ATMOST['cost']-ATMOST['bestBound'])/ATMOST['cost']-ATMOST['gap'])<1e-10,'Reported gap');require(abs(total(align(DATA['final'],EXACT['routes']))-EXACT['cost'])<1e-8,'Colour assignment preserves cost')
spec=importlib.util.spec_from_file_location('green',ROOT/'06_green_resources.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);visits=[]
for r in g.G['routes']:
 require(r[0]==r[-1]==0,'Green depot returns');require(g.duration(r)<=g.T,'Green duration');fuel=g.B;elapsed=0
 for k,(i,j) in enumerate(zip(r,r[1:]),1):
  distance=g.GD[i,j];require(distance<=fuel,'Green fuel feasible');s=g.green_state(r,elapsed+.5*distance/g.V);require(np.allclose(s[0],.5*(g.GX[i]+g.GX[j])),'Green midpoint follows arc');require(abs(s[1]-(fuel-.5*distance))<1e-8,'Green continuous fuel')
  fuel-=distance;elapsed+=distance/g.V
  if 0<j<=30:visits.append(j)
  if k<len(r)-1:elapsed+=g.R if j==0 or j>30 else g.S
  if j==0 or j>30:fuel=g.B
require(sorted(visits)==list(range(1,31)),'Green exact customer coverage');require(len(g.G['routes'])==7,'Green saved fleet');require(len(g.GX)==39,'Eight saved stations')
for x,y in [(XY[:,0],XY[:,1]),(100-XY[:,0],XY[:,1]),(XY[:,0],100-XY[:,1]),(100-XY[:,0],100-XY[:,1]),(XY[:,1],XY[:,0]),(100-XY[:,1],XY[:,0]),(XY[:,1],100-XY[:,0]),(100-XY[:,1],100-XY[:,0])]:
 p=np.c_[x,y];require(np.allclose(np.linalg.norm(p[:,None]-p[None,:],axis=2),DIST),'POMO symmetry preserves costs')
# Real capacity violation, rather than an arbitrary short route.
violation=[0];q=0
for i in range(1,31):
 violation.append(i);q+=DEMAND[i]
 if q>Q:break
violation.append(0);require(load(violation)>Q,'Capacity violation example')
from PIL import Image
import cv2
media=[]
for p in sorted((ROOT/'outputs').rglob('*.gif')):
 im=Image.open(p);require(im.n_frames>1,'Real animated GIF '+p.name);cap=cv2.VideoCapture(str(p.with_suffix('.mp4')));frames=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  frames+=1
 cap.release();require(frames>=2,'MP4 decodes '+p.name);media.append({'gif':str(p.relative_to(ROOT/'outputs')),'gifFrames':im.n_frames,'mp4DecodedFrames':frames})
report={'checks':count,'Q':Q,'fleet':K,'totalDemand':int(DEMAND.sum()),'cwCost':total(cw_routes),'methodCost':total(current),'exactSevenCost':EXACT['cost'],'atMostSevenCost':ATMOST['cost'],'acceptedIterations':[h['iteration'] for h in DATA['history'] if h['accepted']],'media':media,'scope':'No neural inference. Candidate generation and MILP are saved executions; CW and pool DP recomputed.'}
(ROOT/'outputs').mkdir(exist_ok=True);(ROOT/'outputs/verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
