import wntr
from magnets.utils.call_on_functions import *

def build_g_matrix(wn,junc_dict,pipe_dict, unremovable_nodes, special_nodes, alpha):
    
    num_pipes = len(wn.pipe_name_list)
    
    for a in range(num_pipes):
        pipe = wn.pipe_name_list[a]
        if (pipe_dict[pipe]['Start node name'] not in special_nodes and pipe_dict[pipe]['End node name'] not in special_nodes):
            if (pipe_dict[pipe]['Start node name'] not in unremovable_nodes or pipe_dict[pipe]['End node name'] not in unremovable_nodes):
                nlg = nonlin_g(pipe_dict[pipe]['Length'],pipe_dict[pipe]['Diameter'],pipe_dict[pipe]['Roughness'],alpha)
                lg = nonlin_g_to_lin_g(nlg,junc_dict[pipe_dict[pipe]['Start node name']]['Head at op pt'],junc_dict[pipe_dict[pipe]['End node name']]['Head at op pt'])
                pipe_dict[pipe]['Linear g'] = -lg
                junc_dict[pipe_dict[pipe]['Start node name']]['Diagonal g'] = junc_dict[pipe_dict[pipe]['Start node name']]['Diagonal g'] - pipe_dict[pipe]['Linear g']
                junc_dict[pipe_dict[pipe]['End node name']]['Diagonal g'] = junc_dict[pipe_dict[pipe]['End node name']]['Diagonal g'] - pipe_dict[pipe]['Linear g']
                
    
    return junc_dict, pipe_dict
