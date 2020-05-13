import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# ------- DIRECTED

# Build a dataframe with your connections
# This time a pair can appear 2 times, in one side or in the other!
df = pd.DataFrame({ 'from':[1,1,3,2,], 'to':[2,3,4,4]})
df

# Build your graph. Note that we use the DiGraph function to create the graph!
G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

# Make the graph
nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)
plt.show()


task_bucket = {}
task_list = []
priority_map = {}
INF = 1e9 + 7
def input_edge(to_node, from_node, edge_id):
    if edge_id not in adj:
        task_bucket[edge_id] = []

    if edge_id not in task_list:
        task_list.append(edge_id)

    # creating edge
    task_bucket[edge_id].append((to_node, from_node))
    return


def dfs(node, adj, dep):
    pri = INF
    if node in priority_map:
        return priority_map[node][0]
    for i in adj[node]:
        pri = min(pri, dfs(i, adj, dep + 1))
    if pri == INF:
        pri = 0
    priority_map[node] = (pri, dep)
    return pri
    
def generate_topology_for_id(id):
    adj = {}
    indeg = {}
    priority_map.clear()

    for pair in task_bucket[id]:
        u = pair[0]
        v = pair[1]
        if u not in adj:
            adj[u] = []
        if v not in indeg:
            indeg[v] = 0
        if u not in indeg:
            indeg[u] = 0
        adj[u].append(v)
        indeg[v] += 1

    for node, degree in indeg.items():
        if degree == 0:
            dep = 0
            dfs(node, adj, dep)



def generate_graph():
    for id in task_list:
        generate_topology_for_id(id)






'''
                 SIM1
    @vikram --------------->  @pawan
                SIM1
    @pawan -----------------> @rahul

                SIM2
    @vikram --------------->  @pawan


SIM1
@vikram -> @pawan -> @rahul

SIM2
  @vikram -> @pawan

-----------------------
Tops fail
12
13


      1
     / \
     2  3




id: Table x create
1 -> 2
1 -> 3


------------------------

12
13


      1
     / \
     2  3
      \ /
        4


id: Table x create
1 -> 2
1 -> 3
2 -> 4
3 -> 4
--------------------------


1(backend)    2(interface)
 \            /
         4
         (fronend)

show two graphs
1->4
2->4

multiple graphs can be there hence creates confusion

soln is add priority
    - same level has same priority




'''
