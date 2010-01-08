from purplebot.bot import CommandError
from plugins.kfdm._rpc import call_rpc as _call_rpc

def report_request(bot,hostmask,line):
	_report_item(bot,hostmask,line,'request')
report_request.command = '.request'
report_request.example = '.request I would like to request this'
report_request.thread = True

def report_bug(bot,hostmask,line):
	_report_item(bot,hostmask,line,'bug')
report_bug.command = '.bug'
report_bug.example = '.bug I found this bug'
report_bug.thread = True

def _report_item(bot,hostmask,line,type):
	url			= bot.setting_get('BugPlugin::SubmitURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	print 'in _report_item %s %s %s'%(hostmask,line,type)
	
	if len(line[4]) > 100:
		short = line[4][:100]
		long = line[4]+'\nreported by '+hostmask['nick']
	else:
		short = line[4]
		long = 'reported by '+hostmask['nick']
	
	response = _call_rpc(url,{
		'username':user,
		'password':password,
		'short':short,
		'long':long,
		'type':type,
	})
	try: bot.irc_notice(hostmask['nick'],'Added %s as %d - %s'%(type,response['id'],response['url']))
	except KeyError: raise CommandError('Error decoding response')
	