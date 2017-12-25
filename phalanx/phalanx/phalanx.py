#!/usr/bin/env python
# Phalanx
# Developed by acidvegas in Python
# https://github.com/acidvegas/trollbots
# phalanx.py

import random
import socket
import string
import threading
import time

# Connection
server    = 'localhost'
port      = 6667
channel   = '#phalanx'
key       = 'CHANGEME'

# Settings
admin     = 'user@host'
clones    = 1000
oper_pass = 'CHANGEME'

def debug(msg)           : print(f'{get_time()} | [~] - {msg}')
def error(msg, reason)   : print(f'{get_time()} | [!] - {msg} ({reason})')
def get_time()           : return time.strftime('%I:%M:%S')
def random_int(min, max) : return random.randint(min, max)
def random_str(size)     : return ''.join(random.sample((string.ascii_letters), size))

class clone(threading.Thread):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		threading.Thread.__init__(self)

	def run(self):
		self.connect()

	def connect(self):
		try:
			self.sock.connect((server, port))
			self.raw('USER {0} 0 * :{1}'.format(random_str(random_int(4,9)), random_str(random_int(4,9))))
			self.raw('NICK ' + random_str(random_int(4,9)))
		except socket.error as ex:
			error('Failed to connect to IRC server.', ex)
			self.event_disconnect()
		else:
			self.listen()

	def event_disconnect(self):
		self.sock.close()
		time.sleep(random_int(3,5))
		self.connect()

	def event_message(self, ident, msg):
		if ident == admin and msg.startswith('!'):
			if msg == '!recycle':
				self.raw('NICK '     + random_str(random_int(4,9)))
				self.raw('SETHOST '  + random_str(random_int(4,9)))
				self.raw('SETIDENT ' + random_str(random_int(4,9)))
				self.raw('SETNAME '  + random_str(random_int(4,9)))
			elif msg.startswith('!attack') and len(msg.split()) == 2:
				target = msg.split()[1]
				self.raw(f'PRIVMSG {target} :' + random_str(random_int(4,9)))
				self.raw(f'SAJOIN {target} '   + random_str(random_int(4,9)))
			else:
				self.raw(msg[1:])

	def handle_events(self, data):
		args = data.split()
		if data.startswith('ERROR :Closing Link:') : raise Exception('Connection has closed.')
		elif args[0] == 'PING' : self.raw('PONG ' + args[1][1:])
		elif args[1] == '001'  : self.raw('OPER phalanx ' + oper_pass)
		elif args[1] == '381'  : self.raw('SETHOST ' + random_str(random_int(5,10)))
		elif args[1] == '396'  : self.raw(f'JOIN {channel} {key}')
		elif args[1] == '433'  : self.raw('NICK ' + random_str(random_int(5,6)))
		elif args[1] == 'PRIVMSG':
			try:
				ident = args[0].split('!')[1]
				msg   = data.split(f'{args[0]} PRIVMSG {args[2]} :')[1]
				self.event_message(ident, msg)
			except : pass

	def listen(self):
		while True:
			try:
				data = self.sock.recv(1024).decode('utf-8')
				for line in (line for line in data.split('\r\n') if line):
					if len(line.split()) >= 2:
						self.handle_events(line)
			except (UnicodeDecodeError,UnicodeEncodeError):
				pass
			except Exception as ex:
				error('Unexpected error occured.', ex)
				break
		self.event_disconnect()

	def raw(self, msg):
		self.sock.send(bytes(msg + '\r\n', 'utf-8'))

# Main
for i in range(clones):
	clone().start()
	time.sleep(1)
debug('All clones have been loaded!')
while True:
	input('')