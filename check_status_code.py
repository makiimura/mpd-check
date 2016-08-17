import requests
from mpd_test import mpd 
from tabulate import tabulate
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--in', action="store", dest='inputFileName')
parser.add_argument('--out', action='store', dest='outputFileName')
 
arguments = parser.parse_args()
#print arguments.inputFileName
#print arguments.outputFileName
 
filename = arguments.inputFileName
fd = open(filename,'rt')

outfile = arguments.outputFileName


#filename = r'/Users/pataridus/python/input/export7_nano.csv'
#--> filename = raw_input("Input file : ")
#--> fd = open(filename,'rt')
#outfile = r'/Users/pataridus/python/output/output7_nano.csv'
#--> outfile = raw_input("Output file : ")


fdout = open(outfile, 'wt')
lines = fd.readlines()


#header = 'id,title,url'
#fdout.write('id,title,url,status,runtime,audio,subtitle\n')
fdout.write('id,profile,url,status,runtime,audio,subtitle\n')

count_f = {"apple_tv": 0, "hls_3g": 0, "hls_wifi": 0, "tv": 0, "web": 0, "mobile_3g": 0, "mobile": 0, "android_3g": 0, "android": 0, "chromecast": 0, "cth_live_1": 0, "comigo": 0, "nano": 0, "est_download": 0, "temp_download": 0, "samsung_tv": 0} 
count_nf = {"apple_tv": 0, "hls_3g": 0, "hls_wifi": 0, "tv": 0, "web": 0, "mobile_3g": 0, "mobile": 0, "android_3g": 0, "android": 0, "chromecast": 0, "cth_live_1": 0, "comigo": 0, "nano": 0, "est_download": 0, "temp_download": 0, "samsung_tv": 0} 


#start check row2 except header
for line in lines[1:]:
	items = line.strip().split(',')
	#print items[-1] = url
	
	
	print "Checking.. %s" % items[2]

	#print "Not Found : %d" % count_nf["apple_tv"] + count_nf["hls_3g"] + count_nf["hls_wifi"] + count_nf["tv"] + count_nf["web"] + count_nf["mobile_3g"] + count_nf["mobile"] + count_nf["android_3g"] + count_nf["android"] + count_nf["chromecast"] + count_nf["cth_live_1"] + count_nf["comigo"]	+ count_nf["nano"] + count_nf["est_download"] + count_nf["temp_download"] + count_nf["samsung_tv"]
	#print "Found : %d" % count_f["apple_tv"] + count_f["hls_3g"] + count_f["hls_wifi"] + count_f["tv"] + count_f["web"] + count_f["mobile_3g"] + count_f["mobile"] + count_f["android_3g"] + count_f["android"] + count_f["chromecast"] + count_f["cth_live_1"] + count_f["comigo"]	+ count_f["nano"] + count_f["est_download"] + count_f["temp_download"] + count_f["samsung_tv"]
	#check array[2] in list = url column
	if requests.head(items[2]).status_code ==200:

		
		items.append('Found')

		if items[1] == 'Apple TV':
			#countf_aptv += 1
			count_f["apple_tv"] +=1
		elif items[1] == 'HLS 3G':
			count_f["hls_3g"] +=1
		elif items[1] == 'HLS WIFI':
			count_f["hls_wifi"] +=1
		elif items[1] == 'TV' :
			count_f["tv"] +=1
		elif items[1] == 'Mobile 3G' :
			count_f["mobile_3g"] +=1
		elif items[1] == 'Mobile' :
			count_f["mobile"] +=1
		elif items[1] == 'Android 3G' :
			count_f["android_3g"] +=1
		elif items[1] == 'Android' :
			count_f["android"] +=1
		elif items[1] == 'ChromeCast' :
			count_f["chromecast"] +=1
		elif items[1] == 'CTH Live 1' :
			count_f["cth_live_1"] +=1
		elif items[1] == 'Comigo' :
			count_f["comigo"] +=1
		elif items[1] == 'Nano' :
			count_f["nano"] +=1
		elif items[1] == 'EST Download' :
			count_f["est_download"] +=1
		elif items[1] == 'Temp Download' :
			count_f["temp_download"] +=1
		elif items[1] == 'Samsung TV' :	
			count_f["samsung_tv"] +=1

		elif items[1] == 'Web':
			count_f["web"] +=1
		#if items[1] == 'Web' or items[1] == 'Android':	
   			#print "Checking %s" % items[2]
   			obj = mpd(items[2])

   			#obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M(?P<secs>\d+)\.(?P<mil>\d+)S")
			obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M(?P<secs>\d+)")
			obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M")
			obj.addDateTimePattern("PT(?P<hour>\d+)H")
			obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<secs>\d+)")
			obj.addDateTimePattern("PT(?P<minutes>\d+)M(?P<secs>\d+)")


   			obj.parse()
   			items.append(str(obj.mediaPresentationDuration))

   			temp_arr_audio = []
   			for audio in obj.audios:
   				temp_arr_audio.append(audio.lang)
   			temp_str_audio = ','.join(sorted(temp_arr_audio))
   			items.append("\"%s\"" %temp_str_audio.upper())

   			temp_arr_subs = []
			for sub in obj.subtitles:
				temp_arr_subs.append(sub.lang)
			temp_str_subs = ','.join(sorted(temp_arr_subs))
   			items.append("\"%s\""%temp_str_subs.upper())
		else:
   			items.append('--')




		#print items[1] + '[OK]'
	else:
		items.append('Not Found')
		#print items[1] + ' [Not Found]'

		if items[1] == 'Apple TV':
			#countf_aptv += 1
			count_nf["apple_tv"] +=1
		elif items[1] == 'HLS 3G':
			count_nf["hls_3g"] +=1
		elif items[1] == 'HLS WIFI':
			count_nf["hls_wifi"] +=1
		elif items[1] == 'TV' :
			count_nf["tv"] +=1
		elif items[1] == 'Mobile 3G' :
			count_nf["mobile_3g"] +=1
		elif items[1] == 'Mobile' :
			count_nf["mobile"] +=1
		elif items[1] == 'Android 3G' :
			count_nf["android_3g"] +=1
		elif items[1] == 'Android' :
			count_nf["android"] +=1
		elif items[1] == 'ChromeCast' :
			count_nf["chromecast"] +=1
		elif items[1] == 'CTH Live 1' :
			count_nf["cth_live_1"] +=1
		elif items[1] == 'Comigo' :
			count_nf["comigo"] +=1
		elif items[1] == 'Nano' :
			count_nf["nano"] +=1
		elif items[1] == 'EST Download' :
			count_nf["est_download"] +=1
		elif items[1] == 'Temp Download' :
			count_nf["temp_download"] +=1
		elif items[1] == 'Samsung TV' :	
			count_nf["samsung_tv"] +=1
		elif items[1] == 'Web':
			count_f["web"] +=1

	#items.append('1234')
	#items.append("\"EN,TH\"")
	#items.append("\"EN,TH\"")
	outstring = ','.join(items)
	fdout.write(outstring)
	fdout.write('\n')

