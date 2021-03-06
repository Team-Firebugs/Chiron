#!/usr/bin/python
# Filename: sniffer_process.py
#import multiprocessing
from scapy.all import *
version = '0.9'

class mySniffer():
    #def __init__ (self,filter,interface,scan_type,myresults, packets_sent_list,q):
    def __init__ (self,filter,interface,scan_type,packets_sent_list,q, sniffer_timeout):
        self.filter = filter
        self.packets_sent_list = packets_sent_list
        self.interface = interface
        self.scan_type=scan_type
	self.q=q
	self.sniffer_timeout=sniffer_timeout
	print "Starting sniffing..."
	print "Sniffer filter is",self.filter
	print "I will sniff for",self.sniffer_timeout,"seconds, unless interrupted by Ctrl-C"
    	sniff(filter=self.filter, iface=self.interface, prn=self.handler, store=0, timeout=self.sniffer_timeout)
    def handler(self,packets):
        #Due to the filter used, only IPv6 traffic should be captured
		res=[]
	#if packets.haslayer(IPv6):#because it seems that the filter does not apply immediately and the very first traffic goes through: Scapy bug?
        	if packets.haslayer(ICMPv6DestUnreach):
			if self.scan_type==6:
				returned_packet=packets.getlayer(ICMPv6DestUnreach)
				if returned_packet.haslayer(ICMPv6EchoRequest):
					embedded_packet=returned_packet.getlayer(ICMPv6EchoRequest)
					if self.packets_sent_list.has_key(embedded_packet.id):
						res.append(self.packets_sent_list.get(embedded_packet.id)[1])
						res.append(self.packets_sent_list.get(embedded_packet.id)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6DestUnreach.type%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code%")
				elif returned_packet.payload.haslayer(TCPerror):
					embedded_packet=returned_packet.getlayer(TCPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6DestUnreach.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code%")
				elif returned_packet.payload.haslayer(UDPerror):
					embedded_packet=returned_packet.getlayer(UDPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6DestUnreach.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code%")
				elif returned_packet.payload.haslayer(TCP):
					embedded_packet=returned_packet.getlayer(TCP)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6DestUnreach.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code%")
				elif returned_packet.payload.haslayer(UDP):
					embedded_packet=returned_packet.getlayer(UDP)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6DestUnreach.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code%")
				else:
					print returned_packet.summary()
			else:
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1 or self.scan_type==5:
					res.append(packets.sprintf("%src%"))
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6DestUnreach.type%"))
				res.append(packets.sprintf("%ICMPv6DestUnreach.code%"))
				if packets.payload.payload.payload.nh==17:#if UDP
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code% Target:"),packets.payload.payload.payload.sprintf("%dst%"),packets.payload.payload.payload.payload.sprintf("UDP port %dport% CLOSED")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.payload.sprintf("UDP port %dport% CLOSED"))
				elif packets.payload.payload.payload.nh==6:#if TCP
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code% Target:"),packets.payload.payload.payload.sprintf("%dst%"),packets.payload.payload.payload.payload.sprintf("TCP port %dport% CLOSED")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.payload.sprintf("TCP port %dport% CLOSED"))
				elif packets.payload.payload.payload.nh==58:#if ICMPv6
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code% Enclosed Protocol:"),packets.payload.payload.sprintf("%nh%"),packets.payload.payload.payload.sprintf("%type% %code%")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.payload.sprintf("Type: %type%"))
					res.append(packets.payload.payload.payload.payload.sprintf("Code: %code%"))
				else:
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6DestUnreach.type% %ICMPv6DestUnreach.code% Enclosed Protocol:"),packets.payload.payload.sprintf("%nh%")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.sprintf("Enclosed protocol: %nh%"))
        	elif packets.haslayer(ICMPv6ParamProblem):
			if self.scan_type==6:
				returned_packet=packets.getlayer(ICMPv6ParamProblem)
				if returned_packet.haslayer(ICMPv6EchoRequest):
					embedded_packet=returned_packet.getlayer(ICMPv6EchoRequest)
					if self.packets_sent_list.has_key(embedded_packet.id):
						res.append(self.packets_sent_list.get(embedded_packet.id)[1])
						res.append(self.packets_sent_list.get(embedded_packet.id)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6ParamProblem.type%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%ICMPv6ParamProblem.type% %ICMPv6ParamProblem.code%")
				elif returned_packet.payload.haslayer(TCPerror):
					embedded_packet=returned_packet.getlayer(TCPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6ParamProblem.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6ParamProblem.type% %ICMPv6ParamProblem.code%")
				elif returned_packet.payload.haslayer(UDPerror):
					embedded_packet=returned_packet.getlayer(UDPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6ParamProblem.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6ParamProblem.type% %ICMPv6ParamProblem.code%")
			else:
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6ParamProblem.type% %ICMPv6ParamProblem.code%")
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1 or self.scan_type==5:
					res.append(packets.sprintf("%src%"))
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6ParamProblem.type%"))
				res.append(packets.sprintf("%ICMPv6ParamProblem.code%"))
				res.append(packets.sprintf("%ICMPv6ParamProblem.ptr%"))
        	elif packets.haslayer(ICMPv6TimeExceeded):
			if self.scan_type==6:
				returned_packet=packets.getlayer(ICMPv6TimeExceeded)
				if returned_packet.haslayer(ICMPv6EchoRequest):
					embedded_packet=returned_packet.getlayer(ICMPv6EchoRequest)
					if self.packets_sent_list.has_key(embedded_packet.id):
						res.append(self.packets_sent_list.get(embedded_packet.id)[1])
						res.append(self.packets_sent_list.get(embedded_packet.id)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6TimeExceeded.type%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code%")
				elif returned_packet.payload.haslayer(TCPerror):
					embedded_packet=returned_packet.getlayer(TCPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6TimeExceeded.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code%")
				elif returned_packet.payload.haslayer(TCP):
					embedded_packet=returned_packet.getlayer(TCP)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6TimeExceeded.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code%")
				elif returned_packet.payload.haslayer(UDPerror):
					embedded_packet=returned_packet.getlayer(UDPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6TimeExceeded.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code%")
				elif returned_packet.payload.haslayer(UDP):
					embedded_packet=returned_packet.getlayer(UDP)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6TimeExceeded.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code%")
				else:
					print returned_packet.summary()
			else:
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code%")
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1 or self.scan_type==5:
					res.append(packets.sprintf("%src%"))
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6TimeExceeded.type%"))
				res.append(packets.sprintf("%ICMPv6TimeExceeded.code%"))
				if packets.payload.payload.payload.nh==17:#if UDP
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code% Target:"),packets.payload.payload.payload.sprintf("%dst%"),packets.payload.payload.payload.payload.sprintf("UDP port %dport% CLOSED")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.payload.sprintf("UDP port %dport% CLOSED"))
				elif packets.payload.payload.payload.nh==6:#if TCP
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code% Target:"),packets.payload.payload.payload.sprintf("%dst%"),packets.payload.payload.payload.payload.sprintf("TCP port %dport% CLOSED")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.payload.sprintf("TCP port %dport% CLOSED"))
				elif packets.payload.payload.payload.nh==58:#if ICMPv6
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code% Enclosed Protocol:"),packets.payload.payload.sprintf("%nh%"),packets.payload.payload.payload.sprintf("%type% %code%")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.payload.sprintf("Type: %type%"))
					res.append(packets.payload.payload.payload.payload.sprintf("Code: %code%"))
				else:
                			print packets.sprintf("%src% %IPv6.src% ICMPv6 %ICMPv6TimeExceeded.type% %ICMPv6TimeExceeded.code% Enclosed Protocol:"),packets.payload.payload.sprintf("%nh%")
					res.append(packets.payload.payload.payload.sprintf("Target: %dst%"))
					res.append(packets.payload.payload.payload.sprintf("Enclosed protocol: %nh%"))
        	elif packets.haslayer(ICMPv6PacketTooBig):
			if self.scan_type==6:
				returned_packet=packets.getlayer(CMPv6PacketTooBig)
				if returned_packet.haslayer(ICMPv6EchoRequest):
					embedded_packet=returned_packet.getlayer(ICMPv6EchoRequest)
					if self.packets_sent_list.has_key(embedded_packet.id):
						res.append(self.packets_sent_list.get(embedded_packet.id)[1])
						res.append(self.packets_sent_list.get(embedded_packet.id)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6PacketTooBig.type%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%CMPv6PacketTooBig.type% %CMPv6PacketTooBig.code%")
				elif returned_packet.payload.haslayer(TCPerror):
					embedded_packet=returned_packet.getlayer(TCPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6PacketTooBig.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6PacketTooBig.type% %ICMPv6PacketTooBig.code%")
				elif returned_packet.payload.haslayer(UDPerror):
					embedded_packet=returned_packet.getlayer(UDPerror)
					if self.packets_sent_list.has_key(embedded_packet.sport):
						res.append(self.packets_sent_list.get(embedded_packet.sport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.sport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(returned_packet.sprintf("%ICMPv6PacketTooBig.type%"))
						print self.packets_sent_list.get(embedded_packet.sport)[1],self.packets_sent_list.get(embedded_packet.sport)[0],packets.payload.src,packets.sprintf("%ICMPv6PacketTooBig.type% %ICMPv6PacketTooBig.code%")
			else:
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6PacketTooBig.type% %ICMPv6PacketTooBig.code% %ICMPv6PacketTooBig.mtu%")
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1 or self.scan_type==5:
					res.append(packets.sprintf("%src%"))
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6PacketTooBig.type%"))
				res.append(packets.sprintf("%ICMPv6PacketTooBig.code%"))
				res.append(packets.sprintf("%ICMPv6PacketTooBig.mtu%"))
		elif packets.haslayer(IPv6ExtHdrRouting):
			print packets.sprintf("%src% %IPv6.src% %IPv6.dst% %IPv6ExtHdrRouting.type% %IPv6ExtHdrRouting.addresses% %IPv6ExtHdrRouting.segleft%")
			res.append(packets.sprintf("%IPv6.src%"))
			if self.scan_type==1:
				res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf("%IPv6.dst%"))
			res.append(packets.sprintf("%IPv6ExtHdrRouting.nh%"))
			res.append(packets.sprintf("%IPv6ExtHdrRouting.type%"))
			res.append(packets.sprintf("%IPv6ExtHdrRouting.segleft%"))
			res.append(packets.sprintf("%IPv6ExtHdrRouting.addresses%"))
			#res.append(packets.sprintf("%src%"))
		elif packets.haslayer(IPv6ExtHdrFragment):
			if self.scan_type==6:
				returned_packet=packets.getlayer(IPv6ExtHdrFragment)
				if returned_packet.haslayer(ICMPv6EchoReply):
					embedded_packet=returned_packet.getlayer(ICMPv6EchoReply)
					if self.packets_sent_list.has_key(embedded_packet.id):
						res.append(self.packets_sent_list.get(embedded_packet.id)[1])
						res.append(self.packets_sent_list.get(embedded_packet.id)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(embedded_packet.sprintf("%ICMPv6EchoReply.type%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%IPv6.nh%"),embedded_packet.sprintf("%ICMPv6EchoReply.type%")
				elif returned_packet.haslayer(TCPError):
					embedded_packet=returned_packet.getlayer(TCPError)
					if self.packets_sent_list.has_key(embedded_packet.dport):
						res.append(self.packets_sent_list.get(embedded_packet.dport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.dport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(embedded_packet.sprintf("%TCP.sport%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%IPv6.nh%"),embedded_packet.sprintf("%TCP.sport%")
				elif returned_packet.haslayer(UDPError):
					embedded_packet=returned_packet.getlayer(UDPError)
					if self.packets_sent_list.has_key(embedded_packet.dport):
						res.append(self.packets_sent_list.get(embedded_packet.dport)[1])
						res.append(self.packets_sent_list.get(embedded_packet.dport)[0])
						res.append(packets.payload.sprintf("%IPv6.src%"))
						res.append(embedded_packet.sprintf("%UDP.sport%"))
						print self.packets_sent_list.get(embedded_packet.id)[1],self.packets_sent_list.get(embedded_packet.id)[0],packets.payload.src,packets.sprintf("%IPv6.nh%"),embedded_packet.sprintf("%UDP.sport%")
			else:
				returned_packet=packets.getlayer(IPv6ExtHdrFragment)
				print returned_packet.summary()
				res.append(returned_packet.summary())
        	elif packets.haslayer(ICMPv6EchoReply) and not self.scan_type==3 and not self.scan_type==4 and not self.scan_type==7:
			if self.scan_type==6:
				#print packets.payload.payload.id
				if self.packets_sent_list.has_key(packets.payload.payload.id):
					res.append(self.packets_sent_list.get(packets.payload.payload.id)[1])
					res.append(self.packets_sent_list.get(packets.payload.payload.id)[0])
					res.append(packets.payload.sprintf("%IPv6.src%"))
					res.append(packets.payload.payload.sprintf("%ICMPv6EchoReply.type%"))
					print self.packets_sent_list.get(packets.payload.payload.id)[1],self.packets_sent_list.get(packets.payload.payload.id)[0],packets.payload.src,packets.sprintf("%ICMPv6EchoReply.type% %ICMPv6EchoReply.code%")
			else:
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6EchoReply.type%")
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1 or self.scan_type==5:
					res.append(packets.sprintf("%src%"))
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6EchoReply.type%"))
				res.append(packets.sprintf("%ICMPv6EchoReply.id%"))
				res.append(packets.sprintf("%ICMPv6EchoReply.data%"))
				#res.append(packets.sprintf("%ICMPv6EchoReply.seq%"))
        	elif packets.haslayer(ICMPv6EchoRequest) and self.scan_type==1:
                	print packets.sprintf("%src% %IPv6.src% %ICMPv6EchoRequest.type%")
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf(" ICMPv6 "))
			res.append(packets.sprintf("%ICMPv6EchoRequest.type%"))
			res.append(packets.sprintf("%ICMPv6EchoRequest.id%"))
			res.append(packets.sprintf("%ICMPv6EchoRequest.data%"))
			#res.append(packets.sprintf("%ICMPv6EchoRequest.seq%"))
        	elif packets.haslayer(IPv6ExtHdrHopByHop) and (self.scan_type==1 or self.scan_type==8):
			#print "Hop-by-Hop Header"
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			#print packets.payload.show()
        		if packets.payload.haslayer(ICMPv6MLReport):
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6MLReport.type% %ICMPv6MLReport.mladdr%")
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6MLReport.type%"))
				multicast_address=packets.payload.getlayer(ICMPv6MLReport).mladdr
				if multicast_address=="ff02::1:3":
					res.append("Windows")
				elif multicast_address=="ff02::c":
					res.append("/Client/")
				elif "ff02::2:ff" in multicast_address:
					res.append("FreeBSD")
				elif "ff02::1:2" in multicast_address or "ff05::1:3" in multicast_address:
					res.append("/DHCPv6 Server-Relay/")
				elif ":7fff" in multicast_address:
					res.append("SAPv0")
				elif ":7ffe" in multicast_address:
					res.append("SAPv1")
				else:
					res.append(packets.sprintf("/%ICMPv6MLReport.mladdr%/"))
        		elif packets.payload.haslayer(ICMPv6MLDone):
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6MLDone.type% %ICMPv6MLDone.mladdr%")
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6MLDone.type%"))
				multicast_address=packets.payload.getlayer(ICMPv6MLDone).mladdr
				if multicast_address=="ff02::1:3":
					res.append("/Windows/")
				elif multicast_address=="ff02::c":
					res.append("/Client/")
				elif "ff02::2:ff" in multicast_address:
					res.append("/FreeBSD/")
				elif "ff02::1:2" in multicast_address or "ff05::1:3" in multicast_address:
					res.append("/DHCPv6 Server-Relay/")
				elif "::2:7fff" in multicast_address:
					res.append("/SAPv0/")
				elif "::2:7ffe" in multicast_address:
					res.append("/SAPv1/")
				else:
					res.append(packets.sprintf("/%ICMPv6MLReport.mladdr%/"))
        		elif packets.payload.haslayer(ICMPv6MLQuery):
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6MLQuery.type%")
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6MLQuery.type%"))
				res.append("MLD capable router")
        		elif packets.payload.haslayer(ICMPv6MLReport2):
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6MLReport2.type%")
				res.append(packets.sprintf(" ICMPv6 "))
				res.append(packets.sprintf("%ICMPv6MLReport2.type%"))
			else:
                		print packets.sprintf("%src% %IPv6.src% %ICMPv6MLReport2.type%")
				#print packets.payload.show()
        	elif packets.haslayer(TCP) and (self.scan_type==3 or self.scan_type==1 or self.scan_type==6):
			if self.scan_type==6:
				if self.packets_sent_list.has_key(packets.payload.payload.dport):
					res.append(self.packets_sent_list.get(packets.payload.payload.dport)[1])
					res.append(self.packets_sent_list.get(packets.payload.payload.dport)[0])
					res.append(packets.payload.sprintf("%IPv6.src%"))
					res.append(packets.payload.payload.sprintf("%TCP.sport%"))
					print self.packets_sent_list.get(packets.payload.payload.dport)[1],self.packets_sent_list.get(packets.payload.payload.dport)[0],packets.payload.src,packets.sprintf("%TCP.sport% %TCP.dport%")
			else:
                		print packets.sprintf("%src% %IPv6.src% %dst% %IPv6.dst% TCP %TCP.sport% %TCP.dport% %TCP.flags%")
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1:
					res.append(packets.sprintf("%src%"))
					res.append(packets.sprintf(" TCP "))
					res.append(packets.sprintf("sport=%TCP.sport%"))
					res.append(packets.sprintf("dport=%TCP.dport%"))
					res.append(packets.sprintf("TCPflags=%TCP.flags%"))
				else:
					res.append(packets.sprintf(" TCP "))
					res.append(packets.sprintf("%TCP.sport%"))
					res.append(packets.sprintf("%TCP.flags%"))
        	elif packets.haslayer(UDP) and (self.scan_type==4 or self.scan_type==1 or self.scan_type==6 or self.scan_type==8): #8 is for DHCPv6 operation
			if self.scan_type==6:
				if self.packets_sent_list.has_key(packets.payload.payload.dport):
					res.append(self.packets_sent_list.get(packets.payload.payload.dport)[1])
					res.append(self.packets_sent_list.get(packets.payload.payload.dport)[0])
					res.append(packets.payload.sprintf("%IPv6.src%"))
					res.append(packets.payload.payload.sprintf("%UDP.sport%"))
					print self.packets_sent_list.get(packets.payload.payload.dport)[1],self.packets_sent_list.get(packets.payload.payload.dport)[0],packets.payload.src,packets.sprintf("%UDP.sport% %UDP.dport%")
			layer4_header = packets.getlayer(UDP)
			if (layer4_header.sport==546 and layer4_header.dport==547):
				print "DHCPv6 packet"
				if layer4_header.haslayer(DHCP6_Solicit):
                			print "DHCPv6 Solicit message. Transaction ID =",layer4_header.sprintf("%DHCP6_Solicit.trid%")
					if layer4_header.haslayer(DHCP6OptClientId):
						print "Client DUID =",layer4_header.sprintf("%DHCP6OptClientId.duid%") 
						ClientID=layer4_header.getlayer(DHCP6OptClientId)
						print "Client Identifier =",ClientID.show()
			else:
               			print packets.sprintf("%src% %IPv6.src% %IPv6.dst% UDP %UDP.sport% %UDP.dport%")
				res.append(packets.sprintf("%IPv6.src%"))
				if self.scan_type==1:
					res.append(packets.sprintf("%src%"))
					res.append(packets.sprintf(" UDP "))
					res.append(packets.sprintf("sport=%UDP.sport%"))
					res.append(packets.sprintf("dport=%UDP.dport%"))
				else:	
					res.append(packets.sprintf(" UDP "))
					res.append(packets.sprintf("%UDP.sport%"))
        	elif packets.haslayer(ICMPv6ND_NA) and self.scan_type==1:
                	print packets.sprintf("%src% %IPv6.src% %ICMPv6ND_NA.type% %ICMPv6ND_NA.tgt% ")
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf(" ICMPv6 "))
			res.append(packets.sprintf("%ICMPv6ND_NA.type%"))
			#res.append(packets.sprintf("%ICMPv6ND_NA.code%"))
			res.append(packets.sprintf("%ICMPv6ND_NA.R%"))
			res.append(packets.sprintf("%ICMPv6ND_NA.S%"))
			res.append(packets.sprintf("%ICMPv6ND_NA.O%"))
			res.append(packets.sprintf("%ICMPv6ND_NA.tgt%"))
        	elif packets.haslayer(ICMPv6ND_NS) and self.scan_type==1:
                	print packets.sprintf("%src% %IPv6.src% %ICMPv6ND_NS.type% %ICMPv6ND_NS.tgt% ")
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf(" ICMPv6 "))
			res.append(packets.sprintf("%ICMPv6ND_NS.type%"))
			#res.append(packets.sprintf("%ICMPv6ND_NS.code%"))
			res.append(packets.sprintf("%ICMPv6ND_NS.tgt%"))
        	elif packets.haslayer(ICMPv6ND_RA) and self.scan_type==1:
                	print packets.sprintf("%src% %IPv6.src% %ICMPv6ND_RA.type%")
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf(" ICMPv6 "))
			res.append(packets.sprintf("%ICMPv6ND_RA.type%"))
			#res.append(packets.sprintf("%ICMPv6ND_RA.code%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.chlim%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.M%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.O%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.H%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.prf%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.P%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.routerlifetime%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.reachabletime%"))
			res.append(packets.sprintf("%ICMPv6ND_RA.retranstimer%"))
			if packets.haslayer(ICMPv6NDOptPrefixInfo):
				res.append(packets.sprintf("%ICMPv6NDOptPrefixInfo.prefix%"))
				res.append(packets.sprintf("%ICMPv6NDOptPrefixInfo.prefixlen%"))
				res.append(packets.sprintf("%ICMPv6NDOptPrefixInfo.L%"))
				res.append(packets.sprintf("%ICMPv6NDOptPrefixInfo.A%"))
				res.append(packets.sprintf("%ICMPv6NDOptPrefixInfo.R%"))
				res.append(int(packets.sprintf("%ICMPv6NDOptPrefixInfo.validlifetime%"),16))
				res.append(int(packets.sprintf("%ICMPv6NDOptPrefixInfo.preferredlifetime%"),16))
        	elif packets.haslayer(ICMPv6ND_RS) and self.scan_type==1:
                	print packets.sprintf("%src% %IPv6.src% %ICMPv6ND_RS.type%")
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf(" ICMPv6 "))
			res.append(packets.sprintf("%ICMPv6ND_RS.type%"))
			res.append(packets.sprintf("%ICMPv6ND_RS.code%"))
        	elif packets.haslayer(ICMPv6MLReport) and self.scan_type==1:
               		print packets.sprintf("%src% %IPv6.src% %ICMPv6MLReport.type% %ICMPv6MLReport.mladdr%")
			res.append(packets.sprintf("%IPv6.src%"))
			res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf(" ICMPv6 "))
			res.append(packets.sprintf("%ICMPv6MLReport.type%"))
			res.append(packets.sprintf("%ICMPv6MLReport.code%"))
			res.append(packets.sprintf("%ICMPv6MLReport.mrd%"))
			res.append(packets.sprintf("%ICMPv6MLReport.mladdr%"))
        	elif not self.scan_type==2 and not self.scan_type==5 and not self.scan_type==3 and not self.scan_type==6 and not self.scan_type==7:
                	print packets.sprintf("%src% %IPv6.src% %IPv6.nh%")
			#res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf("%IPv6.src%"))
			if self.scan_type==1:
				res.append(packets.sprintf("%src%"))
			res.append(packets.sprintf("%IPv6.nh%"))
		if res:
			self.q.put(res)
version = '0.9'
# End of sniffer_process.py
