import cv2
import math 
import os
import sys
from PIL import Image
from PIL import ImageChops
import numpy

from target import *

cascPath = "haarcascade_frontalface_default.xml"

def shift_resize_images(target_frames, name, output_scale):

	#find the largest face height/width and scale all other faces

	largest_target_width = 0
	largest_target_height = 0
	for target in target_frames:
		if(target.w > largest_target_width):
			largest_target_width = target.w
		if(target.h > largest_target_height):
			largest_target_height = target.h

	# scale up images to match largest face (pixel-pixel wise)
	# (this is so all targets are the same size, and we dont lose resolution from downsizing larger images) 
	for target in target_frames:
		#set new image height and width so we can match face's pixel height/width
		scaleW = largest_target_width / target.w
		scaleH = largest_target_height / target.h
		newImageW = int(scaleW*target.imageW)
		newImageH = int(scaleH*target.imageH)
		target.scale_image(newImageW, newImageH)
		#resize image
		target.PILimage = target.PILimage.resize((target.imageW, target.imageH))

		"""
		# for debugging: use cv2 with face rectangles so we can see
		img = face.PILimage
		open_cv_image = numpy.array(img) 
		open_cv_image = open_cv_image[:, :, ::-1].copy() 
		#rectangle marking face
		cv2.rectangle(open_cv_image, (face.x, face.y), (face.x+face.w, face.y+face.h), (0, 255, 0), 2)
		#line marking error
		cv2.line(open_cv_image, (int(face.imageW/2), int(face.imageH/2)), 
			(int((face.x+face.x+face.w)/2),int((face.y+face.y+face.h)/2)), (0, 255, 0), 4)
		cv2.imshow("Face found", open_cv_image)
		cv2.waitKey(0)
		"""

	#scale outwards by specified amount so we can see more of the subject
	final_width = target_frames[0].w*output_scale[0]
	final_height = target_frames[0].h*output_scale[1]

	#position faces to the center of image and then
	#paste images onto black background 
	for target in target_frames:
		background = Image.new('RGB', (final_width, final_height), (0, 0, 0))

		#offset the image to have the face centered in new, larger image
		offset = (int((final_width-target.imageW)/2+target.xErr),
			int((final_height-target.imageH)/2+target.yErr))
		
		background.paste(target.PILimage, offset)
		target.PILimage = background

		"""
		#convert to cv image so we can see
		open_cv_image = numpy.array(background) 
		open_cv_image = open_cv_image[:, :, ::-1].copy()
		cv2.imshow("Face found", open_cv_image)
		cv2.waitKey(0)
		"""

	video=cv2.VideoWriter(f'video_{name}.avi',0,30,(final_width,final_height))

	for target in target_frames:
		open_cv_image = numpy.array(target.PILimage) 
		open_cv_image = open_cv_image[:, :, ::-1].copy()
		# cv2.imshow("Face found", open_cv_image)
		# cv2.waitKey(0)
		video.write(open_cv_image)

	cv2.destroyAllWindows()
	video.release()



def parse_video(path, entity_movement_threshold):
	# files = os.listdir(imagesPath)
	# files = [file for file in files if "jpg" in file]
	# files.sort(key=lambda x:int(x[5:][:-4])) #"frame###.jpg" sorts by number
	# print(files)
		
	frames = []
	
	vidcap = cv2.VideoCapture(path)
	success,image = vidcap.read()
	count = 1
	while success:
		frames.append(image)
		success,image = vidcap.read()
		count += 1

	# Create the haar cascade
	cascade = cv2.CascadeClassifier(cascPath)
	detected_entities = []

	frame = 0

	for image in frames:

		# Read the image
		# image = cv2.imread(file)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Detect targets in the image
		entities = cascade.detectMultiScale(
		    gray,
		    scaleFactor=1.1,
		    minNeighbors=5,
		    minSize=(30, 30),
		)

		print(f"Found {len(entities)} entitiy(s) in video {path} frame {frame}!")

		# Draw a rectangle around the targets
		height, width, channel = image.shape

		#try to match target to entities
		for (x, y, w, h) in entities:
			if(w !=0 and h!=0): 
				newTarget = Target(x,y,w,h,width,height,image)
				found = False
				for entry in detected_entities:
					if(abs(entry.frames[-1].x - x) < entity_movement_threshold
						and abs(entry.frames[-1].y - y) < entity_movement_threshold):
						entry.frames.append(newTarget)
						found=True
				if not found:
					newEntity = Entity(newTarget, len(detected_entities))
					detected_entities.append(newEntity)
				# Uncomment to see each target per frame
				# cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
				# cv2.imshow("Target found", image)
				# cv2.waitKey(0)
		
		frame+=1

	return detected_entities, frame


if __name__ == "__main__":

	if(len(sys.argv)!=2):
		print("Wrong arguments")
		print("Usage: face_track.py <input mp4>")
		exit()

	videoPath = sys.argv[1]

	#amount of pixel movement between frames for an entity to still be considered
	#that entity
	entity_movement_threshold = 40
	#percent of frames that an entity must be in for an entity to count as a real entity
	entity_frame_threshold = 0.50
	#amount of outside of image from face (2,3) referes to 2x larger than detection width, 3x taller than detection height
	output_scale = (2,2)
	
	detected_entities, frames = parse_video(videoPath, entity_movement_threshold)

	for entity in detected_entities:
		if(len(entity.frames)>=(frames*entity_frame_threshold)):
			print(f"Entity '{entity.name}' found in {len(entity.frames)} frames. Saving result")
			shift_resize_images(entity.frames, entity.name, output_scale)

