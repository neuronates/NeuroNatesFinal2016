#!usr/bin/python

from multiprocessing import Process
import spiTest
import picamera
from subprocess import call, check_call, PIPE, Popen
import time
import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(18,GPIO.OUT)

#GPIO.output(18,GPIO.HIGH)

#from subprocess import check_call

with open('patientData.txt','r') as f:
    data=f.read()
name = data.split('\n')
print name
if(name[-1] == ''):
	name[-1] = 'testName'
nameh264 = 'videos/' + name[-1] + ".h264"
namemp4 = 'videos/' + name[-1] + ".mp4"


with picamera.PiCamera() as camera:
	
	try:
		time = 15
		print 'start'
		#Initialize concurrent processes
 #		camera.wait_recording(time)
		p1 = Process(target = camera.wait_recording, args = (time,))
		print 'before'
		p2 = Process(target = spiTest.spiTestRun, args = (name[-1],))#execfile("spiTest.py"))
		print 'after'
		camera.resolution = (800, 480)
		camera.framerate = 30
		camera.start_preview()
		
		#=============================================
		# Comment out the lines between the other set of ========
		# Uncommen the lines below
		# That should correct for the delay in video monitoring and eeg recording
#		p2.start()
#		time.sleep(6)
#		camera.start_recording(nameh264)
		#=============================================
		
		#============================================
		camera.start_recording(nameh264)
		p2.start()
		#=============================================
		
		camera.wait_recording(time)
		#Process(target = spiTest).start()
		##Process(target = camera.wait_recording, args = (time,)).start()
		#print 'wait recording'
		#print type(spiTest.spiTestRun)
		#p1.start()
		#p2.start()
		camera.stop_recording()
		p2.terminate()	
		print 'recording stopped'
		
		# essentially, you need a bash script that
		# concatenates all files that match window_*.txt
		# cat ls -tr window_*.txt > [patientname].txt
		# then delete all files that match window_*.txt (rm data/window_*.txt)
	
	except KeyboardInterrupt:
		print 'Stopped by Keyboard'
		camera.stop_recording()
		p2.terminate()	

#GPIO.output(18,GPIO.LOW)


concat_files_0 = "cat window_*_montage_0.txt > " + name[-1] + "_0.txt"
concat_files_1 = "cat window_*_montage_1.txt > " + name[-1] + "_1.txt"
concat_files_2 = "cat window_*_montage_2.txt > " + name[-1] + "_2.txt"
concat_files_3 = "cat window_*_montage_3.txt > " + name[-1] + "_3.txt"
concat_files_4 = "cat window_*_montage_4.txt > " + name[-1] + "_4.txt"
concat_files_5 = "cat window_*_montage_5.txt > " + name[-1] + "_5.txt"
concat_files_6 = "cat window_*_montage_6.txt > " + name[-1] + "_6.txt"
concat_files_7 = "cat window_*_montage_7.txt > " + name[-1] + "_7.txt"
concat_files_8 = "cat window_*_montage_8.txt > " + name[-1] + "_8.txt"
concat_files_9 = "cat window_*_montage_9.txt > " + name[-1] + "_9.txt"
concat_files_10 = "cat window_*_montage_10.txt > " + name[-1] + "_10.txt"
concat_files_11 = "cat window_*_montage_11.txt > " + name[-1] + "_11.txt"

concat_files_seiz = "cat window_*_seizure_results.txt > " + name[-1] + "_seiz.txt"

d = "/home/pi/algorithm/UI/data"

p1 = Popen(["ls", "-tr"], cwd=d,stdout=PIPE)
p2 = Popen(concat_files_0 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_1 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_2 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_3 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_4 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_5 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_6 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_7 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_8 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_9 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_10 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_11 ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

p2 = Popen(concat_files_seiz ,shell=True, cwd = d, stdin=p1.stdout,stdout=PIPE)
p2.communicate()[0]

remove_files = "rm window_*.txt"

#call([concat_files], cwd=d, shell = True)
#call()
#check_call(["ls","-tr","|","cat","window_*.txt",">",txtName], cwd=d)
call(["rm window_*.txt"], shell = True, cwd=d)

convert_video = "MP4Box -fps 30 -add " + nameh264 + " " + namemp4 
delete_video = "rm " + nameh264
call([convert_video], shell = True)
call([delete_video], shell = True)
