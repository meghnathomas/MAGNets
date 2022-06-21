# In[]: IMPORTING LIBRARIES

import wntr
import matplotlib.pyplot as plt
import magnets as mg
import networkx.drawing.nx_pylab as nxp

# In[]: Import KY2 inp file

inp_file = 'networks/ky2.inp'

# In[] Define plotting function

def plot_network(wn, title, num):

    G = wn.get_graph()
    G_edge_list = list(G.edges())

    pos_dict = {}
    for node_name, node in wn.nodes():
        pos_dict[node_name] = node.coordinates
                  
    plt.sca(ax[num])
    nxp.draw_networkx_nodes(G, pos_dict, node_size = 5, node_color = 'k', ax = ax[num])
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.tank_name_list, node_size = 30, node_color = 'b', node_shape = 'h', ax = ax[num])
    nxp.draw_networkx_nodes(G, pos_dict, nodelist = wn.reservoir_name_list, node_size = 30, node_color = 'r', node_shape = 's', ax = ax[num])
    nxp.draw_networkx_edges(G, pos_dict, edgelist = G_edge_list, edge_color = 'k', width = 1, arrows = False, ax = ax[num])
    ax[num].set_axis_off
    ax[num].set_title(title)
    
# In[]: Reduce KY2 inp file 
    
# Extract hyraulic simulation results for original model
wn = wntr.network.WaterNetworkModel(inp_file)

# Reduce model with operating point = 0
wn2 = mg.reduction.reduce_model(inp_file)

# In[] Plot the original and reduced networks
fig, ax = plt.subplots(1, 2, figsize=(14,6))
plot_network(wn, 'Full network', 0)
plot_network(wn2, 'Fully reduced network', 1)
plt.setp(ax, ylim=ax[0].get_ylim())
plt.setp(ax, xlim=ax[0].get_xlim())