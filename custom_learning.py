"""
This code is aimed at creating a learning switch using the pox controller
it basically learns the mac address of hosts and their ports
then forwards the data to the specific ports.

If the destination port is unknown, the packet is flooded
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool


log = core.getLogger()

class LearningSwitch( object ):
	
	def __init__(self):

		core.openflow.addListeners(self)
		
		self.connections = set()
		self.mac_to_port = {}
		
	def _handle_PacketIn(self, event):
		log.info(" PACKET IN PEOPLE ")
		packet = event.parsed

		# this function floods the packet to all the ports appart from the port in which it was received
		def flood():
			msg = of.ofp_flow_mod()
			msg.actions.append( of.ofp_action_output(port = of.OFPP_FLOOD) )
			msg.in_port = event.port
			event.connection.send( msg )

		# sees if the packet was a broadcast or a multicast 
		# floods the packet if this is true
		if packet.dst.is_multicast:
			print("MULTICAST")
			flood()

		# this happens if the packet is sent to a specific user and is not broadcasted or multicasted
		else:
			print("UNICAST")

			# looks if the 
			if packet.dst not in self.mac_to_port:
				flood()

			else:
				msg = of.ofp_flow_mod()
				dst_port = self.mac_to_port[packet.dst]
				msg.actions.append( of.ofp_action_output(port = dst_port) )
				msg.data = event.ofp
				# msg.in_port = event.port
				event.connection.send(msg)

		self.mac_to_port[packet.src] = event.port
		print(self.mac_to_port)

	"""
	def _handle_ConnectionUp( self, event ):
		msg = of.ofp_flow_mod()
		msg.actions.append( of.ofp_action_output(port = of.OFPP_FLOOD) )
		event.connection.send( msg ) 
		log.info(" CONNECTION UP PEOPLE ")
	"""
	
	def _handle_PortStatus( self, event ):
		if event.added:
			action = "added"
		elif event.deleted:
			action = "deleted"
		else:
			action = "modified"
		print( "Port {} has been {}".format(event.port, action) )

def launch():
	core.registerNew( LearningSwitch ) #, str_to_bool(transparent))