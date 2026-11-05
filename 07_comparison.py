"""Compare unchanged heuristic results and the two saved full-graph MILP results."""
from common import *
if __name__=='__main__':
 a=options(__doc__);exact=align(DATA['final'],EXACT['routes']);variants=[('Initial $S_0$ = Clarke–Wright',DATA['initial']['routes']),('Our method: restricted pool DP',DATA['final']),('Full MILP: exactly 7 — Proven optimal',exact),('Full MILP: at most 7 — Not proven optimal',ATMOST['routes'])]
 fig,axs=plt.subplots(2,2,figsize=(11,10));fig.subplots_adjust(hspace=.3,wspace=.3,bottom=.1)
 for ax,(name,rs) in zip(axs.flat,variants):graph(ax,name+f'\nCost {total(rs):.6f}; {len(rs)} routes; feasible');route_lines(ax,rs)
 fig.text(.08,.025,'Same coordinates, demands, Q=18 and seven available vehicles. Exactly-seven policy keeps all collectors active.\nAt-most-seven result uses five routes; route-to-collector assignment is arbitrary. No change to either optimisation problem.',fontsize=9);save(fig,'07-same-graph-comparison',a)
 if a.show:plt.show()
 plt.close(fig)
 timing=json.loads((ROOT/'data/heuristic-timings.json').read_text());rows=[['Initial $S_0$',f'{total(DATA["initial"]["routes"]):.6f}','7','Feasible',f'{timing["cwSeconds"]:.6f}','Heuristic'],['Clarke–Wright',f'{total(DATA["initial"]["routes"]):.6f}','7','Feasible',f'{timing["cwSeconds"]:.6f}','Same solution as $S_0$'],['Our method',f'{total(DATA["final"]):.6f}','7','Feasible',f'{timing["totalMethodSeconds"]:.6f}','Restricted pool only'],['MILP: exactly 7',f'{EXACT["cost"]:.6f}','7','Feasible',f'{EXACT["totalSeconds"]:.6f}','Proven optimal'],['MILP: at most 7',f'{ATMOST["cost"]:.6f}','5','Feasible',f'{ATMOST["totalSeconds"]:.6f}','Time limit; not proven']]
 fig,ax=plt.subplots(figsize=(12,5));ax.axis('off');ax.set_title('Recorded results on the unchanged instance',pad=20);table=ax.table(cellText=rows,colLabels=['Method','Cost','Routes','Feasibility','Time (s)','Status'],loc='center',cellLoc='left',colWidths=[.20,.14,.07,.12,.13,.34]);table.auto_set_font_size(False);table.set_fontsize(9);table.scale(1,2.2)
 fig.text(.05,.06,f'Exactly 7: bound {EXACT["bestBound"]:.9f}; gap ≈ 0. At most 7: bound {ATMOST["bestBound"]:.6f}; gap {100*ATMOST["gap"]:.4f}%.\nHiGHS 1.8.0 / SciPy 1.16.3. Saved solve times; no new MILP solve. Heuristic and MILP timing scopes differ.\nExact pool selection is not a global optimality certificate.',fontsize=10);save(fig,'07-results-table',a)
 if a.show:plt.show()
 plt.close(fig)
 routing_animation(exact,'07-exact-seven',a,'Full-graph MILP: exactly 7 — Proven optimal, cost 650.968917')
 routing_animation(ATMOST['routes'],'07-at-most-seven',a,'Full-graph MILP: at most 7 — Time limit, cost 638.816967')
