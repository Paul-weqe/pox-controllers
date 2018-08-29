from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.addresses import IPAddr

class Chris( object ):

	def __init__(self):
		core.openflow.addListeners(self)

	def _handle_PacketIn(self, event):

		
		def host1():
			msg = of.ofp_flow_mod()
			msg.match.in_port = 1
			msg.match.tp_dst = 8000
			msg.match.nw_dst = IPAddr("10.0.0.3")
			msg.actions.append(of.ofp_action_output(port = 3))
			event.connection.send(msg)

		def host2():
			msg = of.ofp_flow_mod()
			msg.match.in_port = 2
			msg.match.tp_dst = 8000
			msg.match.nw_dst = IPAddr("10.0.0.4")
			msg.actions.append(of.ofp_action_output(port = 4))
			event.connection.send(msg)

		def host3():
			msg = of.ofp_flow_mod()
			msg.match.in_port = 3
			msg.match.nw_dst = IPAddr("10.0.0.1")
			msg.actions.append(of.ofp_action_output(port = 1))
			event.connection.send(msg)
            
		def host4():
			msg = of.ofp_flow_mod()
			msg.match.in_port = 4
			msg.match.nw_dst = IPAddr("10.0.0.2")
			msg.actions.append(of.ofp_action_output(port = 2))
			event.connection.send(msg)

		host1()
		host2()
		host3()
		host4()
		

def launch():
	print("CHRIS IS UP")
	core.registerNew( Chris )
	