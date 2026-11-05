"""Calculate a local capacity/visited mask, without AM inference or probabilities."""
from common import *
if __name__=='__main__':
 a=options(__doc__);r=DATA['final'][5];maxcost=cost(r);fig,ax=plt.subplots(figsize=(10,7));fig.subplots_adjust(right=.72,bottom=.16);graph(ax,'Feasibility mask: computed constraints, no neural inference');route_lines(ax,[r],colors=[COLORS[5]])
 sc=ax.scatter(XY[1:,0],XY[1:,1],s=85,facecolors='none',edgecolors='green',lw=1.6,zorder=8);dot=ax.plot([],[],marker='o',color=COLORS[5],ms=8,zorder=9)[0];text=fig.text(.75,.78,'',va='top',fontsize=10)
 fig.text(.12,.04,'Green ring: allowed next customer. Red ring: visited or demand exceeds remaining capacity.\nDepot return is always allowed in this local illustration. No decoder scores or softmax are simulated.',fontsize=9)
 move_portraits=add_portraits(ax,[5],a)
 def update(p):
  pos,dist,q,fr,to=state(r,p*maxcost);visited=[]
  for customer in r[1:-1]:
   if customer==to and fr!=to:break
   visited.append(customer)
   if customer==fr:break
  if dist==0:visited=[]
  if p>=1:visited=r[1:-1]
  allowed=np.array([i not in visited and DEMAND[i]<=Q-q for i in range(1,31)]);sc.set_edgecolors(['#2b8a3e' if ok else '#c92a2a' for ok in allowed]);dot.set_data([pos[0]],[pos[1]])
  move_portraits([pos])
  text.set_text('Teaching illustration\nWednesday route replay\n\n'+f'Current arc: {fr} → {to}\nCollected: {q}\n'+r'$Q-q_t$'+f' = {Q-q}\nAllowed: {allowed.sum()} customers\n\nMask formula:\n'+r'$m_i=\mathbf{1}[i\notin V_t]$'+'\n'+r'$\quad\cdot\mathbf{1}[d_i\leq Q-q_t]$'+'\n\nOnly this route’s visits\nare tracked here.\nNot a full AM rollout.')
 update(.65);save(fig,'04-feasibility-mask',a);animate(fig,update,'04-feasibility-mask',a)
