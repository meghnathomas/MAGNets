import numpy as np
import wntr
from magnets import reduction as mr
import time

# Define .INP file and operating point
inp_file = 'Net3 ND.inp'
op_pt = 3

# Find EPS results for original model
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

# Create dictionary to store heads of nodes in original model
junc_names = wn.junction_name_list
num_junc = len(junc_names)
junc_dict = {}

for i in range(num_junc):
    junc_dict[junc_names[i]] = {'Original head': results.node['head'].loc[:, junc_names[i]]}

# Define a function to calculate percentage deviation of heads between reduced and original models
def plot_fn(wn,wn2, op_pt):
    
    # Find EPS results for reduced model
    sim2 = wntr.sim.EpanetSimulator(wn2)
    results2 = sim2.run_sim()
    
    junc_names = wn2.junction_name_list
    num_junc = len(junc_names)
    
    # Store heads od nodes in reduced model
    for i in range(num_junc):
        junc_dict[junc_names[i]]['Reduced head'] = results2.node['head'].loc[:, junc_names[i]]
    
    error = []
        
    for i in range(num_junc):
        error.append(abs((junc_dict[junc_names[i]]['Original head']-junc_dict[junc_names[i]]['Reduced head'])/junc_dict[junc_names[i]]['Original head'])*100)

    return np.average(np.array(error)), np.median(np.array(error))

# Generate four sets of lists with 25%, 50%, 75%, 100% of nodes removed 
junc_name_list = wn.junction_name_list
num_junc = len(junc_name_list)

link_1 = []
link_2 = []
 
# Build link_list and new_link_list
for link_name, link in wn.links():
    n1 = link.start_node_name
    n2 = link.end_node_name
    link_1.append(link.start_node_name)
    link_2.append(link.end_node_name)
link_list = tuple(zip(link_1,link_2))
new_link_list = list(link_list)
 
connections = []

for i in range(num_junc):
    junc_name = junc_name_list[i]
    junction = wn.get_node(junc_name)

    connected_nodes = []
    for a,b in new_link_list:
        if (a == junc_name):
            connected_nodes.append(b)
        if (b == junc_name):
            connected_nodes.append(a)
    connections.append(len(connected_nodes))
       
# Build static ordered list
new_list = [x for _, x in sorted(zip(connections, junc_name_list))]

quad_1 = int(num_junc/4)
quad_2 = 2*quad_1
quad_3 = 3*quad_1

list_1 = []
list_2 = []
list_3 = []
    
for i in range(quad_1):
    list_1.append(new_list[i])
    list_2.append(new_list[i])
    list_3.append(new_list[i])

for i in range(quad_1, quad_2):
    list_2.append(new_list[i])
    list_3.append(new_list[i])

    
for i in range(quad_2, quad_3):
    list_3.append(new_list[i])

# In[]:

# Generate new reduced inp files for each list

# Remove 25% of nodes
wn = wntr.network.WaterNetworkModel(inp_file)
t1 = time.time()
wn4 = mr.reduce_model(inp_file, op_pt, list_3)
t2 = time.time()
e4, e41 = plot_fn(wn,wn4,op_pt)

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('Statically ordered list of nodes to keep')
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print('25% nodes removed')
print('Number of edges left in model:',len(wn4.pipe_name_list))
print('Average error value:',e4)
print('Median error value:',e41)
print('Reduction time:', t2-t1)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
# In[]

# Remove 50% of nodes
wn = wntr.network.WaterNetworkModel(inp_file)
t3 = time.time()
wn3 = mr.reduce_model(inp_file, op_pt, list_2)
t4 = time.time()
e3, e31 = plot_fn(wn,wn3,op_pt)

print('50% nodes removed')
print('Number of edges left in model:',len(wn3.pipe_name_list))
print('Average error value:',e3)
print('Median error value:',e31)
print('Reduction time:', t4-t3)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# In[]

# Remove 75% of nodes
wn = wntr.network.WaterNetworkModel(inp_file)
t5 = time.time()
wn2 = mr.reduce_model(inp_file, op_pt, list_1)
t6 = time.time()
e2, e21 = plot_fn(wn,wn2,op_pt)

print('75% nodes removed')
print('Number of edges left in model:',len(wn2.pipe_name_list))
print('Average error value:',e2)
print('Median error value:',e21)
print('Reduction time:', t6-t5)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

# In[]

# Remove all nodes
wn = wntr.network.WaterNetworkModel(inp_file)
t7 = time.time()
wn5 = mr.reduce_model(inp_file, op_pt)
t8 = time.time()
e, e1 = plot_fn(wn, wn5, op_pt)

print('100% nodes removed')
print('Number of edges left in model:',len(wn5.pipe_name_list))
print('Average error value:',e)
print('Median error value:',e1)
print('Reduction time:', t8-t7)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')