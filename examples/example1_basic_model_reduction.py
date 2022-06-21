import magnets as mg
import time

"""
This basic example demonstrates how MAGNets can be used to reduce a water distribution network model around a given operating point, with the user providing a list 
of nodes they would like to retain in the model.

"""

# Define .INP file 
inp_file = 'networks/Net3 ND.inp'

# Specify operating point (optional)
op_pt = 3

# Specify list of nodes to keep (optional)
list_of_nodes_to_keep = ['157','107']

# Specify maximum nodal degree in reduced model (optional)
# max_nodal_degree = 1 indicates removal of only branches and merging of parallel pipes
# max_nodal_degree = 2 indicates removal of branches, merging of parallel pipes, and merging of pipes in series
max_nodal_degree = None 

# Call model reduction function
t1 = time.time()
wn2 = mg.reduction.reduce_model(inp_file, op_pt, list_of_nodes_to_keep, max_nodal_degree)
t2 = time.time()

# Display reduction time
print('Total reduction time:', t2-t1, 's')


