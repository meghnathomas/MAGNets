import wntr


def branch_ends(relations, wn, new_link_list, junc_dict, pipe_dict, unremovable_nodes):

    num_connections = [len(node) for node in relations.values()]
    
    while min(num_connections) == 1:
        junc_names = wn.junction_name_list
        link_names = wn.link_name_list
        branch_ends = []
        node_indexes = []
        link_indexes = []
        receiving_nodes = []
        
        for i in range(len(num_connections)):
            if num_connections[i] == 1:
                if junc_names[i] not in unremovable_nodes:
                    branch_ends.append(junc_names[i])
                    node_indexes.append(i)
        
        if len(branch_ends) == 0:
            break
        
        for i in range(len(branch_ends)):
            branch_end_node = wn.get_node(branch_ends[i])
            receiving_node_name = relations.get(branch_ends[i])[0]
            receiving_node = wn.get_node(receiving_node_name)
            receiving_nodes.append(receiving_node_name)
                    
            receiving_node.demand_timeseries_list[0].base_value = receiving_node.demand_timeseries_list[0].base_value + branch_end_node.demand_timeseries_list[0].base_value
            junc_dict[receiving_node_name]['Demand'] = receiving_node.demand_timeseries_list[0].base_value
            
            #delete links and nodes and update G
            for j in range(len(new_link_list)):
                if (new_link_list[j][0] == branch_ends[i] and new_link_list[j][1] == receiving_node_name) or (new_link_list[j][1] == branch_ends[i] and new_link_list[j][0] == receiving_node_name):
                    link_indexes.append(j)
                    
        link_indexes.sort(reverse=True)       
        for k in range(len(link_indexes)):
            wn.remove_link(link_names[link_indexes[k]], force = True)       
            new_link_list.remove(new_link_list[link_indexes[k]])
            del pipe_dict[link_names[link_indexes[k]]]
            
        for l in range(len(branch_ends)):
            wn.remove_node(branch_ends[l], force=True)
            del relations[branch_ends[l]]
            del junc_dict[branch_ends[l]]
            for value in relations.values():
                if branch_ends[l] in value:
                    value.remove(branch_ends[l])
            for m in range(len(receiving_nodes)):
                if branch_ends[l] in junc_dict[receiving_nodes[m]]['Connected nodes']:
                    junc_dict[receiving_nodes[m]]['Connected nodes'].remove(branch_ends[l])
                    
    
        num_connections = [len(node) for node in relations.values()]
        
    return wn, junc_dict, pipe_dict, relations, new_link_list