import wntr
from wntr.network.elements import Pipe, Junction
import warnings


def characteristics(inp_file, op_pt = None, nodes_to_keep = None):
    
    wn = wntr.network.WaterNetworkModel(inp_file)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    
    report_time_step = wn.options.time.report_timestep
    
    horizon = int(wn.options.time.duration/report_time_step)
    time_steps = list(range(0,horizon+1))
    
    if op_pt == None:
        op_pt = 0
    
    if op_pt not in time_steps:
        warnings.warn('Invalid operating point provided by user. \ Running simulation with operating point = 0.')
        op_pt = 0
        
    #returns list of junction demands 
    dq = []
    
    for junc_name, junction in wn.junctions():
        dq.append(junction.demand_timeseries_list[0].base_value)
        
    link_1 = []
    link_2 = []
    
    #build link_list and new_link_list
    for link_name, link in wn.links():
        n1 = link.start_node_name
        n2 = link.end_node_name
        link_1.append(link.start_node_name)
        link_2.append(link.end_node_name)
    link_list = tuple(zip(link_1,link_2))
    new_link_list = list(link_list)
    
    #building junction dictionary
    junc_names = wn.junction_name_list
    junc_dict = {}
    
    for i in range(len(junc_names)):
        junc_name = junc_names[i]
        junction = wn.get_node(junc_name)
        
        connected_nodes = []
        for a,b in new_link_list:
            if (a == junc_name):
                connected_nodes.append(b)
            if (b == junc_name):
                connected_nodes.append(a)

        op_pt_head = results.node['head'].loc[op_pt*report_time_step, junc_name]
            
        junc_dict[junc_name] = {'Demand': junction.demand_timeseries_list[0].base_value, 'Connected nodes': connected_nodes, 'Head at op pt': op_pt_head, 'Diagonal g': 0}
    
    #building pipe dictionary
    pipe_names = wn.pipe_name_list
    pipe_dict = {}
    
    for i in range(len(pipe_names)):
        pipe_name = pipe_names[i]
        pipe = wn.get_link(pipe_name)
        pipe_dict[pipe_name] = {'Start node name': pipe.start_node_name, 'End node name': pipe.end_node_name, 'Length': pipe.length, 'Diameter': pipe.diameter, 'Roughness':pipe.roughness, 'Linear g':0}
        
    # In[]: BUILD LISTS OF SPECIAL AND UNREMOVABLE ELEMENTS
        
    special_links = []
    special_nodes = []
    unremovable_nodes = []
    special_links_nodes = []
    
    #check reservoirs and tanks
    for res_name, reservoir in wn.reservoirs():
        if reservoir.name not in special_nodes:
            special_nodes.append(reservoir.name)
            unremovable_nodes.append(reservoir.name)
    
    for tank_name, tank in wn.tanks():
        if tank.name not in special_nodes:
            special_nodes.append(tank.name)
            unremovable_nodes.append(tank.name)
    
    #check nodes with negative demand
    for i in range(len(dq)):
        if dq[i]<0:
            if junc_names[i] not in special_nodes:
                special_nodes.append(junc_names[i])
                unremovable_nodes.append(junc_names[i])
    
    #check nodes connected to pumps and valves
    for pump_name, pump in wn.pumps():
        n1 = pump.start_node_name
        n2 = pump.end_node_name
        if n1 not in special_nodes:
            unremovable_nodes.append(n1)
        if n2 not in special_nodes:
            unremovable_nodes.append(n2)
        special_links.append(pump_name)
        special_links_nodes.append((n1,n2))
        
    for valve_name, valve in wn.valves():
        n1 = valve.start_node_name
        n2 = valve.end_node_name
        if n1 not in special_nodes:
            unremovable_nodes.append(n1)
        if n2 not in special_nodes:
            unremovable_nodes.append(n2)
        special_links.append(valve_name)
        special_links_nodes.append((n1,n2))
    
    #identify junctions and links with control rules
    junc_with_controls = []
    pipe_with_controls = []
    for name, control in wn.controls():
            for req in control.requires():
                if isinstance(req, Junction):
                    junc_with_controls.append(req.name)
                elif isinstance(req, Pipe):
                    pipe_with_controls.append(req.name)
    junc_with_controls = list(set(junc_with_controls))
    pipe_with_controls = list(set(pipe_with_controls))
    
    #set control junctions and links to be unremovable
    for junc_name in junc_with_controls:
        if junc_name not in unremovable_nodes:
            unremovable_nodes.append(junc_name)
            
    for pipe_name in pipe_with_controls:
        n1 = wn.get_link(pipe_name).start_node_name
        n2 = wn.get_link(pipe_name).end_node_name
        if n1 not in special_nodes and n1 not in unremovable_nodes:
            unremovable_nodes.append(n1)
        if n2 not in special_nodes and n2 not in unremovable_nodes:
            unremovable_nodes.append(n2)
        special_links.append(pipe_name)
        special_links_nodes.append((n1,n2))
    
    #check nodes connected to special nodes          
    for a,b in new_link_list:
        if (a in special_nodes and b not in special_nodes):
            if b not in unremovable_nodes:
                unremovable_nodes.append(b)
        if (b in special_nodes and a not in special_nodes):
            if a not in unremovable_nodes:
                unremovable_nodes.append(a)    
                
    #check list of nodes to keep provided by user
    if nodes_to_keep is not None:
        counter = 0
        for i in range(len(nodes_to_keep)):
            if nodes_to_keep[i] not in unremovable_nodes and nodes_to_keep[i] not in special_nodes and nodes_to_keep[i] in junc_names:
                unremovable_nodes.append(nodes_to_keep[i])
            else:
                counter = counter+1
        if counter > 0:
            warnings.warn('Some values in list of nodes to keep provided by user do not exist in the model or have already been classified as special nodes. These values have been ignored.')
                    
    #build relations
    connected_nodes = []
    num_connections = []
    
    for i in range(len(junc_names)):
        connected_nodes.append([])
        for a,b in new_link_list:
            if (a == junc_names[i]):
                connected_nodes[i].append(b)
            if (b == junc_names[i]):
                connected_nodes[i].append(a)
    
    relations = dict(zip(junc_names,connected_nodes))
    
    return wn, op_pt,  pipe_dict,junc_dict,unremovable_nodes,special_nodes,special_links,special_links_nodes, relations, new_link_list, results
