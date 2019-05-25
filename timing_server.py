#!/usr/bin/python

from __future__ import print_function
import time, argparse, socket

parser = argparse.ArgumentParser()
parser.add_argument("--server", action="store_true")
parser.add_argument("--peer-host", type=str)
parser.add_argument("--peer-port", type=int)
parser.add_argument("--bind-port", type=int)

class Main:
	def __init__(self, args):
		self.args = args
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(("0.0.0.0", args.bind_port))

	def get_packet(self):
		data, addr = self.sock.recvfrom(1024)
		return data

	def send(self, message):
		self.sock.sendto(message, (self.args.peer_host, self.args.peer_port))

	def launch_server(self):
		while True:
			data = self.get_packet()
			now = time.time()
			self.send("%r" % (now,))

	def launch_client(self):
		def do_round_trip():
			start_now = time.time()
			self.send("ping")
			reply = self.get_packet()
			round_trip_now = time.time()
			their_time = float(reply)
			round_trip_time = round_trip_now - start_now
			assumed_time_of_receipt = 0.5 * round_trip_time + start_now
			time_delta = their_time - assumed_time_of_receipt
			print("RTT: %.4fms  -- Time delta: %.4fms" % (1e3 * round_trip_time, 1e3 * time_delta))
		while True:
			do_round_trip()
			time.sleep(1)

if __name__ == "__main__":
	args = parser.parse_args()
	print("Args:", args)
	m = Main(args)
	if args.server:
		m.launch_server()
	else:
		m.launch_client()

