"""Execute the original savings rule; replay merges and continuously animate routes."""
from common import *
if __name__=='__main__':
 a=options(__doc__);routes,merges,decisions=cw();assert routes==DATA['initial']['routes'];assert all(check(routes,exact_fleet=True).values())
 (a.out/'02-cw-calculation.json').parent.mkdir(parents=True,exist_ok=True);(a.out/'02-cw-calculation.json').write_text(json.dumps({'cost':total(routes),'merges':merges,'decisions':decisions},indent=2))
 fig,ax=plt.subplots(figsize=(8,7));fig.subplots_adjust(bottom=.17)
 def update(p):
  ax.clear();step=min(len(merges),int(p*(len(merges)+1)));rs=merges[step-1]['routes'] if step else [[0,i,0] for i in range(1,31)];graph(ax,f'Clarke–Wright: {step}/23 accepted merges');route_lines(ax,rs,colors=[COLORS[next(i for i,rr in enumerate(routes) if set(r[1:-1])<=set(rr[1:-1]))] for r in rs])
  if step:
   e=merges[step-1];ax.plot(XY[[e['i'],e['j']],0],XY[[e['i'],e['j']],1],color='black',lw=3);caption=f"Merge {e['i']}–{e['j']}; saving = {e['saving']:.4f}"
  else:caption='30 individual trips: exceeds the seven-vehicle fleet'
  footer.set_text(caption+f'\n{len(rs)} routes | cost {total(rs):.6f} | stop at exactly seven routes')
 footer=fig.text(.12,.045,'',fontsize=10);update(1);save(fig,'02-cw-merges',a);animate(fig,update,'02-cw-merges',a)
 routing_animation(routes,'02-cw-routes',a,'Clarke–Wright = initial solution $S_0$; cost 673.042401')
