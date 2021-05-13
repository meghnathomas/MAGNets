"""
The relative error function calculates the perecentage difference (of pressure heads of the nodes in the reduced file) between the original and reduced INP files.

"""

import wntr
import matplotlib.pyplot as plt
import numpy as np


def relative_error(inp_file,inp_file2):
    
    wn = wntr.network.WaterNetworkModel(inp_file)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    
    wn2 = wntr.network.WaterNetworkModel(inp_file2)
    sim2 = wntr.sim.EpanetSimulator(wn2)
    results2 = sim2.run_sim()
    
    junc_names = wn2.junction_name_list
    num_junc = len(junc_names)
    print(num_junc)
    
    
    x_val = len(results2.node['head'].loc[:, junc_names[0]])
    x = np.linspace(0,x_val-1,x_val)
    error = []
    
    plt.figure(figsize=(10,6))
    
    for i in range(num_junc):
        error.append(abs((results.node['head'].loc[:,junc_names[i]]
    -results2.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
        plt.plot(x,error[i],label='Error Node {}'.format(junc_names[i]))
        plt.legend()
        plt.title('Absolute value of relative error of heads for {}'.format(inp_file))
        plt.xlabel('Time [hours]')
        plt.ylabel('Relative error [%]')
        
    return 1
  