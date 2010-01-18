
class message(object):
	def __init__(self,str,debug=False):
		self._line = str.rstrip()
		self._parts = self._line.split(' ',4)
		
		if self._parts[0]=='PING':
			self.type = 'PING'
			self.src = self._parts[1][1:]
			return
		if self._parts[0]=='PONG':
			self.type = 'PONG'
			self.src = self._parts[1][1:]
			return
		if self._parts[0]=='ERROR':
			self.type = 'ERROR'
			return
		if self._parts[1]=='PRIVMSG':
			self.type = 'PRIVMSG'
			self.src = self._parts[0][1:]
			self.dst = self._parts[2]
			self.msg = self._parts[3:]
			return
		if self._parts[1]=='NOTICE':
			self.type = 'NOTICE'
			self.src = self._parts[0][1:]
			self.dst = self._parts[2]
			self.msg = self._parts[3:]
			return
		if self._parts[1]=='JOIN':
			self.type = 'JOIN'
			self.user = self._parts[0][1:]
			self.channel = self._parts[2]
			return
		if self._parts[1]=='PART':
			self.type = 'PART'
			self.user = self._parts[0][1:]
			self.channel = self._parts[2]
			return
		if self._parts[1]=='MODE':
			self.type = 'MODE'
			return
		if self._parts[1]=='NICK':
			self.type = 'NICK'
			return
		self.type = 'UNKNOWN'
		if debug: raise Exception(line)
	def __repr__(self):
		return '<irc:%s>'%self.type
	def __getitem__(self,items):
		'''
		Wrap around self._parts to maintain compatibility with old dict message
		'''
		return self._parts[items]
	def __str__(self):
		'''
		Wrap around self._parts to maintain compatibility with old dict message
		'''
		return str(self._parts)
	def __len__(self):
		'''
		Wrap around self._parts to maintain compatibility with old dict message
		'''
		return len(self._parts)
	def debug(self):
		print repr(self)
		for key,data in self.__dict__.iteritems():
			print '\t',key,'->',data
		print

if __name__ == '__main__':
	f = open('../test.log','r')
	for line in f.readlines():
		message(line,True).debug()
