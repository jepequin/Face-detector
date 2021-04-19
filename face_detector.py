import os
from time import time
import pytesseract
import cv2 #import OpevCV
from PIL import Image
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
	'''Changes coordinates rectangle from (upper_left_x, upper_left_y, witdth, height) to (upper_left_x, upper_left_y, lower_right_x, lower_right_y)
	:type coordinates: list 
	:param coordinates: integer list of upper-left coordinates and dimensions

	:rtype: list
	:return: integer list with diagonal coordinates of rectangle
	'''
	coordinates[2] += coordinates[0]
	coordinates[3] += coordinates[1]
	return coordinates	

def resize(images):
	'''Resizes images to match smallest image dimensions 
	:type images: list
	:param images: list of pillow images

	:rtype: list
	:return: list of equally sized pillow images
	'''
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

def image_dictionary(folder):
	'''Creates image dictionary using images in folder
	:type folder: str
	:param folder: path to folder containing images

	:rtype: dict
	:return: dictionary whose keys are image (relative) paths, and values are numpy array images
	'''
	image_dictionary = dict()
	for image_name in os.listdir(folder):
		image_path = os.path.join(folder,image_name)
		image = cv2.imread(image_path) # load image with opencv
		image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # change mode to grayscale allows to capture more text	
		image_dictionary[image_path] = image
	return image_dictionary	

def filter_by_keyword(image_dictionary,keyword):
	'''Filters image_dictionary images according to keyword
	:type image_dictionary: dict
	:param image_dictionary: keys are image (relative) paths, values are numpy array images	
	:type keyword: str
	:param keyword: string used to filter entries of dictionary image_dictionary

	:rtype: dict
	:return: filtered dictionary containing images where keyword was found
	'''
	keyword = keyword.lower()
	dictionary = image_dictionary.copy()
	for image_path in image_dictionary:
		image = dictionary[image_path]
		text = pytesseract.image_to_string(image).lower() # get text from image 
		if keyword not in text:
			del dictionary[image_path] # delete entry from dictionary if keyword not detected
	return dictionary

def delete_text(image):
	'''Performs image segmentation to delete text from image 
	:param image: image to be segmented
	:type image: numpy array image

	:return: image with text deleted 
	:rtype: numpy array image
	'''
	boxes = list()
	segmentation_data = pytesseract.image_to_data(image) # each line of this string corresponds to a potentially retrieved word
	segmentation_data = segmentation_data.split('\n')[1:] # ignore header 
	for data_string in segmentation_data:		
		data_list = data_string.split('\t')
		word_detected = data_list[-1].strip() # no word was retrieved if this stripped string is empty  
		if word_detected:
			coordinates = coordinate_change([int(coordinate) for coordinate in data_list[6:10]])
			start_point = tuple(coordinates[:2])
			end_point = tuple(coordinates[2:])
			image = cv2.rectangle(image,start_point,end_point,color=255,thickness=-1) # thickness -1 fills rectangle shape by specified (white) color. 
	return image

def detect_faces(image):
	'''Detects faces in image
	:param image: image for facial recognition
	:type image: numpy array image

	:rtype: list
	:return: list of pillow images cotaining faces
	'''
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') # xml file stored during opencv installation
	face_coordinates = face_cascade.detectMultiScale(image,minNeighbors=17) # higher minNeighbors value lowers false-positives detections
	image = Image.fromarray(image)
	faces = list()
	for coordinates in face_coordinates:
		coordinates = coordinate_change(coordinates) # detectMultiScale returns (upper_left_x, upper_left_y, witdth, height)
		face = image.crop(coordinates)
		faces.append(face)
	return faces

def mosaic(images):
	'''Creates mosaic from images in list images
	:param images: list of pillow images
	:type images: list

	:return: mosaic image
	:rtype: pillow image
	'''
	images = resize(images)
	### Calculate mosaic's number of rows and columns  
	nb_columns = floor(sqrt(len(images)))
	nb_rows = ceil(len(images)/nb_columns)
	### Get dimensions of images to form mosaic 
	tesserae_width = images[0].width
	tesserae_height = images[0].height
	### Calculate dimenson of mosaic
	mosaic_width = tesserae_width*nb_columns
	mosaic_height = tesserae_height*nb_rows
	### Create contact sheet
	mosaic = Image.new('L',(mosaic_width,mosaic_height))
	for index in range(len(images)):
		x_position = index % nb_columns
		y_position = floor(index/nb_columns)
		mosaic.paste(images[index],(x_position*tesserae_width,y_position*tesserae_height)) # second parameter specifies where to paste image (upper left coordinates) 
	return mosaic

def main():
	keyword = input_keyword()
	start = time()
	print('Creating image dictionary...')
	img_dictionary = image_dictionary('small_img')
	end = time()
	print('Image dictionary created in {}s'.format(end-start))
	start = time()
	print('Looking for instances of keyword "{}" in images'.format(keyword))
	filtered_dictionary = filter_by_keyword(img_dictionary,keyword)
	end = time()
	print('Acomplished in {}s. Keyword "{}"" found in images: {}'.format(end-start,keyword,filtered_dictionary.keys()))
	for key in filtered_dictionary:
		print('Analyzing image {}...'.format(key))
		image = filtered_dictionary[key]
		print('Dictionary updated')
		image = delete_text(image)
		print('Text deleted')
		faces = detect_faces(image)
		print('Faces detected')
		mosaic(faces).show()
		break

main()
 

