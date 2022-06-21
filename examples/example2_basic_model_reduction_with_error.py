import wntr 
import magnets.reduction as mr
import time
import numpy as np
import matplotlib.pyplot as plt

"""
This example demonstrates how MAGNets can be used to reduce a water distribution network model around a given operating point, with the user providing a list 
of nodes they would like to retain in the model. Additionally, this example shows how the user can plot the percentage deviation of the pressure heads of each node 
in the reduced model from the equivalent node in the original model to test the accuracy of MAGNets. This characterization of error can inform the user of the degree 
to which they should reduce the model as well as which operating point they should select.

"""

# Define .INP file 
inp_file = 'networks/ky1.inp'

# Define operating point
op_pt = 9

# Call model reduction function
t1 = time.time()
wn2 = mr.reduce_model(inp_file, op_pt)
t2 = time.time()

# Find EPS results for original model
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Find EPS results for reduced model
sim2 = wntr.sim.EpanetSimulator(wn2)
results2 = sim2.run_sim()

# Determine which nodes remain in the reduced model
junc_names = wn2.junction_name_list
num_junc = len(junc_names)

# Plot percentage deviation of node heads in reduced model from original model over entire simulation duration
x_val = len(results2.node['head'].loc[:, junc_names[0]])
time_step = wn.options.time.report_timestep
mult_ts = 3600/time_step
x = np.linspace(0,(x_val-1)/mult_ts,x_val)
error = []

max_error = []
prob_nodes = []
prob_nodes_g = []

plt.figure(figsize=(10,6))
for i in range(num_junc):
    error.append(abs((results.node['head'].loc[:,junc_names[i]]
-results2.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
    plt.plot(x,error[i],label='Error Node {}'.format(junc_names[i]))
    # plt.legend()
    plt.title('Absolute value of relative error of heads for {}'.format(inp_file))
    plt.xlabel('Time [hours]')
    plt.ylabel('Relative error [%]')
    max_error.append(np.amax(np.array(error)))
                            
error_op_pt = np.argmax(max_error)

# Print helpful statistics
print('INP file:', inp_file)
print('Number of junctions in the original model:', len(wn.junction_name_list))
print('Number of junctions in the reduced model:', len(wn2.junction_name_list))
print('Total reduction time:', t2-t1, 's')
print('Maximum percentage error amongst all nodes:',max_error[error_op_pt])
