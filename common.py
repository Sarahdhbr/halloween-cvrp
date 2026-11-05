"""Fixed-instance computations and plain Matplotlib rendering; no web dependencies."""
from pathlib import Path
import json,os,argparse,math
os.environ.setdefault('MPLCONFIGDIR','/tmp/cvrp-matplotlib')
import numpy as np
import matplotlib
if '--show' not in __import__('sys').argv:matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'data/execution.json').read_text())
EXACT=json.loads((ROOT/'data/exact-seven.json').read_text())
ATMOST=json.loads((ROOT/'data/exact-at-most-seven.json').read_text())
XY=np.array([[n['x'],n['y']] for n in DATA['nodes']]);DEMAND=np.array([n['q'] for n in DATA['nodes']])
Q,K=DATA['Q'],DATA['k'];DIST=np.linalg.norm(XY[:,None]-XY[None,:],axis=2)
COLORS=['#1971c2','#c92a2a','#2b8a3e','#9c36b5','#e67700','#0b7285','#6741d9']
NAMES=['Pennywise','Jason Voorhees','Annabelle','Chucky','Casper','Wednesday','Pumpkin']
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white','pdf.fonttype':42})
def cost(route):return float(sum(DIST[a,b] for a,b in zip(route,route[1:])))
def total(routes):return sum(map(cost,routes))
def load(route):return int(sum(DEMAND[i] for i in route))
def check(routes,ids=None,exact_fleet=False,limit=K):
 ids=list(range(1,31)) if ids is None else list(ids)
 visits=[i for r in routes for i in r[1:-1]]
 return {'coverage':sorted(visits)==sorted(ids),'capacity':all(load(r)<=Q for r in routes),'depot':all(len(r)>=3 and r[0]==r[-1]==0 and 0 not in r[1:-1] for r in routes),'fleet':len(routes)==limit if exact_fleet else len(routes)<=limit}
def cw():
 """Same parallel savings rule, endpoint checks, ties and stop-at-seven as original."""
 rs=[[i] for i in range(1,31)];merges=[];decisions=[]
 savings=sorted([(DIST[0,i]+DIST[0,j]-DIST[i,j],i,j) for i in range(1,31) for j in range(i+1,31)],key=lambda a:(-a[0],a[1],a[2]))
 for saving,i,j in savings:
  if len(rs)<=K:break
  a=next((t for t,r in enumerate(rs) if i in [r[0],r[-1]]),-1);b=next((t for t,r in enumerate(rs) if j in [r[0],r[-1]]),-1)
  reason='Internal customer' if min(a,b)<0 else 'Same route' if a==b else 'Capacity exceeded' if load(rs[a])+load(rs[b])>Q else 'Accepted'
  decisions.append({'i':i,'j':j,'saving':float(saving),'reason':reason})
  if reason!='Accepted':continue
  ra=rs[a] if rs[a][-1]==i else rs[a][::-1];rb=rs[b] if rs[b][0]==j else rs[b][::-1]
  rs=[r for t,r in enumerate(rs) if t not in (a,b)]+[ra+rb]
  merges.append({'i':i,'j':j,'saving':float(saving),'routes':[[0,*r,0] for r in rs]})
 return [[0,*r,0] for r in rs],merges,decisions

def select_subproblem(routes,iteration):
 anchor=(iteration-1)%len(routes)
 centers=np.array([XY[r[1:-1]].mean(axis=0) for r in routes]);origin=centers[anchor]
 order=sorted(range(len(routes)),key=lambda i:(float(np.linalg.norm(centers[i]-origin)),i))
 selected=[];count=0
 for i in order:
  if count+len(routes[i])-2<=15:selected.append(i);count+=len(routes[i])-2
 return selected

def partition(ids,pool,k):
 """Exact set partition of the saved route pool, with exactly k routes."""
 from functools import lru_cache
 masks=[sum(1<<ids.index(i) for i in r[1:-1]) for r in pool];full=(1<<len(ids))-1
 @lru_cache(None)
 def solve(mask,left):
  if mask==full:return (0.,()) if left==0 else None
  if left==0:return None
  first=next(i for i in range(len(ids)) if not mask&(1<<i));best=None
  for p,m in enumerate(masks):
   if m&(1<<first) and not m&mask:
    tail=solve(mask|m,left-1)
    if tail is not None:
     v=cost(pool[p])+tail[0]
     if best is None or v<best[0]-1e-8:best=(v,(p,*tail[1]))
  return best
 return solve(0,k)

def align(reference,routes):
 """Display assignment by maximal customer overlap; does not optimise routes."""
 if len(reference)!=len(routes):return routes
 from functools import lru_cache
 @lru_cache(None)
 def visit(slot,mask):
  if slot==len(reference):return 0,()
  best=None
  for j,r in enumerate(routes):
   if not mask&(1<<j):
    score,tail=visit(slot+1,mask|(1<<j));v=(len(set(reference[slot][1:-1])&set(r[1:-1]))+score,(j,*tail))
    if best is None or v[0]>best[0]:best=v
  return best
 out=[]
 for i,j in enumerate(visit(0,0)[1]):
  r=routes[j][:]
  if reference[i][1]==r[-2]:r=r[::-1]
  out.append(r)
 return out

