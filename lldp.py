import collections
from collections import OrderedDict
from ipaddress import *

from cisco import Cisco


class LLDP():
    """
    class for get the lldp information
    """

    # List of devices we've already checked
    _name_ip = {}

    def get_name_by_ip(self, ip_range):
        """
        return a dictonary with the ip of the network that are Cisco devices
        """

        hosts = list(ip_network(ip_range, False).hosts())

        # get the name of one host
        for x in hosts:
            device_host = str(x)
            print device_host
            try:
                d = Cisco(host=device_host, community='CAMPUS')
                self._name_ip[d.name] = device_host
            except:
                print "The device isn't Cisco"

        return self._name_ip

    # list of the nodes of the network
    _nodes = []
    # list of the links of the network
    _links = []

    # variables for the checking of the algorithm
    _cheked = []
    _insert = []

    # property for get the value of attribute nodes and links
    @property
    def nodes(self):
        """
        returns the attribute that is the result of the method get_nodes
        """
        return self._nodes

    @property
    def links(self):
        """
        returns the attribute that is the result of the method get_links
        """
        return self._links

    def get_nodes_links(self, device, network, cost_hop=1.000):
        """
        find the nodes and links of a network
        """

        # add a node in the list _nodes
        try:
            # prevent the dublication of nodes
            if device.name not in self._insert:
                node = {"id": device.host,
                        "label": device.name}
                self._nodes.append(node)
                self._insert.append(device.name)
        except:
            print "device not recognized"
            return {"id": "", "label": ""}

        # find the neighbours of the device
        try:
            neighbours = device.get_neighbours_names()
        except:
            return

        # if it is an end point return
        if not neighbours:
            return

        # Loop prevention
        for i in range(0, len(neighbours)):
            x = neighbours[i].items()[0][1]
            if x and (x not in self._cheked):

                try:
                    # find the ip of the device
                    # from the dictonary of the network
                    my_host = network[x]
                    # create the new Cisco device
                    d = Cisco(host=my_host, community='CAMPUS')

                    # add a link to the list
                    link = OrderedDict([("source", device.host),
                                        ("target", d.host),
                                        ("cost", cost_hop)])
                    self._links.append(link)
                    # Recurse!
                    self._cheked.append(x)
                    add = self.get_nodes_links(d, network, cost_hop)
                    if add is not None:
                        self._nodes.append(add)

                except KeyError:
                    print "The device is not in the network!"
                    self._cheked.append(x)

        return

    # get the value in NetJSON
    def network_to_netJSON(self, device, network, cost=1.000,):

        # get the network and find the info
        network_devices = self.get_name_by_ip(network)
        self.get_nodes_links(device, network_devices, cost)

        net = collections.OrderedDict(
           [('type', 'NetworkGraph'),
            ('protocol', 'l2'),
            ('version', '0.1'),
            ('router_id', device.host),
            ('label', 'Urbino network'),
            ('nodes', self._nodes),
            ('links', self._links)])

        return net
