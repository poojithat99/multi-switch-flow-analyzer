from pox.core import core
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class LearningSwitch(object):
    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        connection.addListeners(self)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return
        self.mac_to_port[packet.src] = event.port
        if packet.dst in self.mac_to_port:
            out_port = self.mac_to_port[packet.dst]
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match.from_packet(packet, event.port)
            msg.idle_timeout = 30
            msg.hard_timeout = 0
            msg.priority = 1
            msg.actions.append(of.ofp_action_output(port=out_port))
            msg.data = event.ofp
            self.connection.send(msg)
        else:
            msg = of.ofp_packet_out()
            msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            msg.data = event.ofp
            msg.in_port = event.port
            self.connection.send(msg)

class LearningSwitch_Launch(object):
    def __init__(self):
        core.openflow.addListeners(self)

    def _handle_ConnectionUp(self, event):
        log.info("Switch %s connected." % dpidToStr(event.dpid))
        LearningSwitch(event.connection)

def launch():
    core.registerNew(LearningSwitch_Launch)