print "----------------------------------------"
#print tabulate([['Apple tv', count_nf["apple_tv"], count_f["apple_tv"]], ['HLS 3G', count_nf["hls_3g"], count_f["hls_3g"]]], headers=['Profile', 'Found', 'Not Found'], tablefmt='orgtbl')
print tabulate([['Apple TV', count_nf["apple_tv"], count_f["apple_tv"]], ['HLS 3G', count_nf["hls_3g"], count_f["hls_3g"]], ['HLS WIFI', count_nf["hls_wifi"], count_f["hls_wifi"]], ['TV', count_nf["tv"], count_f["tv"]], ['Web', count_nf["web"], count_f["web"]], ['Mobile 3G', count_nf["mobile_3g"], count_f["mobile_3g"]], ['Mobile', count_nf["mobile"], count_f["mobile"]], ['Android 3G', count_nf["android_3g"], count_f["android_3g"]], ['Android', count_nf["android"], count_f["android"]], ['ChromeCast', count_nf["chromecast"], count_f["chromecast"]], ['CTH Live 1', count_nf["cth_live_1"], count_f["cth_live_1"]], ['Comigo', count_nf["comigo"], count_f["comigo"]], ['Nano', count_nf["nano"], count_f["nano"]], ['EST Download', count_nf["est_download"], count_f["est_download"]], ['Temp Download', count_nf["temp_download"], count_f["temp_download"]], ['Samsung TV', count_nf["samsung_tv"], count_f["samsung_tv"]]], headers=['Profile', 'Found', 'Not Found'], tablefmt='orgtbl')

print "----------------------------------------"
print "All : %d" % (sum(count_f.values()) + sum(count_nf.values()))
print "Found : %d" % sum(count_f.values())
print "Not Found : %d" % sum(count_nf.values())

'''
if count_nf[items[1]] > 0
print items[1]
'''
#close(fdout)
#close(fd)

