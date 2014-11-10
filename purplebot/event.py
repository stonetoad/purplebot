import logging
import collections

__all__ = ['EventDelegate']

logger = logging.getLogger(__name__)


class EventDelegate(object):
	def __init__(self, bot):
		self.__events = collections.defaultdict(list)
		self.bot = bot

	def __call__(self, event_name, *args):
		'''Run events on named queue
		:param event_name: Examples PRIVMSG, CONNECT, JOIN
		:type event_name: str
		:param param: Parameters to send to the registered functions. Varies from
		event to event
		'''
		if event_name in self.__events:
			for event in self.__events[event_name]:
				logger.debug('%s | %s', event_name, args)
				event(self.bot, *args)
		else:
			logger.debug('No events found for: %s', event_name)

	def register(self, event_name, function):
		"""Register a new event
		:param event_name: Examples PRIVMSG, CONNECT, JOIN
		:type event_name: str
		:param function: function to be called. Order is not guarenteed
		:type function: func
		"""
		event_name = event_name.upper()
		logger.debug('Registering %s as %s', function, event_name)
		self.__events[event_name].append(function)

	def unregister(self, event_name, function):
		"""Unregister an event

		:param event_name: Examples PRIVMSG, CONNECT, JOIN
		:type event_name: str
		:param function: function to be unregistered
		:type function: func
		"""
		event_name = event_name.upper()
		logger.debug('Unregistering %s from %s', function, event_name)
		if event_name in self.__events:
			self.__events[event_name].remove(function)
