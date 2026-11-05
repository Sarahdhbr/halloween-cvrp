"""Display the unchanged instance and its definitions."""
from common import *
if __name__=='__main__':
 a=options(__doc__);fig,ax=plt.subplots(figsize=(10,8));fig.subplots_adjust(right=.74,bottom=.13);graph(ax,'Fixed CVRP instance: 30 customers and one depot',demands=True)
 # Only a nearby-edge subset is drawn. The optimisation graph remains complete.
 for i in range(31):
  for j in np.argsort(DIST[i])[1:4]:
   if i<j:ax.plot(XY[[i,j],0],XY[[i,j],1],color='.82',lw=.7,zorder=1)
 fig.text(.76,.77,'D: depot (50, 50)\n'+r'$d_i$: customer demand'+'\n'+r'$Q=18$: route capacity'+'\n'+r'$K=7$: available collectors'+'\nTotal demand: 84\n\nScenario: 7 active routes.\nSeparate MILP: at most 7.\n\n'+r'$c_{ij}=\|x_i-x_j\|_2$'+'\nUnrounded Euclidean costs.\nComplete symmetric graph.\nSome edges hidden only\nfor readability.',fontsize=10,va='top')
 fig.text(.12,.045,'Candy collection is an analogy for the delivery CVRP.\nEach customer is visited once; every route returns to D and has total demand at most Q.',fontsize=10)
 save(fig,'01-instance',a)
 if a.show:plt.show()
