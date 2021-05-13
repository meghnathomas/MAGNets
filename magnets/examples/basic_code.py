import wntr
import magnets as mg
from wntr.epanet.util import *
import time

inp_file = 'Net3 new demand LS.inp'

t1 = time.time()

# Run the model reduction code
wn2 = mg.reduction.reduce_model(inp_file, 7)

t2 = time.time()

print('Reduction time = ', t2-t1)
