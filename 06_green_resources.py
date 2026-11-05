"""Replay the saved resource-feasible routes with real travel, service and refill stops."""
from common import *
G=DATA['green'];GX=np.array([[n['x'],n['y']] for n in G['nodes']]);GD=np.ceil(np.linalg.norm(GX[:,None]-GX[None,:],axis=2)*10);B,T,V=G['B'],G['T'],G['speed'];S,R=G['service'],G['refuel'];GDEMAND=np.r_[DEMAND,np.zeros(8,dtype=int)]
def gcost(r):return sum(GD[i,j] for i,j in zip(r,r[1:]))
def duration(r):return gcost(r)/V+sum(1 for i in r if 0<i<=30)*S+sum(1 for i in r[1:-1] if i==0 or i>30)*R

def green_state(r,t):
 fuel=B;elapsed=0.;distance=0.;q=0
 for k,(i,j) in enumerate(zip(r,r[1:]),1):
  length=GD[i,j];travel=length/V
  if t<elapsed+travel:
   f=(t-elapsed)/travel
   return GX[i]+f*(GX[j]-GX[i]),fuel-f*length,distance+f*length,q,'travelling',i,j
  fuel-=length;distance+=length;elapsed+=travel
  if 0<j<=30:q+=int(DEMAND[j])
  stop=R if j==0 or j>30 else S
  if k==len(r)-1:stop=0
  if t<elapsed+stop:return GX[j],fuel,distance,q,'refuelling' if j==0 or j>30 else 'service',i,j
  elapsed+=stop
  if j==0 or j>30:fuel=B
 return GX[0],fuel,distance,q,'finished',r[-2],0
if __name__=='__main__':
 a=options(__doc__);rs=G['routes'];fig,(ax,bars)=plt.subplots(1,2,figsize=(11,7),gridspec_kw={'width_ratios':[3,1]});fig.subplots_adjust(bottom=.23,wspace=.45);graph(ax,'Green VRP: fuel and station stops',xy=GX);route_lines(ax,rs,xy=GX)
 ax.scatter(GX[31:,0],GX[31:,1],marker='^',s=75,color='black',zorder=8)
 for i in range(31,39):ax.annotate(f'S{i-30}',GX[i],xytext=(5,-12),textcoords='offset points',fontsize=8)
 bars.set(xlim=(0,B),ylim=(-.5,6.5),xlabel='Fuel remaining',title='Fuel capacity $B=650$');bars.set_yticks(range(7),NAMES,fontsize=8);bars.invert_yaxis();rects=bars.barh(range(7),[B]*7,color=COLORS)
 dots=[ax.plot([],[],marker='o',ms=7,c=COLORS[i],zorder=9)[0] for i in range(7)];status=fig.text(.08,.015,'',fontsize=8);maxt=max(map(duration,rs))
 move_portraits=add_portraits(ax,range(7),a)
 def update(p):
  states=[green_state(r,p*maxt) for r in rs]
  for dot,bar,s in zip(dots,rects,states):dot.set_data([s[0][0]],[s[0][1]]);bar.set_width(s[1])
  move_portraits([s[0] for s in states])
  status.set_text(f'Time: {p*maxt*60:.2f} min | limit {T*60:.0f} min | 1 fuel unit/metre | full refill at D or stations\n'+'\n'.join('; '.join(f'{NAMES[i]}: {s[4]}, {s[2]:.0f} m' for i,s in list(enumerate(states))[k:k+3]) for k in range(0,7,3))+'\nSaved station insertions; resource states calculated in Python. Time checked after construction, not during search. No CO₂ model.')
 update(.3);save(fig,'06-green-resources',a);animate(fig,update,'06-green-resources',a)
