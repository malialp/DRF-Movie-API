from django.core.exceptions import ValidationError
import random, string, os, io
from PIL import Image, ImageSequence
import math

def random_id(l=11):
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(l)])

def get_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{random_id(20)}.{ext}'
    return os.path.join('images', filename)

def resize(path, gif=False):
	if gif:
		img = path
	else:
		img = Image.open(path)
	
	width, height = img.size 
	maxsquaresize = min((*img.size,1080))

	x = math.ceil((width - maxsquaresize) / 2)
	y = math.ceil((height - maxsquaresize) / 2)
	width, height = maxsquaresize, maxsquaresize

	crop_data = (x, y, x + width, y + height)
	return img.crop(crop_data)

def image_size_validator(image):
	file_size = image.size
	max_size = 10.0
	if file_size > max_size * 1024 * 1024:
		raise ValidationError('You cannot upload file more than 10Mb')
	return image

def resize_gif(path):
	image = Image.open(path)

	frames = []
	for frame in ImageSequence.Iterator(image):
		frames.append(resize(frame, gif=True))

	duration = 0

	while True:
		try:
			frame_duration = image.info['duration']
			duration += frame_duration
			image.seek(image.tell() + 1)
		except EOFError:
			break

	buffer = io.BytesIO()
	frames[0].save(buffer, format=image.format.lower(), save_all=True, append_images=frames[1:], duration=duration, loop=0)
	return buffer