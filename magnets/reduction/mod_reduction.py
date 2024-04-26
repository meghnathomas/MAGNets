import wntr
from magnets.reduction import build_g_matrix
from magnets.reduction import reinitialize
from magnets.utils.characteristics import *
from magnets.utils.call_on_functions import *
import warnings

def mod_reduction(wn, new_link_list, junc_dict, pipe_dict, unremovable_nodes, relations, nodes_to_be_removed, new_pipe_len, alpha, inp_file, max_nodal_degree, op_pt, save_filename):
    
    if max_nodal_degree == None: 
        max_nodal_degree = 100
        
    if (max_nodal_degree < 1 or (isinstance(max_nodal_degree, int) == False and max_nodal_degree != None)):
        warnings.warn('Invalid maximum nodal degree provided by user. \ Running simulation with maximum nodal degree = 100.')
        max_nodal_degree = 100
        
    count = 1
    
    while (len(nodes_to_be_removed)!=0):
               
        junc_names = wn.junction_name_list
        num_junc = len(junc_names)
        pipe_names = wn.pipe_name_list
        num_pipes = len(pipe_names)
                
        #identify node with minimum number of connections
        num_connections = []
        
        for i in range(len(nodes_to_be_removed)):
            num_connections.append(len(junc_dict[nodes_to_be_removed[i]]['Connected nodes']))
            
        removal_node = nodes_to_be_removed[num_connections.index(min(num_connections))]
        
        if min(num_connections) > max_nodal_degree:
            break
        
        neighbor_nodes = junc_dict[removal_node]['Connected nodes']
                
        if len(neighbor_nodes)==1:
            
            nb_node = neighbor_nodes[0]
            for j in range(num_pipes):
                if (pipe_dict[pipe_names[j]]['Start node name'] == nb_node and pipe_dict[pipe_names[j]]['End node name'] == removal_node) or (pipe_dict[pipe_names[j]]['Start node name'] == removal_node and pipe_dict[pipe_names[j]]['End node name'] == nb_node):
                    nb_link = pipe_names[j]
            
            #update diagonal g~
            junc_dict[nb_node]['Diagonal g'] = junc_dict[nb_node]['Diagonal g'] - junc_dict[removal_node]['Diagonal g']
            
            #update demand
            junc_dict[nb_node]['Demand'] = junc_dict[nb_node]['Demand'] + junc_dict[removal_node]['Demand']
            wn.get_node(nb_node).demand_timeseries_list[0].base_value = wn.get_node(nb_node).demand_timeseries_list[0].base_value + wn.get_node(removal_node).demand_timeseries_list[0].base_value
            if wn.get_node(nb_node).demand_timeseries_list[0].pattern_name == '':
                            if wn.get_node(removal_node).demand_timeseries_list[0].pattern_name != '':
                                wn.get_node(nb_node).demand_timeseries_list[0]._pattern = wn.get_pattern(wn.get_node(removal_node).demand_timeseries_list[0].pattern_name)

            #delete link and node and update dictionaries
            wn.remove_link(nb_link)
            wn.remove_node(removal_node)
            
            nodes_to_be_removed.remove(removal_node)
            del relations[removal_node]
            del junc_dict[removal_node]
            del pipe_dict[nb_link]
            
            junc_names = wn.junction_name_list
            num_junc = len(junc_names)
            
            for value in relations.values():
                if removal_node in value:
                    value.remove(removal_node)
            for k in range(num_junc):
                if removal_node in junc_dict[junc_names[k]]['Connected nodes']:
                    junc_dict[junc_names[k]]['Connected nodes'].remove(removal_node)
            
        else:
            
            removal_links = []
            pipe_names = wn.pipe_name_list
            
            for d in range(len(neighbor_nodes)):
                node_x = neighbor_nodes[d]
                for e in range(len(pipe_names)):
                    if (pipe_dict[pipe_names[e]]['Start node name'] == node_x and pipe_dict[pipe_names[e]]['End node name'] == removal_node) or (pipe_dict[pipe_names[e]]['Start node name'] == removal_node and pipe_dict[pipe_names[e]]['End node name'] == node_x):
                        link_x = pipe_names[e]
                        
                        #update demand
                        junc_dict[node_x]['Demand'] = junc_dict[node_x]['Demand'] + abs(pipe_dict[link_x]['Linear g']*junc_dict[removal_node]['Demand']/junc_dict[removal_node]['Diagonal g'])
                        wn.get_node(node_x).demand_timeseries_list[0].base_value = wn.get_node(node_x).demand_timeseries_list[0].base_value + abs(pipe_dict[link_x]['Linear g']*wn.get_node(removal_node).demand_timeseries_list[0].base_value/junc_dict[removal_node]['Diagonal g'])
                        if wn.get_node(node_x).demand_timeseries_list[0].pattern_name == '':
                            if wn.get_node(removal_node).demand_timeseries_list[0].pattern_name != '':
                                wn.get_node(node_x).demand_timeseries_list[0]._pattern = wn.get_pattern(wn.get_node(removal_node).demand_timeseries_list[0].pattern_name)

                        #update diagonal g
                        junc_dict[node_x]['Diagonal g'] = junc_dict[node_x]['Diagonal g'] - abs((pipe_dict[link_x]['Linear g']**2)/junc_dict[removal_node]['Diagonal g'])
                        
                        removal_links.append(link_x)
            
            nb_pairs = [(neighbor_nodes[a],neighbor_nodes[b]) for a in range(len(neighbor_nodes)) for b in range(a+1, len(neighbor_nodes))]
            
            
            for node1, node2 in nb_pairs:
            
                link_1_2 = -1
                pipe_names = wn.pipe_name_list
                
                
                for l in range(len(pipe_names)):
                    
                    if (pipe_dict[pipe_names[l]]['Start node name'] == node1 and pipe_dict[pipe_names[l]]['End node name'] == node2) or (pipe_dict[pipe_names[l]]['Start node name'] == node2 and pipe_dict[pipe_names[l]]['End node name'] == node1):
                        link_1_2 = pipe_names[l]
                        
                    if (pipe_dict[pipe_names[l]]['Start node name'] == node1 and pipe_dict[pipe_names[l]]['End node name'] == removal_node) or (pipe_dict[pipe_names[l]]['Start node name'] == removal_node and pipe_dict[pipe_names[l]]['End node name'] == node1):
                        link_1_rem = pipe_names[l]
                        
                    if (pipe_dict[pipe_names[l]]['Start node name'] == node2 and pipe_dict[pipe_names[l]]['End node name'] == removal_node) or (pipe_dict[pipe_names[l]]['Start node name'] == removal_node and pipe_dict[pipe_names[l]]['End node name'] == node2):
                        link_2_rem = pipe_names[l]
                                                       
                #update non-diagonal g
                #Existing link between nodes 1 and 2
                if link_1_2 != -1:
                    pipe_dict[link_1_2]['Linear g'] = pipe_dict[link_1_2]['Linear g'] - abs(pipe_dict[link_1_rem]['Linear g']*pipe_dict[link_2_rem]['Linear g']/junc_dict[removal_node]['Diagonal g'])
                    pipe_dict[link_1_2]['Diameter'] = calculate_new_D(lin_g_to_nonlin_g(pipe_dict[link_1_2]['Linear g'],junc_dict[node1]['Head at op pt'], junc_dict[node2]['Head at op pt']),pipe_dict[link_1_2]['Length'],alpha,100)
                    pipe = wn.get_link(link_1_2)
                    pipe.diameter = pipe_dict[link_1_2]['Diameter']
                    pipe.roughness = 100
                    
                #No previously existing link between nodes 1 and 2
                else:
                    new_g = - abs(pipe_dict[link_1_rem]['Linear g']*pipe_dict[link_2_rem]['Linear g']/junc_dict[removal_node]['Diagonal g'])
                                        
                    wn.add_pipe('new-pipe-{}'.format(count), start_node_name = node1, end_node_name = node2, length = new_pipe_len, diameter = calculate_new_D(lin_g_to_nonlin_g(new_g,junc_dict[node1]['Head at op pt'], junc_dict[node2]['Head at op pt']), new_pipe_len, alpha, 100), roughness = 100, minor_loss = 0)
                    pipe_dict['new-pipe-{}'.format(count)] = {'Start node name': node1, 'End node name': node2, 'Length': new_pipe_len, 'Diameter':calculate_new_D(lin_g_to_nonlin_g(new_g,junc_dict[node1]['Head at op pt'], junc_dict[node2]['Head at op pt']), new_pipe_len, alpha, 100), 'Roughness':100, 'Linear g': new_g}
                    junc_dict[node1]['Connected nodes'].append(node2)
                    junc_dict[node2]['Connected nodes'].append(node1)
                    relations[node1].append(node2)
                    relations[node2].append(node1)
                    
                    count = count + 1

            for m in range(len(removal_links)):
                wn.remove_link(removal_links[m])
                del pipe_dict[removal_links[m]]                                  

            wn.remove_node(removal_node)
            
            nodes_to_be_removed.remove(removal_node)
            del relations[removal_node]
            del junc_dict[removal_node]
            
            junc_names = wn.junction_name_list
            num_junc = len(junc_names)
            
            for value in relations.values():
                if removal_node in value:
                    value.remove(removal_node)
            for k in range(num_junc):
                if removal_node in junc_dict[junc_names[k]]['Connected nodes']:
                    junc_dict[junc_names[k]]['Connected nodes'].remove(removal_node)
    
    if save_filename == None:
        if '/' in inp_file:
            index = inp_file.rindex('/') + 1
            new_name = inp_file[:index] + 'reduced ' + str(op_pt) + ' ' + inp_file[index:] 
            writeinpfile(wn, new_name)
            
        else:
            writeinpfile(wn, 'reduced {} {}'.format(op_pt, inp_file))
    else:
        writeinpfile(wn, save_filename + '.inp')
                    
    return 1
