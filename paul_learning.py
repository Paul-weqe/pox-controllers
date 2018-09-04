
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import str_to_bool

log = core.getLogger()

class PaulSwitch( object ):
	
	def __init__(self):
		core.openflow.addListeners(self)
		self.mac_to_port = {}

		return None

	def _handle_ConnectionUp(self, event):
		print("CONNECTION UP")

	def _handle_PacketIn(self, event):

		packet = event.parsed
		
		if packet.type == packet.ARP_TYPE:
			print(True)

		print("PACKET IN")
		
def launch():
	core.registerNew( PaulSwitch )
