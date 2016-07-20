import requests
from mpd_test import mpd 
 


#filename = r'/Users/pataridus/python/input/export7_nano.csv'
filename = raw_input("Input file : ")
fd = open(filename,'rt')
#outfile = r'/Users/pataridus/python/output/output7_nano.csv'
outfile = raw_input("Output file : ")


fdout = open(outfile, 'wt')
lines = fd.readlines()
#header = 'id,title,url'
#fdout.write('id,title,url,status,runtime,audio,subtitle\n')
fdout.write('id,profile,url,status,runtime,audio,subtitle\n')



#start check row2 except header
for line in lines[1:]:
	items = line.strip().split(',')
	#print items[-1] = url
	
	

	#check array[2] in list = url column
	if requests.head(items[2]).status_code ==200:

		
		items.append('Found')

		if items[1] == 'Web':
		#if items[1] == 'Web' or items[1] == 'Android':	
   			print "Checking %s" % items[2]
   			obj = mpd(items[2])

   			#obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M(?P<secs>\d+)\.(?P<mil>\d+)S")
			obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M(?P<secs>\d+)")
			obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<minutes>\d+)M")
			obj.addDateTimePattern("PT(?P<hour>\d+)H")
			obj.addDateTimePattern("PT(?P<hour>\d+)H(?P<secs>\d+)")


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

	#items.append('1234')
	#items.append("\"EN,TH\"")
	#items.append("\"EN,TH\"")
	outstring = ','.join(items)
	fdout.write(outstring)
	fdout.write('\n')

#close(fdout)
#close(fd)

