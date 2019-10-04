from PIL import Image, ImageOps
#take frame in and chop it up
#pixel points are static here but will be dynamic in final
#current takes image(frame) gets the size flips the left and right 
#and recombines the image
#center is comment out b/c it doesnt need to be modified 
image = Image.open('gtr.jpg')
#get the size
width, height = image.size

print (width)
print (height)

Lbox = (0,0,426,720)
Lframe1 = image.crop(Lbox)
#Lframe1.show()

#Cbox = (426,0,753.34,720)
#Cframe = image.crop(Cbox)
#Cframe.show()

Rbox = (852,0,1280,720)
Rframe1 = image.crop(Rbox)
#Rframe1.show()

#run the HOG meth on Lbox&&Rbox
#send out the frame back out modified & pplboxed
#ScannedL & Cframe & ScannedR; merge the 3 together
#might have to be a new image
SL = ImageOps.flip(Lframe1)
SR = ImageOps.flip(Rframe1)
image.paste(SL,Lbox)
image.paste(SR,Rbox)
image.show()


#pedest time stamps
#5.29 ----- 6.04
#9.19 ----- 9.39

#lane 
#0.45 ----- 1.15
