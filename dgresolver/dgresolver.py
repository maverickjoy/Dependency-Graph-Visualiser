import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable

# --------------------------
task_bucket = {}
task_list = []
priority_map = {}
components = {}
INF = 1e9 + 7
# --------------------------


def input_edge(to_node, from_node, edge_id):
    if edge_id not in task_bucket:
        task_bucket[edge_id] = []

    if edge_id not in task_list:
        task_list.append(edge_id)

    # creating edge
    task_bucket[edge_id].append((to_node, from_node))
    return


def print_graph(edges):
    from_nodes = []
    to_nodes = []
    for edge in edges:
        from_nodes.append(edge[0])
        to_nodes.append(edge[1])

    df = pd.DataFrame({ 'from': from_nodes, 'to':to_nodes})
    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

    nx.draw(G, with_labels=True, node_size=1500, alpha=0.3, arrows=True)
    plt.show()
    return

def print_priority_map():
    table = PrettyTable(['Name', 'Priority', '# of dependencies'])
    for node, row in priority_map.items():
        table.add_row([node, row[0], row[1]])
    print(table)
    return

def dfs1(node, un_adj, comp_id):
    components[node] = comp_id
    if node in un_adj:
        for i in un_adj[node]:
            if i not in components:
                dfs1(i, un_adj, comp_id)
    return


def dfs2(node, adj):
    pri = INF
    if node in priority_map:
        return priority_map[node][0] + 1

    if node in adj:
        for i in adj[node]:
            pri = min(pri, dfs2(i, adj))

    if pri == INF:
        pri = 1
    priority_map[node] = [pri, -1]
    return pri + 1

def dfs3(node, adj, dep):
    addDep = 0
    if priority_map[node][1] == -1:
        priority_map[node][1] = 0
        addDep = 1
    priority_map[node][1] += dep

    if node in adj:
        for i in adj[node]:
            dfs3(i, adj, dep + addDep)
    return

def generate_topology_for_id(id):
    adj = {}
    un_adj = {}
    indeg = {}
    priority_map.clear()
    components.clear()

    for pair in task_bucket[id]:
        u = pair[0]
        v = pair[1]
        if u not in adj:
            adj[u] = []
        if v not in indeg:
            indeg[v] = 0
        if u not in indeg:
            indeg[u] = 0
        if u not in un_adj:
            un_adj[u] = []
        if v not in un_adj:
            un_adj[v] = []

        adj[u].append(v)
        un_adj[u].append(v)
        un_adj[v].append(u)
        indeg[v] += 1

    comp_id = 0
    for node in indeg:
        if node not in components:
            comp_id += 1
            dfs1(node, un_adj, comp_id)

    for node, degree in indeg.items():
        if degree == 0:
            dfs2(node, adj)

    for node, degree in indeg.items():
        if degree == 0:
            dfs3(node, adj, 0)

    comp_to_edge = {}
    for pair in task_bucket[id]:
        u = pair[0]
        v = pair[1]
        if components[u] not in comp_to_edge:
            comp_to_edge[components[u]] = []
        comp_to_edge[components[u]].append((u, v))

    print_priority_map()

    for id, edges in comp_to_edge.items():
        print_graph(edges)

    return


def generate_graph():
    for id in task_list:
        generate_topology_for_id(id)


if __name__ == "__main__":
    n = int(input())
    for i in range(n):
        to_node, from_node, edge_id = input().split()
        input_edge(to_node, from_node, edge_id)

    generate_graph()




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

-----------------------

- same indegree same component/ different component


'''
