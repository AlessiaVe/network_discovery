# Network Discovery

Network discovery has the purpose to get informations from the Cisco devices of a network. This work uses the library Netengine for the informations and the library Netjsongraph to build a graph with the nodes of the network.

## Usage

The usage of the library require the installation of the server Apache and the query must be done on devices that have the lldp protocol enable. Only these devices are marked by the network scan. 
These are the steps that must be done to view the result:
1. open the network.py file and insert the value of the ip, the network and the cost by hop: 
```python
host = "192.168.17.10"
community = 'string_of_the_community'
network = '192.168.17.0/22'
cost_hops = 1.000
```
2. open a terminal and enter into the folder of the project;
3. run the file network.py, with the command:
```python
python network.py
```
4. copy the content of the folder output in the folder of the Apache server;

5. open the browser and search the path: 127.0.0.1/path/of/the/file/output.html. With Chrome is necessary to open Chrome in a terminal with:
```
chrome --allow-file-acces-from-file.
```

## References

The links to the libraries are reported hereinafter:
1. [Netengine](https://github.com/ninuxorg/netengine)
2. [Netjsongraph](https://github.com/netjson/netjsongraph.js)
