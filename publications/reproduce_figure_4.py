# In[]: IMPORTING LIBRARIES

import wntr
import numpy as np
import matplotlib.pyplot as plt
import magnets as mg

# In[]: Import KY2 inp file

inp_file = 'networks/ky2.inp'
op_pt_1 = 0
op_pt_2 = 13

# In[]: Reduce KY2 inp file with two different operating points and extract extended period simulation results
    
# Extract hyraulic simulation results for original model
wn = wntr.network.WaterNetworkModel(inp_file)
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

tank2_level = results.node['head'].loc[:,'T-2']
pump1_flow = results.link['flowrate'].loc[:,'~@Pump-1']

# Reduce model with operating point = 0
wn2 = mg.reduction.reduce_model(inp_file, op_pt_1)
sim2 = wntr.sim.EpanetSimulator(wn2)
results2 = sim2.run_sim()

# Reduce model with operating point = 13
wn3 = mg.reduction.reduce_model(inp_file, op_pt_2)
sim3 = wntr.sim.EpanetSimulator(wn3)
results3 = sim3.run_sim()

# Extract simulation results for tank T-2 and pump ~@Pump-1
tank2_level_red_0 = results2.node['head'].loc[:,'T-2']
tank2_level_red_13 = results3.node['head'].loc[:,'T-2']

pump1_flow_red_0 = results2.link['flowrate'].loc[:,'~@Pump-1']
pump1_flow_red_13 = results3.link['flowrate'].loc[:,'~@Pump-1']


duration = len(tank2_level)
x_values = np.linspace(0,duration-1,duration) 

# In[] Plot tank heads and pump flow rates to compare

fig, ax = plt.subplots(2,2 , figsize=(12,8))
ax[0,0].plot(x_values, tank2_level, 'k')
ax[0,0].plot(x_values, tank2_level_red_0, 'k--')
ax[0,0].set_ylabel('Node head [$m$]',fontsize = 14)

ax[1,0].plot(x_values, pump1_flow, color = 'k')
ax[1,0].plot(x_values, pump1_flow_red_0, 'k--')
ax[1,0].set_ylabel('Flowrate [$m^3/s$]',fontsize=14)
ax[1,0].set_xlabel('Time [$hr$]',fontsize = 14)

ax[0,1].plot(x_values, tank2_level, 'k')
ax[0,1].plot(x_values, tank2_level_red_13, 'k--')

ax[1,1].plot(x_values, pump1_flow, color = 'k')
ax[1,1].plot(x_values, pump1_flow_red_13, 'k--')
ax[1,1].set_xlabel('Time [$hr$]',fontsize = 14)
plt.show()
