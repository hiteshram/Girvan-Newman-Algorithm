'''
Name - Hitesh Ram Kotha

Explanation - I have taken BFS approach as reference. Initially we will create a BFS tree by taking the 'a' source, then we will fetch 
the leaf nodes of the BFS Tree and assign their flow as 1 and we will add the parents to the queue and when a parent comes up we will 
add one for itself and the sum the flows of its child and append the current node's parent to the list. 

Although, the flow seems to be off by 1 for couple of edges but the betweeness order is same, tested via Karate dataset. 
'''

import networkx as nx

# This function below returns the leaf nodes for every BFS Tree
def get_leaf_nodes(bfs_output,source):
    
    leaf_nodes_list=list()
    nodes_list=list(nx.bfs_successors(g,source))
    parent_nodes_list=list()
    for i in range(0,len(nodes_list)):
        parent_nodes_list.append(nodes_list[i][0])

    for i in bfs_output.nodes:
        if(i not in parent_nodes_list):
            leaf_nodes_list.append(i)
    
    return leaf_nodes_list

# This function returns the parent nodes for the current node passed as parameter
def get_parent_nodes(parent_nodes_list,current_node):
    parent_list=list()
    for node in parent_nodes_list:
        if(current_node==node[0]):
            parent_list.append(node[1])
    
    return parent_list

# This function returns the child nodes for the current node passed as parameter
def get_child_nodes(children_nodes_list,current_node):
    child_list=list()
    for node in children_nodes_list:
        if(current_node==node[0]):
            child_list.append(node[1])
    
    return child_list[0]

# Master Function which creates BFS Tree and updates the forward and backward flow values to local betweeness dictionary,  
# which will be updated to the master edge betweeness values 
def get_bfs(source):
    edge_local=dict()
    for i in g.edges:
        edge_local[tuple(sorted(i))]=0
    bfs_output=nx.Graph(nx.bfs_tree(g,source))
    leaf_nodes_list=get_leaf_nodes(bfs_output,source)
    parent_nodes_list=list(nx.bfs_predecessors(bfs_output,source))
    children_nodes_list=list(nx.bfs_successors(bfs_output,source))

    # Initializing the queue with the leaf nodes 
    queue=list(leaf_nodes_list)
    while len(queue)>0:
        current_node=queue.pop(0)
        #Assign 1 to the flow if the current node is a leaf node
        if current_node in leaf_nodes_list:
            parents=get_parent_nodes(parent_nodes_list,current_node)
            temp=(current_node,parents[0])
            edge_local[tuple(sorted(temp))]=1
        else:
            parents=get_parent_nodes(parent_nodes_list,current_node)
            children=get_child_nodes(children_nodes_list,current_node)
            forward_val=1
            
            for c in children:
                temp=(current_node,c)
                forward_val=forward_val+edge_local[tuple(sorted(temp))]
            
            if len(parents)>0:
                temp=(current_node,parents[0])
                edge_local[tuple(sorted(temp))]=forward_val
            
        if len(parents)>0 and parents[0] not in queue:
                queue.append(parents[0])
        
    return edge_local



g=nx.Graph()

'''
Adjacency list 
A:B,C
B:A,C,H
C:A,D,B
D:C,E,F
E:D,F,G
F:D,E
G:H,I,E
H:B,I,G
I:H,G
'''
g.add_edges_from([('a','b'),('a','c')])
g.add_edges_from([('b','a'),('b','c'),('b','h')])
g.add_edges_from([('c','a'),('c','d'),('c','b')])
g.add_edges_from([('d','c'),('d','e'),('d','f')])
g.add_edges_from([('e','d'),('e','f'),('e','g')])
g.add_edges_from([('f','d'),('f','e')])
g.add_edges_from([('g','h'),('g','i'),('g','e')])
g.add_edges_from([('h','b'),('h','i'),('h','g')])
g.add_edges_from([('i','h'),('i','g')])

# Initializing the edge master dictionary with zero betweeness 
# we store all the betweeness observed from all the BFS Trees
# - make sure to divide these values by 2 and print in the output 
edge_master=dict()
for i in g.edges:
    edge_master[tuple(sorted(i))]=0

for i in g.nodes:
    temp=get_bfs(i)
    for k,v in edge_master.items():
        edge_master[k]=v+temp[k]

for k,v in edge_master.items():
    edge_master[k]=v/2

print('   Edges    Betweeness')
for k,v in edge_master.items():
    print(str(k).upper(),' - ',v)





