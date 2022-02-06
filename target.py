from PIL import Image
import math 
import cv2

class Entity():
	"""
	Entity that the target belongs to
	Resembes a collection of target frames put together
	"""
	def __init__(self, frame, entity_name):
		"""Constructor for the entity"""
		self.frames = [] #frames that entity is alive
		self.frames.append(frame)
		self.possible_frames = []
		self.name = entity_name


class Target():
	"""
	Specified target (by the cascade)
	Ex: Target=Face
	"""
	def __init__(self, x, y, w, h, iw, ih, file):
		"""Constructor for the target"""
		self.x = x #start x of face
		self.y = y #start y of face
		self.w = w #width of face
		self.h = h #height of face
		self.xCenter = x+w/2 #center of face
		self.yCenter = y+h/2
		self.imageW = iw #image width
		self.imageH = ih #image height
		img = cv2.cvtColor(file, cv2.COLOR_BGR2RGB)
		self.PILimage = Image.fromarray(img)
		self.calculate_error() 
	def scale_image(self, newImageW, newImageH):
		"""Scale the image to match passed in target height and width"""
		self.x = int((newImageW / self.imageW)*self.x)
		self.y = int((newImageH / self.imageH)*self.y)
		self.w = int((newImageW / self.imageW)*self.w)
		self.h = int((newImageH / self.imageH)*self.h)
		self.imageH = newImageH
		self.imageW = newImageW
		#recalculate error values 
		self.calculate_error()
	def calculate_error(self):
		"""Find the pixel error from the center of the image"""
		self.xErr = self.imageW/2 - (self.x+self.x+self.w)/2 #pixels offset from x center
		self.yErr = self.imageH/2 - (self.y+self.y+self.h)/2 #pixels offset from y center
		self.Err = math.sqrt(self.yErr**2 + self.xErr**2) #total distance face is from center
