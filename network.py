from __future__ import unicode_literals

import json

from cisco import Cisco
from lldp import LLDP

# enter the input data
host = ""
community = ''
network = ''
cost_hops = 1.000

device = Cisco(host=host, community=community)

# create a new lldp object
lldp = LLDP()

# get the data
data = lldp.network_to_netJSON(device, network, cost_hops)

# write the data in json in the network.json file
with open('output/network.json', 'w') as outfile:
    json.dump(data, outfile)
