import magnets as mg
import time

# Define .INP file 
inp_file = 'networks/Net3 ND.inp'

# Specify operating point (optional)
op_pt = 3

# Specify list of nodes to keep (optional)
list_of_nodes_to_keep = ['157','107']

# Call model reduction function
t1 = time.time()
wn2 = mg.reduction.reduce_model(inp_file, op_pt, list_of_nodes_to_keep)
t2 = time.time()

# Display reduction time
print('Total reduction time:', t2-t1, 's')


