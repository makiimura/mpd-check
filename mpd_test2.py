import requests
from xml.dom.minidom import parseString
from datetime import datetime

class mpd(object):
	
	def __init__(self, url):
		self.url = url
		self.mediaPresentationDuration = None
		self.audios = list()
		self.video = None
		self.subtitles = list()
		self.datetimePatterns = list()

	def parse(self):
		# load mpd from url
		response = requests.get(self.url)
		if response.status_code != 200:
			return False


		root = parseString(response.content)

		# get mediaPresentationDuration
		mpd = root.getElementsByTagName('MPD')[0]
		temp = str(mpd.attributes['mediaPresentationDuration'].value)
		self.mediaPresentationDuration = self.convertTime(temp)

		#get video
		adaptationsets = mpd.getElementsByTagName('AdaptationSet')
		for ad in adaptationsets:
			if ad.hasAttribute('contentType') and ad.getAttribute('contentType') == 'video':
				self.video = video(ad)
			elif ad.hasAttribute('contentType') and ad.getAttribute('contentType') == 'audio':
				self.audios.append(audio(ad))
			elif ad.hasAttribute('mimeType') and ad.getAttribute('mimeType') == 'text/vtt':
				self.subtitles.append(subtitle(ad))


		return True

	'''
	def convertTime(self, runtime):
			try: 
				d = datetime.strptime(runtime, "PT%HH%MM%S.%fS")
				return (d.hour*3600)+(d.minute*60)+(d.second)
			except ValueError:
				return 0
	'''
	def addDateTimePattern(self, pattern):
		self.addDateTimePattern.append(re.compile(pattern))
	def convertTime(self, runtime):
		m = None
		for r in self.datetimePatterns:
			m = r.match(runtime)
			if m:
				break

		# Check if we cannot match any of our format
		# Just return 0
		if not m:
			return 0
		# Get hour/minutes/second from 'm' object by group name

		# Need to check if there is a group or not. if not use 0
		# For example:
		# PT01H30M will don't have 'secs' group, so we will use 0 for secods
		h = 0
		m = 0
		s = 0
		ms = 0
		if 'hour' in m.groupdict().keys():
			h = m.group('hour')

		if 'minutes' in m.groupdict().keys():
			m = m.group('minutes')

		if 'secs' in m.groupdict().keys():
			s = m.group('secs')


		return (h*3600) + (m*60) + s

obj = mpd(‘someurl’)

#add pattern
obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M(?P<secs>\d+)\.(?P<mil>\d+)S")
obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M")
obj.addDateTimePattern("PT(?P<hour>\d+)H")
obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<secs>\d+)\.(?P<mil>\d+)S")



# parsing manifest
obj.parse()


class subtitle(object):

	def __init__(self, element):
		if element.getAttribute('mimeType') != 'text/vtt':
			raise ValueError

		self.mimeType = element.getAttribute('mimeType')
		self.lang = element.getAttribute('lang')


class video(object):

	def __init__(self, element):
		if element.getAttribute('contentType') != 'video':
			raise ValueError

		self.lang = element.getAttribute('lang')
		self.maxBandwidth = int(element.getAttribute('maxBandwidth'))
		self.minBandwidth = int(element.getAttribute('minBandwidth'))
		self.frameRate = element.getAttribute('frameRate')
		self.codec = element.getAttribute('codecs')
		self.mimeType = element.getAttribute('mimeType')


class audio(object):
	def __init__(self, element):
		if element.getAttribute('contentType') != 'audio':
			raise ValueError

		self.lang = element.getAttribute('lang')
		self.minBandwidth = int(element.getAttribute('minBandwidth'))
		self.maxBandwidth = int(element.getAttribute('maxBandwidth'))
		self.samplingRate = int(element.getAttribute('audioSamplingRate'))
		self.codec = element.getAttribute('codecs')
		self.paint = 'hello'
		self.mimeType = element.getAttribute('mimeType')



'''
def test():
	test_url = r'http://cdn.goprimetime.info/video/1/A534e59000080/0/Manifest-wh.mpd'
	obj = mpd(test_url)
	if obj.parse():
		print "------ Video -----"
		print "Duration : %d" % obj.mediaPresentationDuration
		#print obj.video.codec
		#print obj.video.maxBandwidth
		#print obj.video.minBandwidth
		#print obj.video.frameRate
		#print obj.video.mimeType
		print "------ Audio -----"
		for audio in obj.audios:
			print audio.lang
			#print audio.minBandwidth
			#print audio.maxBandwidth
			#print audio.codec
			#print audio.mimeType
			#print audio.paint
			#print ""

		print "----- Subtitles -----"
		for sub in obj.subtitles:
			print sub.lang
			#print sub.mimeType
			#print ""
	else:
		print "Manifest not found"		



if __name__=='__main__':
	test()
'''



