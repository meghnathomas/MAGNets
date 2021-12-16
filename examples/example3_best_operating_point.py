import wntr
import magnets.reduction as mr
import time
import numpy as np

# Define .INP file 
inp_file = 'networks/ky1.inp'

# Find EPS results for original model
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

report_time_step = wn.options.time.report_timestep

horizon = int(wn.options.time.duration/report_time_step) # Total number of time steps in the simulation report

max_error = []

# Loop through all operating points and find percentage deviation of nodes remaining in reduced model from equivalent nodes in original model
t1 = time.time()
for i in range(horizon):
    wn2 = mr.reduce_model(inp_file, i)
    sim2 = wntr.sim.EpanetSimulator(wn2)
    results2 = sim2.run_sim()
    
    junc_names = wn2.junction_name_list
    
    error = []
    
    for j in range(len(junc_names)):
        
        h1 = results.node['head'].loc[:,junc_names[j]]
        h2 = results2.node['head'].loc[:,junc_names[j]]
        error.append((max(abs((h1-h2)*100/h1))))
        
    # Find largest percentage error value amongst all remaining nodes for each operating point
    max_error.append(np.amax(np.array(error)))

t2 = time.time()    
best_op_pt = np.argmin(max_error) # Find operating point with lowest maximum error

# Display results
print('INP file:', inp_file)
print('Best operating point for this network:',best_op_pt)
print('Maximum error at this operating point:', max_error[best_op_pt])
wn2 = mr.reduce_model(inp_file, best_op_pt)    
print('Total time taken to find best operating point:', t2-t1, 's')