def state(route,distance,xy=XY,dist=DIST,dem=DEMAND):
 travelled=0.;collected=0
 for a,b in zip(route,route[1:]):
  length=dist[a,b]
  if distance<travelled+length:
   fraction=(distance-travelled)/length
   return xy[a]+fraction*(xy[b]-xy[a]),travelled+fraction*length,collected,a,b
  travelled+=length;collected+=int(dem[b])
 return xy[route[-1]],travelled,collected,route[-1],route[-1]

def graph(ax,title,xy=XY,demands=False):
 ax.set(xlim=(0,100),ylim=(0,100),aspect='equal',xlabel='$x$ (distance units)',ylabel='$y$ (distance units)',title=title)
 ax.set_xticks(np.arange(0,101,20));ax.set_yticks(np.arange(0,101,20));ax.grid(color='.92',lw=.6,zorder=0)
 ax.scatter(xy[1:31,0],xy[1:31,1],s=34,c='white',edgecolors='black',zorder=5)
 ax.scatter(*xy[0],marker='s',s=85,c='black',zorder=6)
 ax.annotate('D',xy[0],xytext=(6,6),textcoords='offset points',weight='bold',zorder=7)
 for i,p in enumerate(xy[1:31],1):ax.annotate(f'{i}'+(f' ($d_{{{i}}}={DEMAND[i]}$)' if demands else ''),p,xytext=({5:(-43,7),6:(3,-12),11:(-53,4),12:(5,-12),22:(-55,4),23:(5,7),29:(-47,7),30:(5,-10)}.get(i,(4,4)) if demands else (4,4)),textcoords='offset points',fontsize=7,zorder=7)

def route_lines(ax,routes,colors=None,alpha=.65,lw=1.7,xy=XY,**kwargs):
 colors=COLORS if colors is None else colors
 for i,r in enumerate(routes):ax.plot(xy[r,0],xy[r,1],color=colors[i%len(colors)],alpha=alpha,lw=lw,zorder=2,**kwargs)
def legend(ax,route_ids=range(7)):
 ax.legend(handles=[Line2D([0],[0],color=COLORS[i],lw=2,label=NAMES[i]) for i in route_ids],loc='upper left',bbox_to_anchor=(1.01,1),frameon=False,fontsize=8)
def save(fig,name,args):
 args.out.mkdir(parents=True,exist_ok=True)
 for ext in ['png','pdf']:fig.savefig(args.out/f'{name}.{ext}',dpi=150,bbox_inches='tight')
def options(description):
 p=argparse.ArgumentParser(description=description);p.add_argument('--portraits',action='store_true',help='Show existing authentic character images, offset from route markers');p.add_argument('--show',action='store_true',help='Open a Matplotlib window; Space pauses, +/- changes speed');p.add_argument('--export',action='store_true',help='Write PNG/PDF and GIF/MP4');p.add_argument('--out',type=Path,default=None);p.add_argument('--frames',type=int,default=120);p.add_argument('--fps',type=int,default=15);a=p.parse_args()
 if a.out is None:a.out=ROOT/'outputs'/('portraits' if a.portraits else '')
 if a.frames<2 or a.fps<1:p.error('frames >= 2 and fps >= 1 are required')
 if not a.show:a.export=True
 return a

