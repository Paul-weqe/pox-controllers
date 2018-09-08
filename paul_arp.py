from pox.core import core
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.arp import arp 
import pox.openflow.libopenflow_01 as of


log = core.getLogger()

class CustomArp():
	def __init__(self):
		core.openflow.addListeners(self)
		self.ip_to_mac = {}
		self.dpid_ip_to_port = {}


	def _handle_PacketIn(self, event):
		print(event.dpid)
		eth_packet = event.parsed

		if eth_packet.type != ethernet.ARP_TYPE:
			return
		log.info("HANDLE ARP PACKET")
		arp_packet = eth_packet.payload

		# learns the source MAC address and maps it to a specific port
		self._do_source_learning(event)

		# Process ARP packet
		if arp_packet.opcode == arp.REQUEST:
			self._handle_arp_request(event)
		elif arp_packet.opcode == arp.REPLY:
			self._handle_arp_reply(event)
	
	def _handle_arp_request(self, event):
		eth_packet = event.parsed
		arp_packet = eth_packet.payload
		if arp_packet.protodst not in self.ip_to_mac:
			log.info("MAC {} NOT MATCHED IN TABLE".format(arp_packet.protodst))
			for conn in core.openflow.connections:
				conn_ports = conn.features.ports 

				host_ports = [ port.port_no for port in conn_ports
                              if port.port_no not in
                              self.dpid_ip_to_port.values() ]

				action_out_ports = [of.ofp_action_output(port=port) for port in host_ports]

				core.openflow.sendToDPID( conn.dpid, of.ofp_packet_out(
					data = eth_packet.pack(),
					action=action_out_ports
					) )

		else:
			# if the entry exists
			dst_mac = self.ip_to_mac[arp_packet.protodst]
			switch_id = event.dpid

	def _handle_arp_reply(self, event):
		eth_packet = event.parsed
		arp_packet = eth_packet.payload
		

	def _do_source_learning(self, event):
		eth_packet = event.parsed
		arp_packet = eth_packet.payload
		if arp_packet.protosrc not in self.ip_to_mac:
			self.ip_to_mac[arp_packet.protosrc] = arp_packet.hwsrc
			log.info("Learn: ip={} => mac={}".format(arp_packet.protosrc,
				arp_packet.hwsrc))

def launch():
	print("STARTED")
	core.registerNew(CustomArp)
