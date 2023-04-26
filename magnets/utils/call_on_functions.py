import numpy as np
from packaging.version import Version, parse
import wntr

epsilon = 10**(-6)

#function to calculate alpha
def calculate_unit_coeff(pipe_dict, junc_dict, wn, results, op_pt, special_nodes):
    alpha = []
    pipe_names = wn.pipe_name_list
    
    report_time_step = wn.options.time.report_timestep
    
    for i in range(len(wn.pipe_name_list)):
        if (results.link['flowrate'].loc[op_pt*report_time_step, pipe_names[i]]>0):
            flow = results.link['flowrate'].loc[op_pt*report_time_step, pipe_names[i]]
            pipe = pipe_names[i]
            n1 = pipe_dict[pipe]['Start node name']
            n2 = pipe_dict[pipe]['End node name']
            if n1 not in special_nodes and n2 not in special_nodes:
                h1 = junc_dict[n1]['Head at op pt']
                h2 = junc_dict[n2]['Head at op pt']
                alpha.append(((abs(h1-h2))*((pipe_dict[pipe]['Roughness']/flow)**1.852)*(pipe_dict[pipe]['Diameter']**4.87))/pipe_dict[pipe]['Length'])
    
    return (np.mean(np.array(alpha)))

# alpha = calculate_unit_coeff(pipe_dict, junc_dict, wn)

#function to calulate K
def calc_K(L,D,R,alpha):
    return (alpha*L)/((R**1.852)*(D**4.87))

#function to calculate non-linear g
def nonlin_g(leng,diam,rough,alpha):
    K = 0
    g = 0
    K = calc_K(leng,diam,rough,alpha)
    g = (1/K)**(1/1.852)
    return g

#function to convert non-linear to linearized g
def nonlin_g_to_lin_g(g, h1, h2):
    if h1 == h2:
        h1 = 0
        h2 = epsilon
    return ((g*(abs(h1-h2)**((1/1.852)-1)))/1.852)

#function to convert linearized to non-linear g
def lin_g_to_nonlin_g(g,h1,h2):
    if h1 == h2:
        h1 = 0
        h2 = epsilon
    return ((abs(g)*1.852)/(abs(h1-h2)**((1/1.852)-1)))

#function calculate diameter of each new pipe
def calculate_new_D(g, L, alpha, C):
    return ((((g/C)**1.852)*alpha*L)**(1/4.87))

#function to calculate pipe length of all new pipes
def new_pipe_length(wn, pipe_dict):
    lengths = []
    pipe_names = wn.pipe_name_list
    for i in range(len(wn.pipe_name_list)):
        lengths.append(pipe_dict[pipe_names[i]]['Length'])
    return (np.mean(np.array(lengths)))

def writeinpfile(wn, new_name):
    if parse(str(wntr.__version__)) < parse('0.5.0'):
        wn.write_inpfile(new_name)
    else:
        wntr.network.io.write_inpfile(wn, new_name)