import simplejson
import urllib, urllib2
from purplebot.bot import CommandError

__handler = urllib2.HTTPHandler()
__opener = urllib2.build_opener(__handler)
__opener.addheaders = [('X-Requested-With','XMLHttpRequest')]
urllib2.install_opener(__opener)

def call_rpc(url,params):
	try:
		api_params	= urllib.urlencode(params)
		api_call = urllib2.urlopen(url, api_params)
		response = api_call.read()
		response = simplejson.loads(response)
	except ValueError:
		raise CommandError('Error reading response')
	except urllib2.URLError:
		raise CommandError('Error opening '+url)
	try:
		if response['result'] == 'OK': return response
		raise CommandError(response['result'])
	except KeyError:
		print response
		raise CommandError('Error reading response key')