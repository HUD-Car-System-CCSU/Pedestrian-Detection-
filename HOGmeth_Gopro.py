#opencv has histogram of oriented gradients (HOG)deteection built in
#sauce on the method and creators is
#@ https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf
#skip a frame ---- couldnt quite tell if it worked 
#brought in time to create a delay between frame scanning w/
# intention to increase
#resolution and decrease latency 
#as of 9/1/19 = program is set to scan 2/5 of frames 
#time delay removed 
#created logging system to record # of detection@time
#added feature to save image of detection for 
#logging false positives 
#================OTHER STUFF(s)============
#it does things that kind of work sometimes occasionally when it feels
#like it || encountered errors with HDMI cable & GoPro==  
#solution might be a new higher quality hdmi mini to stdsize adapter 
#as it is the only bit i cannot test rn
#
#When testing use batch file or shortcut so that the logging and pics 
#are contained in the folder "CarProject" <= on desktop
#backups on flashdrive && googledrive && phone
#
#^^Charles 9/2/19
#
# import the necessary packages

import numpy as np
import cv2
import datetime

#turn on/off logging
logging = "on" 
#created time element for data logging purposes
#see note under even more logging 
ctime= datetime.datetime.now()

#create log file && misc logging stuff
if logging == "on":
	logData = open("GoProLogFile.txt","w")
	numDet = 0
	logData.write("Logging enabled")
	logData.write("         \n")

#this space to launch arduino code for lane detection via IR
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# initialize the HOG detector prebuilt from openCV
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cv2.startWindowThread()

#more logging stuff
if logging == "on":
	logData.write("Detection initalized @  ")
	logData.write(str(datetime.datetime.now()))
	logData.write("         \n")

# initalize the gopro video stream
cap = cv2.VideoCapture(0)

# the output will be written to output.avi
out = cv2.VideoWriter(
    'output.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    15.,
    (720,480))
   #^^^^^^ oem val 640 480 15f 
   
# more logging stuff     
if logging == "on":
	logData.write("capture started @  ")
	logData.write(str(datetime.datetime.now()))
	logData.write("         \n")
framenum= 0   

while(True):
	
	while framenum < 2:
		x=0
	# Capture frame-by-frame
		ret, frame = cap.read()
    # if left alone||set past 720 LAG IS OD
		frame = cv2.resize(frame, (720, 480))
    # using a greyscale picture == faster detection
		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # detect people in the image
    # returns the bounding boxes for the detected objects
		boxes, weights = hog.detectMultiScale(frame, winStride=(8,8) )
		boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
		x=x+1
		for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
			cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
			#even more logging 
			if logging == "on":
				#first logs showed multiple detect at same time added
				#a time check help sort the data 
				newtime=datetime.datetime.now()
				ltd = ctime
				if newtime != ltd  :
					logData.write("Detection @  ")
					logData.write(str(datetime.datetime.now()))
					logData.write("         \n\n")
					ctime = datetime.datetime.now()
					cv2.imwrite("frame%d.jpg" %numDet, frame)
					numDet = numDet + 1
							
    #write the output video uint8 b/c opencv uses 8bit rgb pixel values
    #unsignedint8bit integer == uint8
		out.write(frame.astype('uint8'))

    # Display the resulting frame
		cv2.imshow('frame',frame)
		
		framenum = framenum + 1 
	#	print('Scanned <====') 
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	#frame 0 && 1 are skipped from processing but are still displayed to
	#allow a more smooth video output
	while framenum >= 2:
		#print('skipped')
		cv2.imshow('frame',frame)
		#time.sleep(.005)
		if framenum == 5:
			framenum = 0
		else:
			framenum = framenum +1
	
	#end the detection on ESC key ~~ for some reason it needs to run for about 15s+ before it works properly 
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
			if logging == "on":
				#i did this because it was being annoying & didnt 
				#feel like looking up why the .write would only allow 
				#one argument, it works but theres probably a better way
				res = ('Killed by User @ ' + str(datetime.datetime.now())+ '\n')
				ult = ('Total detections noted : '+ str(numDet))
				logData.write(str(res))
				logData.write(str(ult))
				
				
				
			break
#release the capture
cap.release()
#release the output
out.release()
#close the log && window
logData.close()
cv2.destroyAllWindows()
cv2.waitKey(1)
