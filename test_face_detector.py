from PIL import Image
import unittest
from face_detector import filter_by_keyword, build_image_dictionary

class TestImageFilter(unittest.TestCase):
	def test_filter(self):
		image_path = 'small_img/a-0.png'
		image = Image.open(image_path)
		print(type(image))
		image_dictionary = dict()
		image_dictionary[image_path] = image
		# Test images containing keyword are not removed
		updated_dictionary = filter_by_keyword(image_dictionary,'Snyder')
		self.assertEqual(updated_dictionary,image_dictionary)
		# Test images not containing keyword are removed
		updated_dictionary = filter_by_keyword(image_dictionary,'Pokemon')
		self.assertEqual(updated_dictionary,{})
	
class TestDictBuilder(unittest.TestCase):
	def test_builder(self):
		image_paths = ['small_img/a-0.png','small_img/a-1.png','small_img/a-2.png','small_img/a-3.png']
		dictionary = {image_path:Image.open(image_path) for image_path in image_paths}
		# Test image dictionary is correctly created
		folder = "small_img"
		image_dictionary = build_image_dictionary(folder)
		self.assertEqual(image_dictionary,dictionary)