"""Conceptual multiple starts and square symmetries; no learned POMO policy."""
from common import *
if __name__=='__main__':
 a=options(__doc__);u=XY/100;x,y=u[:,0],u[:,1];transforms=[(x,y),(1-x,y),(x,1-y),(1-x,1-y),(y,x),(1-y,x),(y,1-x),(1-y,1-x)];names=['$(x,y)$','$(1-x,y)$','$(x,1-y)$','$(1-x,1-y)$','$(y,x)$','$(1-y,x)$','$(y,1-x)$','$(1-y,1-x)$']
 fig,axs=plt.subplots(2,4,figsize=(13,7));fig.subplots_adjust(bottom=.15,wspace=.35,hspace=.35)
 for ax,(xx,yy),name in zip(axs.flat,transforms,names):graph(ax,name,xy=100*np.c_[xx,yy]);ax.set_xlabel('');ax.set_ylabel('')
 fig.text(.08,.04,'Eight geometric augmentations of the same instance: distances and demands are preserved.\nThese are coordinate transformations, separate from multiple starts. No network or full rollout is executed.',fontsize=11);save(fig,'05-eight-symmetries',a)
 if a.show:plt.show()
 plt.close(fig)
 starts=[1+(4*j)%30 for j in range(7)];rs=[[0,i] for i in starts];fig,ax=plt.subplots(figsize=(9,7));fig.subplots_adjust(right=.73,bottom=.15);graph(ax,'POMO concept: seven alternative first customers');route_lines(ax,rs);legend(ax)
 dots=[ax.plot([],[],marker='o',ms=7,c=COLORS[i],zorder=9)[0] for i in range(7)]
 move_portraits=add_portraits(ax,range(7),a)
 def update(p):
  for dot,i in zip(dots,starts):pos=(1-p)*XY[0]+p*XY[i];dot.set_data([pos[0]],[pos[1]])
  move_portraits([(1-p)*XY[0]+p*XY[i] for i in starts])
 fig.text(.12,.04,'Teaching illustration: imposed first customers 1, 5, 9, 13, 17, 21, 25.\nAlternative starts, not a single feasible fleet solution. No sampled/greedy neural rollout or probabilities.',fontsize=9)
 update(.5);save(fig,'05-multiple-starts',a);animate(fig,update,'05-multiple-starts',a)
