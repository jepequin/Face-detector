import os
import pytesseract
import cv2 #import OpevCV
from PIL import Image, ImageDraw
from math import ceil, floor, sqrt

def input_keyword():
	'''Lets user input word to search for
	:rtype: string
	:return: keyword used to search images
	'''
	stop_input = False
	while not stop_input:
		word = input('Enter keyword to search for: ')
		if word.isalpha():
			stop_input = True
		else:
			print('Input must be alphabetical')
	return word

def coordinate_change(coordinates):
	coordinates[2] += coordinates[0]
	coordinates[3] += coordinates[1]
	return coordinates	

def resize(images):
	heights = list()
	widths = list()
	for image in images:
		height = image.height
		width = image.width
		heights.append(height)
		widths.append(width)
	base_width = sorted(widths)[0]
	base_height = sorted(heights)[0]
	images = [image.resize((base_width,base_height)) for image in images]
	return images

def build_image_dictionary(folder):
	'''Creates image dictionary using images in folder
	:type folder: str
	:param folder: path of folder containing images

	:rtype: dict
	:return: dictionary whose keys are image (relative) paths, and values are pillow images
	'''
	image_dictionary = dict()
	for image_name in os.listdir(folder):
		image_path = os.path.join(folder,image_name)
		
		#image = Image.open(image_path)
		image = cv2.imread(image_path)
		
		#image = image.convert('L') # change mode to grayscale allows to capture more text
		image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
		
		image_dictionary[image_path] = image
	return image_dictionary	

def filter_by_keyword(image_dictionary,keyword):
	''' Filters image_dictionary images according to keyword
	:type image_dictionary: dict
	:param image_dictionary: keys are image (relative) paths, values are pillow images	
	:type keyword: str
	:param keyword: string used to filter entries of dictionary image_dictionary

	:rtype: dict
	:return: filtered dictionary containing images where keyword was found
	'''
	keyword = keyword.lower()
	dictionary = image_dictionary.copy()
	for image_path in image_dictionary:
		#image_path = 'small_img/a-0.png'
		image = dictionary[image_path] # mode attribute shows image is RGB
		#image.show()
		text = pytesseract.image_to_string(image).lower()
		#print(text)
		if keyword not in text:
			del dictionary[image_path]
	return dictionary

def detect_faces(image):
	'''Detects faces in image
	:param image: image for facial recognition
	:type image: numpy array image

	:rtype: list
	:return: list of pillow images cotaining faces
	'''
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # xml file stored during opencv installation
	face_coordinates = face_cascade.detectMultiScale(image)
	image = Image.fromarray(image)
	faces = list()
	#drawing_object = ImageDraw.Draw(image)
	for coordinates in face_coordinates:
		coordinates = coordinate_change(coordinates)
		#drawing_object.rectangle(coordinates,fill=None,outline='red')
		face = image.crop(coordinates)
		faces.append(face)
	return faces

def mosaic(images):
	'''Creates mosaic from images in list images
	:param images: list of PIL images
	:type images: list

	:return: mosaic image
	:rtype: PIL image
	'''
	images = resize(images)
	nb_columns = floor(sqrt(len(images)))
	nb_rows = ceil(len(images)/nb_columns)

	tesserae_width = images[0].width
	tesserae_height = images[0].height
	mosaic_width = tesserae_width*nb_columns
	mosaic_height = tesserae_height*nb_rows
	mosaic = Image.new('L',(mosaic_width,mosaic_height))
	
	for index in range(len(images)):
		x_position = index % nb_columns
		y_position = floor(index/nb_columns)
		mosaic.paste(images[index],(x_position*tesserae_width,y_position*tesserae_height))
	return mosaic

#keyword = input_keyword()
#image_dictionary = build_image_dictionary('small_img')
#updated_dictionary = filter_by_keyword(image_dictionary,keyword)
#print(updated_dictionary.keys())
#faces = detect_faces(image_dictionary['small_img/a-0.png'])
#mosaic(faces).show()