def animate(fig,update,name,args):
 """Continuous arc interpolation, GUI key controls, independently decoded media."""
 n=args.frames
 if args.export:
  from PIL import Image
  import cv2
  args.out.mkdir(parents=True,exist_ok=True);frames=[];writer=None;shape=None
  try:
   for i in range(n):
    update(i/(n-1));fig.canvas.draw();rgb=np.asarray(fig.canvas.buffer_rgba())[:,:,:3].copy();h,w=rgb.shape[:2]
    if writer is None:
     shape=(w//2*2,h//2*2);writer=cv2.VideoWriter(str(args.out/f'{name}.mp4'),cv2.VideoWriter_fourcc(*'mp4v'),args.fps,shape)
     if not writer.isOpened():raise RuntimeError('OpenCV MP4 writer unavailable')
    writer.write(cv2.cvtColor(rgb[:shape[1],:shape[0]],cv2.COLOR_RGB2BGR))
    frames.append(Image.fromarray(rgb).quantize(colors=128))
  finally:
   if writer is not None:writer.release()
  frames[0].save(args.out/f'{name}.gif',save_all=True,append_images=frames[1:],duration=[round((i+1)*100/args.fps)*10-round(i*100/args.fps)*10 for i in range(n)],loop=0,optimize=False,disposal=2)
  im=Image.open(args.out/f'{name}.gif');gif_frames=im.n_frames;assert gif_frames>1
  duration=sum(im.seek(i) or im.info.get('duration',0) for i in range(gif_frames))
  cap=cv2.VideoCapture(str(args.out/f'{name}.mp4'));decoded=0;first=None;last=None
  while True:
   ok,frame=cap.read()
   if not ok:break
   if first is None:first=frame.copy()
   last=frame;decoded+=1
  fps=cap.get(cv2.CAP_PROP_FPS);cap.release();assert decoded==n and fps>0
  assert np.mean(np.abs(first.astype(float)-last.astype(float)))>.001,'Video is static'
  report={'gifEncodedFrames':gif_frames,'sampleCount':n,'gifDurationMs':duration,'mp4DecodedFrames':decoded,'mp4Fps':fps,'mp4Dimensions':shape,'codec':'MPEG-4 Part 2 (mp4v)','mp4DurationSeconds':decoded/fps}
  (args.out/f'{name}.verification.json').write_text(json.dumps(report,indent=2)+'\n');print(name,report,flush=True)
 if args.show:
  progress=[0.];speed=[1.];paused=[False]
  def tick(_):
   if not paused[0]:progress[0]=(progress[0]+speed[0]/n)%1
   return update(progress[0]) or []
  animation=FuncAnimation(fig,tick,interval=1000/args.fps,cache_frame_data=False)
  def key(event):
   if event.key in [' ','p']:paused[0]=not paused[0]
   elif event.key in ['+','=']:speed[0]=min(8.,speed[0]*2)
   elif event.key=='-':speed[0]=max(.125,speed[0]/2)
   elif event.key=='r':progress[0]=0.
   fig.canvas.manager.set_window_title(f'{name} | Space: pause/resume | +/-: speed {speed[0]:g}x | R: restart')
  fig.canvas.mpl_connect('key_press_event',key);plt.show()
 plt.close(fig)

PORTRAIT_FILES=['pennywise.jpg','reference-2.jpg','reference-4.jpg','reference-5.jpg','reference-6.jpg','reference-3.jpg','pumpkin.png']
def add_portraits(ax,indices,args):
 """Existing image thumbnails, tethered to dots; dot coordinates are untouched."""
 if not args.portraits:return lambda positions:None
 from matplotlib.offsetbox import OffsetImage,AnnotationBbox
 from PIL import Image
 artists=[]
 offsets=[(-22,27),(22,-29),(29,22),(-29,-22),(0,39),(36,0),(-36,0)]
 for i in indices:
  im=Image.open(ROOT/'assets/portraits'/PORTRAIT_FILES[i]).convert('RGB');im.thumbnail((25,30))
  artist=AnnotationBbox(OffsetImage(np.asarray(im),zoom=1),(50,50),xybox=offsets[i],xycoords='data',boxcoords='offset points',frameon=True,pad=.12,bboxprops={'edgecolor':COLORS[i],'linewidth':.8,'facecolor':'white'},arrowprops={'arrowstyle':'-','color':COLORS[i],'lw':.6},zorder=12,annotation_clip=False)
  ax.add_artist(artist);artists.append(artist)
 def move(positions):
  for artist,pos in zip(artists,positions):artist.xy=tuple(pos)
 return move

def routing_animation(routes,name,args,title=None,xy=XY):
 fig,ax=plt.subplots(figsize=(9,7));fig.subplots_adjust(right=.73,bottom=.14);graph(ax,title or name,xy=xy);route_lines(ax,routes,xy=xy);legend(ax,range(min(7,len(routes))))
 dots=[ax.plot([],[],marker='o',color=COLORS[i%7],ms=7,zorder=9)[0] for i in range(len(routes))]
 traces=[ax.plot([],[],color=COLORS[i%7],lw=3,zorder=3)[0] for i in range(len(routes))]
 labels=[fig.text(.75,.67-i*.065,'',fontsize=8,color=COLORS[i%7]) for i in range(len(routes))]
 fig.text(.12,.035,'Fixed instance. Candy collection is an analogy for delivery CVRP.\nNo neural policy is executed.',fontsize=9)
 move_portraits=add_portraits(ax,range(min(7,len(routes))),args)
 maxcost=max(map(cost,routes))
 def update(p):
  positions=[]
  for i,r in enumerate(routes):
   pos,dist,q,a,b=state(r,p*maxcost);dots[i].set_data([pos[0]],[pos[1]]);positions.append(pos)
   idx=next((j for j in range(1,len(r)) if sum(DIST[r[k-1],r[k]] for k in range(1,j+1))>dist),len(r)-1)
   line=np.vstack([xy[r[:idx]],pos]);traces[i].set_data(line[:,0],line[:,1]);labels[i].set_text(f'{NAMES[i]}\n{a} → {b} | {dist:.1f} units | {q}/{Q}')
  move_portraits(positions)
 update(.35 if args.portraits else 0);save(fig,name,args);animate(fig,update,name,args)
