from django.core.exceptions import ValidationError
import random, string, os
from PIL import Image
import math

def random_id(l=11):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(l)])

def get_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{random_id(20)}.{ext}'
    return os.path.join('images', filename)

def resize(path):
	img = Image.open(path)
	width, height = img.size
	minsize = min((*img.size,1080))

	if width > height:
		x = math.ceil((width - minsize) / 2)
		y = 0
		width = width - math.floor((width - minsize) / 2)
		height = minsize

	elif width < height:
		x = 0
		y = math.ceil((width - minsize) / 2)
		width = minsize
		height = width - math.floor((width - minsize) / 2)

	elif width == height:
		if width > 1080 or height > 1080:
			img.thumbnail((minsize, minsize), Image.Resampling.LANCZOS)
		return img

	crop_data = (x, y, width, height)
	return img.crop(crop_data)

def image_size_validator(image):
	file_size = image.size
	max_size = 10.0
	if file_size > max_size * 1024 * 1024:
		raise ValidationError('You cannot upload file more than 10Mb')
	return image