
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib.request, urllib.error
import smtplib
import inspect
from Site import Site

import private_sites

def sendWarning(site: Site, status: int):
	host = config('SMTP_HOST')
	port = config('SMTP_PORT')
	username = config('SMTP_USERNAME')
	password = config('SMTP_PASSWORD')
	sender = config('EMAIL_FROM')
	receivers = config('EMAIL_TO')

	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receivers
	msg['Subject'] = 'System Alert: %s - %s status' % (site.name, status)

	body = """
	Alert! Unexpected status from %s.
	URL: %s
	Response Status: %s
	Expected Status: %s
	""" % (site.name, site.url, status, site.expectedStatus)
	msg.attach(MIMEText(body))

	try:
		server = smtplib.SMTP_SSL(host, port)
		server.ehlo()
		server.login(username, password)
		server.sendmail(sender, receivers, msg.as_string())
		server.close()
		print('Donezo!')
	except Exception as e:
		print('whaaaaat')
		print(e)


sitesToCheck = private_sites.exports

for site in sitesToCheck:
	try:
		res = urllib.request.urlopen(site.url)
		status = res.status
	except urllib.error.HTTPError as err:
		status = err.code
	print(status)
	if status != site.expectedStatus:
		print('uh oh')
		sendWarning(site, status)
