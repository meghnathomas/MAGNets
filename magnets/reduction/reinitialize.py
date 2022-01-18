import wntr
from magnets.utils.call_on_functions import *
from magnets.utils.characteristics import *

def reinitialize(wn, new_link_list, special_nodes, unremovable_nodes):
    junc_names = wn.junction_name_list
    
    link_1 = []
    link_2 = []
    
    for link_name, link in wn.links():
        link_1.append(link.start_node_name)
        link_2.append(link.end_node_name)
    link_list = tuple(zip(link_1,link_2))
    new_link_list = list(link_list)
    
    link_list_only_junc = []
    for a,b in new_link_list:
        if a not in special_nodes and b not in special_nodes:
            link_list_only_junc.append((a,b))
    
    for a,b in new_link_list:
        if (a in special_nodes and b not in special_nodes):
            if b not in unremovable_nodes:
                unremovable_nodes.append(b)
        if (b in special_nodes and a not in special_nodes):
            if a not in unremovable_nodes:
                unremovable_nodes.append(a)    
    
    nodes_to_be_removed = []
    for a in junc_names:
        if (a not in unremovable_nodes):
            nodes_to_be_removed.append(a)
    
    return nodes_to_be_removed, link_list_only_junc, unremovable_nodes
