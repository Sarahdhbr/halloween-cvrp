"""Saved candidate generation; recomputed exact pool partition and actual replacement."""
from common import *
if __name__=='__main__':
 a=options(__doc__);h=DATA['history'][1];assert select_subproblem(h['before'],2)==h['selected'];value,chosen=partition(h['ids'],h['pool'],len(h['selected']));assert list(chosen)==h['chosen'];assert abs(value-h['newCost'])<1e-7
 current=[r[:] for r in h['before']]
 for slot,p in zip(h['selected'],chosen):current[slot]=h['pool'][p]
 assert current==h['after']==DATA['final']
 fig,axs=plt.subplots(2,2,figsize=(11,10));fig.subplots_adjust(bottom=.20,hspace=.3,wspace=.3)
 graph(axs[0,0],'1. Select whole routes by centroid proximity');route_lines(axs[0,0],h['before'],alpha=.12)
 for slot in h['selected']:route_lines(axs[0,0],[h['before'][slot]],colors=[COLORS[slot]],alpha=1)
 centers=np.array([XY[r[1:-1]].mean(axis=0) for r in h['before']]);axs[0,0].scatter(centers[:,0],centers[:,1],marker='x',c=COLORS,s=45,zorder=8)
 graph(axs[0,1],'2. Candidate pool: 107 routes (saved generation)')
 # Representative route candidates only, separately from exact selected subset.
 for p in [0,1,2,3,4]:route_lines(axs[0,1],[h['pool'][p]],colors=[COLORS[h['selected'][p if p<4 else 2]]],alpha=.75)
 graph(axs[1,0],r'3. Exact pool partition: $\sum_{r\ni i}z_r=1$, $\sum_r z_r=4$')
 for slot,p in zip(h['selected'],chosen):route_lines(axs[1,0],[h['pool'][p]],colors=[COLORS[slot]],alpha=1)
 graph(axs[1,1],'4. Replace selected routes, retain other routes');route_lines(axs[1,1],current)
 fig.text(.08,.035,'Iteration 2: 12 customers, 4 selected routes; pool IDs 1, 2, 5, 4. Old local cost 254.825101 → 244.943065.\nThree original routes + one 2-opt route; only Wednesday’s order of customers 2 and 8 changes.\nCandidates: classical heuristics, not AM/POMO. Exact pool selection does not prove global CVRP optimality.',fontsize=10)
 fig.legend(handles=[Line2D([0],[0],color=COLORS[i],label=NAMES[i]) for i in range(7)],loc='lower center',bbox_to_anchor=(.5,.105),ncol=4,frameon=False,fontsize=8);save(fig,'03-subproblem',a)
 if a.show:plt.show()
 plt.close(fig)
 # Individual readable phases suitable for slides.
 for phase,(title,rs) in enumerate([('Selected subproblem routes',[h['before'][i] for i in h['selected']]),('Representative pool candidates',h['pool'][:5]),('Selected pool routes',[h['pool'][p] for p in chosen]),('Recombined full solution',current)],1):
  f,ax=plt.subplots(figsize=(8,7));graph(ax,title);route_lines(ax,rs,colors=[COLORS[i] for i in h['selected']] if phase in [1,3] else [COLORS[h['selected'][i if i<4 else 2]] for i in range(5)] if phase==2 else None);f.text(.12,.02,'Saved candidate generation; Python DP selection. No trained policy.',fontsize=9);save(f,f'03-phase-{phase}',a);plt.close(f)
 (a.out/'03-pool-selection.json').write_text(json.dumps({'iteration':2,'poolRouteIdsOneBased':[p+1 for p in chosen],'localCost':value,'globalCost':total(current),'routes':current},indent=2))
 routing_animation(current,'03-recombined-routes',a,'Recombined solution; cost 663.160365 (restricted pool DP)')
