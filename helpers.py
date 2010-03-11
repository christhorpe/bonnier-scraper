import yql

from google.appengine.api import images


def do_yql(query):
	y = yql.Public()
	result = y.execute(query)
	return result



def get_image_aspect(image):
	img = images.Image(image)
	width = img.width
	height = img.height
	if width == height:
		return "square"
	elif width > height:
		return "landscape"
	elif height > width:
		return "portrait"


def get_size(image):
	img = images.Image(image)
	width = img.width
	height = img.height
	return width, height


def check_min_size(image, size):
	width, height = get_size(image)
	errors = []
	if width < size:
		errors.append("The image you supplied is too thin (needs to be a minimum of "+ str(size) +" pixels wide)")
	if height < size:
		errors.append("The image you supplied is not tall enough (needs to be a minimum of "+ str(size) +" pixels high)")
	return errors



def resize_image(image, size):
	img = images.Image(image)
	width = img.width
	height = img.height
	if width > size and height > size:
		aspect = get_image_aspect(image)
		if aspect == "square":
			width = size
			height = size
		elif aspect == "landscape":
			factor = height/size
			height = size
			width = int(width/factor)
		elif aspect == "portrait":
			factor = width/size
			width = size
			height = int(height/factor)
		img.resize(width=width, height=height)
		image = img.execute_transforms(output_encoding=images.JPEG)			
	return image



def crop_image(image, size):
	image = resize_image(image, size)
	img = images.Image(image)
	width = img.width
	height = img.height
	shape = get_image_aspect(image)
	if shape == "square":
		return image
	elif shape == "portrait":
		left_x = 0.0
		top_y = float((height-size)/2)/float(height)
		right_x = 1.0
		bottom_y = float(((height-size)/2) + size)/float(height)
	elif shape == "landscape":
		left_x = float((width-size)/2)/float(width)
		top_y = 0.0
		right_x = float(((width-size)/2) + size)/float(width)
		bottom_y = 1.0
	img.crop(left_x, top_y, right_x, bottom_y)
	cropimage = img.execute_transforms(output_encoding=images.JPEG)	
	return cropimage

