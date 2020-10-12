# Used the edge betweeness function implemented in the Question 1 and calculated the betweeness and removed the edges with maximum betweeness 
# till we get two distinct communities.


import networkx as nx

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

def get_parent_nodes(parent_nodes_list,current_node):
    parent_list=list()
    for node in parent_nodes_list:
        if(current_node==node[0]):
            parent_list.append(node[1])
    
    return parent_list

def get_child_nodes(children_nodes_list,current_node):
    child_list=list()
    for node in children_nodes_list:
        if(current_node==node[0]):
            child_list.append(node[1])
    
    return child_list[0]

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
        if current_node in leaf_nodes_list:
            parents=get_parent_nodes(parent_nodes_list,current_node)
            #leaf nodes will have only one parent 
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





# Initializing the edge master dictionary with zero betweeness 
# we store all the betweeness observed from all the BFS Trees
# - make sure to divide these values by 2 and print in the output 

g=nx.read_gml('karate.gml')

sg=nx.connected_components(g)
sg_count=nx.number_connected_components(g)

while sg_count==1:

    edge_master=dict()
    for i in g.edges:
        edge_master[tuple(sorted(i))]=0

    for i in g.nodes:
        temp=get_bfs(i)
        for k,v in edge_master.items():
            edge_master[k]=v+temp[k]

    for k,v in edge_master.items():
        edge_master[k]=v/2


    for k,v in sorted(edge_master.items(), key=lambda item: item[1], reverse = True):
        edge=k
        break

    g.remove_edge(edge[0],edge[1])
    sg=nx.connected_components(g)
    sg_count=nx.number_connected_components(g)

sg=list(nx.connected_components(g))

print("Community 1 - ",['n'+x for x in list(sg[0])])
print("Community 2 - ",['n'+x for x in list(sg[1])])
