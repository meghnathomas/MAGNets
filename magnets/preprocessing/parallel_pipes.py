import wntr
import collections
import numpy as np
from magnets.utils.call_on_functions import *

def parallel_pipes(relations, wn, new_link_list, junc_dict, pipe_dict, unremovable_nodes, special_nodes, special_links_nodes, special_links, alpha):
    connected_nodes = []
    num_connections = []
    num_junc = wn.num_junctions
    junc_names = wn.junction_name_list
    link_names = wn.link_name_list
    parallel_pipes_list = []
    
    for i in range(num_junc):
        connected_nodes.append([])
        for a,b in new_link_list:
            if (a == junc_names[i]):
                connected_nodes[i].append(b)
            if (b == junc_names[i]):
                connected_nodes[i].append(a)     
    
    for i in range(len(connected_nodes)):
        has_dup = ([item for item, count in collections.Counter(connected_nodes[i]).items() if count > 1])
        if len(has_dup)!= 0:
            # if junc_names[i] not in unremovable_nodes:
            if junc_names[i] not in special_nodes:
                for j in range(len(has_dup)):
                    # if has_dup[j] not in unremovable_nodes:
                    if has_dup[j] not in special_nodes:
                        if ((junc_names[i],has_dup[j]) not in parallel_pipes_list and (has_dup[j],junc_names[i]) not in parallel_pipes_list):
                            if ((junc_names[i],has_dup[j]) not in special_links_nodes and (has_dup[j],junc_names[i]) not in special_links_nodes):
                                parallel_pipes_list.append((junc_names[i],has_dup[j]))
                    
    parallel_links = []
    
    for j in range(len(parallel_pipes_list)):
        parallel_links.append([])
        a = parallel_pipes_list[j][0]
        b = parallel_pipes_list[j][1]
        
        for i in range(len(new_link_list)):
            if (new_link_list[i][0] == a and new_link_list[i][1] == b) or (new_link_list[i][1] == a and new_link_list[i][0] == b):
                if link_names[i] not in parallel_links and link_names[i] not in special_links:
                    parallel_links[j].append(link_names[i])
                    
        junc_dict[a]['Connected nodes'] = list(np.unique(np.array((junc_dict[a]['Connected nodes']))))
        junc_dict[b]['Connected nodes'] = list(np.unique(np.array((junc_dict[b]['Connected nodes']))))
        relations[a] = list(np.unique(np.array((relations[a]))))
        relations[b] = list(np.unique(np.array((relations[b]))))
    
    
    for k in range(len(parallel_links)):
        leng = []
        ks = []
        
        for l in range(len(parallel_links[k])):
            pipe = wn.get_link(parallel_links[k][l])
            leng.append(pipe.length)
            ks.append(calc_K(pipe.length, pipe.diameter,pipe.roughness, alpha))
        
        new_l = min(leng)
        K_sum = 0
        
        for m in range(len(ks)):
            K_sum = K_sum + (1/ks[m])**(1/1.852)
            
        new_K = 1/(K_sum**1.852)
        new_d = (alpha*new_l/((100**1.852)*(new_K)))**(1/4.87)
        
        for n in range(len(parallel_links[k])):
            wn.remove_link(parallel_links[k][n], force=True)
            del pipe_dict[parallel_links[k][n]]
            
        wn.add_pipe('{}'.format(parallel_links[k][0]), start_node_name=parallel_pipes_list[k][0], end_node_name=parallel_pipes_list[k][1],length=new_l, diameter = new_d, roughness=100, minor_loss=0)
        pipe_dict[parallel_links[k][0]] = {'Start node name': parallel_pipes_list[k][0], 'End node name':parallel_pipes_list[k][1], 'Length': new_l, 'Diameter':new_d, 'Roughness':100}
        new_link_list.append((parallel_pipes_list[k][0],parallel_pipes_list[k][1]))
        
    return wn, junc_dict, pipe_dict, relations, new_link_list
