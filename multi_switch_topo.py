from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink

def multi_switch_topology():
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink)
    c0 = net.addController('c0', controller=RemoteController,
                           ip='127.0.0.1', port=6633)
    s1 = net.addSwitch('s1', protocols='OpenFlow10')
    s2 = net.addSwitch('s2', protocols='OpenFlow10')
    s3 = net.addSwitch('s3', protocols='OpenFlow10')
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    h5 = net.addHost('h5', ip='10.0.0.5/24')
    h6 = net.addHost('h6', ip='10.0.0.6/24')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(h5, s3)
    net.addLink(h6, s3)
    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.start()
    print("Topology started!")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    multi_switch_topology()
