# Import libraries
import magnets as mg
import wntr 
import time
import numpy as np
import pandas as pd

# Please uncomment and modify line 10 to reflect the directory in which this code is present on your machine if you want to write the results to a csv file
# Make sure this folder also contains the "networks" folder
#file_path = r'...\publications'  

# Define list of test networks
network_list = ['Net1.inp', 'Net2.inp', 'Net3 ND.inp', 'ky1.inp', 'ky2.inp', 'ky3.inp', 'ky4.inp', 'ky5.inp', 'ky6.inp', 'ky7.inp', 'ky8.inp', 'bwsn2.inp']

# List of "best" operating points for each network (operating point that results in lowest maximum percentage error for each network)
op_pt_list = [7, 16, 3, 9, 13, 5, 0, 32, 38, 24, 14, 35]

# Initialize dictionary to hold results
results_dict = {'Network': network_list,
                'Number of Junctions in Original Model': [], 
                'Number of Junctions in Reduced Model': [],
                'Reduction Time [s]': [],
                'Maximum Error [%]': []}
                               
# Iterate through each network
for inp_file in network_list:
    
    op_pt = op_pt_list[network_list.index(inp_file)]
    
    # Find EPS results for original model
    wn = wntr.network.WaterNetworkModel('networks/' + inp_file)
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()

    # Call model reduction function and find EPS results
    t1 = time.time()
    wn2 = mg.reduction.reduce_model('networks/' + inp_file, op_pt)
    t2 = time.time()
    sim2 = wntr.sim.EpanetSimulator(wn2)
    results2 = sim2.run_sim()
           
    # Determine which nodes remain in the reduced model
    junc_names = wn2.junction_name_list
    num_junc = wn2.num_junctions
    
    # Find maximum percentage deviation of node heads in reduced model from original model over entire simulation duration
    error_each_node = []
    max_error_each_node = []
    
    for i in range(num_junc):
        error_each_node.append(abs((results.node['head'].loc[:,junc_names[i]]
    -results2.node['head'].loc[:,junc_names[i]])/results.node['head'].loc[:,junc_names[i]])*100)
        max_error_each_node.append(np.amax(np.array(error_each_node)))
                                
    max_error_op_pt = np.argmax(max_error_each_node)
    largest_error = max_error_each_node[max_error_op_pt]
    
    results_dict['Number of Junctions in Original Model'].append(wn.num_junctions)
    results_dict['Number of Junctions in Reduced Model'].append(wn2.num_junctions)
    results_dict['Reduction Time [s]'].append(t2 - t1)
    results_dict['Maximum Error [%]'].append(largest_error)
        
# Store results dictionary as dataframe and display results
results_df = pd.DataFrame.from_dict(results_dict)
print(results_df)

# Uncomment the line below if you want to store the results in a csv file
#results_df.to_csv(file_path + '\results.csv')  
