import SocketServer
import re

from kfdm.gntp import gntp

bot_instance = None
server_instance = None

class GNTPServer(SocketServer.ThreadingTCPServer):
	pass

class GNTPHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024)
		if re.match('GNTP/1.0 REGISTER', self.data):
			_debug("%s sent REGISTER:" % self.client_address[0])
			tmp = gntp.GNTPRegister(self.data)
			_register_notification(tmp)
		elif re.match('GNTP/1.0 NOTIFY', self.data):
			_debug("%s sent NOTIFY:" % self.client_address[0])
			tmp = gntp.GNTPNotice(self.data)
			_send_notification(tmp)
		else:
			_debug("%s sent UNKNOWN:" % self.client_address[0])
			_debug('----')
			_debug(self.data)
			_debug('----')

def load(bot):
	global bot_instance
	global server_instance
	bot.debug('Launching growl server')
	bot_instance = bot
	if server_instance == None:
		host = bot.setting_get('gntp::host','')
		port = bot.setting_get('gntp::port',23053)
		try:
			server_instance = GNTPServer((host,port), GNTPHandler)
			server_instance.serve_forever()
		except Exception,e:
			bot.debug('Error creating growl server')
			bot.debug(e)
			server_instance = None
	
def unload(bot):
	bot_instance = None
	#server_instance = None #Kill the server

def _debug(msg):
	global bot_instance
	if bot_instance:
		bot_instance.debug(msg)

def _register_notification(register):
	print register.__unicode__()

def _send_notification(notice):
	global bot_instance
	print notice.__unicode__()
	if bot_instance:
		bot_instance.irc_privmsg('#japanese','%s - %s - %s - %s'%(
			notice.parsed['Application-Name'],
			notice.parsed['Notification-Name'],					
			notice.parsed['Notification-Title'],
			notice.parsed['Notification-Text']
		))

def growl_register(bot,hostmask,line):
	pass

def growl_unregister(bot,hostmask,line):
	pass
