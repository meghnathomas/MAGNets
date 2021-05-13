import wntr

from magnets.utils import characteristics
from magnets.utils import call_on_functions
from magnets.preprocessing import branch_ends 
from magnets.preprocessing import parallel_pipes
from magnets.reduction import reinitialize
from magnets.reduction import build_g_matrix
from magnets.reduction import mod_reduction

def reduce_model(inp_file, op_pt = None, nodes_to_keep = None):
    
    # initialize lists and junction/pipe characteristics
    wn, op_pt,  pipe_dict,junc_dict,unremovable_nodes,special_nodes,special_links,special_links_nodes, relations, new_link_list, results = characteristics(inp_file, op_pt, nodes_to_keep)
    
    # define constants
    alpha = call_on_functions.calculate_unit_coeff(pipe_dict, junc_dict, wn, results, op_pt, special_nodes)
    new_pipe_len = call_on_functions.new_pipe_length(wn, pipe_dict)
    
    # remove branch end nodes and merge parallel pipes
    wn, junc_dict, pipe_dict, relations, new_link_list = branch_ends(relations, wn, new_link_list, junc_dict, pipe_dict, unremovable_nodes)
    wn, junc_dict, pipe_dict, relations, new_link_list = parallel_pipes(relations, wn, new_link_list, junc_dict, pipe_dict, unremovable_nodes, special_nodes, special_links_nodes, special_links, alpha)
    
    # reduce model
    nodes_to_be_removed, link_list_only_junc, unremovable_nodes = reinitialize(wn,new_link_list, special_nodes, unremovable_nodes)
    junc_dict, pipe_dict = build_g_matrix(wn,junc_dict,pipe_dict, unremovable_nodes, special_nodes, alpha)
    mod_reduction(wn, new_link_list, junc_dict, pipe_dict, unremovable_nodes, relations, nodes_to_be_removed, new_pipe_len, alpha, inp_file)
    
    return wn
    
