#!/usr/bin/env python3

# Packet Decoder
# https://adventofcode.com/2021/day/16


class Bitstream:
	
	mask = [0x80, 0xc0, 0xe0, 0xf0, 0xf8, 0xfc, 0xfe, 0xff]
	
	def __init__(self, hex):
		self.bytes = bytes.fromhex(input)
		self.bits = 8
		self.index = 0
		self.current = self.bytes[self.index] if self.index < len(self.bytes) else 0
			
	def next(self, bits):
		result = 0
		while bits > 0:
			bits_to_read = min(bits, self.bits, 8)
			value = self.current & Bitstream.mask[bits_to_read-1]
			self.current <<= bits_to_read
			
			value >>= (8 - bits_to_read)
			result <<= bits_to_read
			result |= value
			
			bits -= bits_to_read
			self.bits -= bits_to_read
			if self.bits == 0:
				self.move_to_next_byte()
		return result
		
	def skip(self):
		if bits != 0:
			self.move_to_next_byte()
			
	def move_to_next_byte(self):
			self.bits = 8
			self.index += 1
			self.current = self.bytes[self.index] if self.index < len(self.bytes) else 0		
		
	def __repr__(self):
		return f"{hex(self.current)} + " + f"{self.bytes[self.index+1:]}"
	
		
class Packets:
	
	def __init__(self, bitstream):
		self.bitstream = bitstream
		
	def next_packet(self):
		version, type_id = self.get_header()
		if type_id == 4:
			literal, bit_length = self.get_literal()
			return (version, type_id, literal), bit_length + 6
		else:
			subpackets, bit_length = self.get_subpackets()
			return (version, type_id, subpackets), bit_length + 6
		
	def get_header(self):
		version = self.bitstream.next(3)
		type_id = self.bitstream.next(3)
		return version, type_id
		
	def get_literal(self):
		literal = 0
		bit_length = 0
		while True:
			bit_length += 5
			next_nibble = self.bitstream.next(5)
			literal <<= 4
			literal |= (next_nibble & 0xf)
			if next_nibble & 0x10 == 0:
				break
		return literal, bit_length
		
	def get_subpackets(self):
		subpackets = []
		bit_length = 0
		length_type = self.bitstream.next(1)
		if length_type == 0:
			length = self.bitstream.next(15)
			while length > 0:
				packet, packet_bits = self.next_packet()
				subpackets.append(packet)
				bit_length += packet_bits
				length -= packet_bits
		else:
			num_packets = self.bitstream.next(11)
			while num_packets > 0:
				packet, packet_bits = self.next_packet()
				subpackets.append(packet)
				bit_length += packet_bits
				num_packets -= 1
		return subpackets, bit_length
			

def read_file(name):
	file = open(name)
	return [line.strip() for line in file.readlines()]


def sum_of_versions(packet):
	version_sum = packet[0]
	if not isinstance(packet[2], list):
		return version_sum
	
	for subpacket in packet[2]:
		version_sum += sum_of_versions(subpacket)
	return version_sum
		

input = read_file("input.txt")[0]
bits = Bitstream(input)
packets = Packets(bits)
packet, _ = packets.next_packet()

result = sum_of_versions(packet)
print(f"Part 1: {result}")

