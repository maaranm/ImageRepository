import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import tempfile
from six.moves.urllib.request import urlopen
from six import BytesIO
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from django.core.files.base import ContentFile
from django.conf import settings
from io import BytesIO, StringIO

#load detector to be used for feature extraction
module_handle = settings.TENSORFLOW_MODULE_URL
detector = hub.load(module_handle).signatures['default']

#helper function to draw bounding box
def draw_bounding_box(image, y_min, x_min, y_max, x_max, color, font, thickness=4, display_str_list=()):
	draw = ImageDraw.Draw(image)
	og_width, og_height = image.size

	(left, right, top, bottom) = (x_min*og_width, x_max*og_width, y_min*og_height, y_max*og_height)

	draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)

	display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]

	total_display_str_height = (1+2*0.05) * sum(display_str_heights)

	if top > total_display_str_height:
		text_bottom = top
	else:
		text_bottom = top+total_display_str_height

	for display_str in display_str_list[::-1]:
		text_width, text_height = font.getsize(display_str)
		margin = np.ceil(0.05*text_height)

		draw.rectangle([(left, text_bottom - text_height - 2 * margin),
						(left + text_width, text_bottom)],
						fill=color)
		draw.text((left+margin, text_bottom - text_height - margin),
					display_str,
					fill="black",
					font=font)
		text_bottom -= text_height - 2*margin

#helper function to draw all bounding boxes
def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
	colors = list(ImageColor.colormap.values())

	font = ImageFont.load_default()

	for i in range(min(boxes.shape[0], max_boxes)):
		if scores[i] >= min_score:
			y_min, x_min, y_max, x_max = tuple(boxes[i])
			display_str = "{}: {}%".format(class_names[i].decode("ascii"), int(100*scores[i]))

			color = colors[hash(class_names[i]) % len(colors)]
			image_pil = Image.fromarray(np.uint8(image)).convert("RGB")

			draw_bounding_box(
				image_pil,
				y_min,
				x_min,
				y_max,
				x_max,
				color,
				font,
				display_str_list=[display_str])

			np.copyto(image, np.array(image_pil))

	return image

#helper function to remove duplicates in detected objects
def simplify_result(full_result):
	return set(full_result['detection_class_entities'])

#helper function to load image for processing
def load_img(path):
	img = tf.io.read_file(path)
	img = tf.image.decode_jpeg(img, channels=3)
	return img

#opens image and runs detector against it
#return a tuple of the detected objects and the generated image with bounding boxes and labels
def run_detector(path):
	img = load_img(path)
	converted_img = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
	result = detector(converted_img)
	result = {key:value.numpy() for key,value in result.items()}
	simple = simplify_result(result)
	numpy_img = draw_boxes(img.numpy(), result["detection_boxes"], result["detection_class_entities"], result["detection_scores"])
	regular_img = Image.fromarray(numpy_img)
	img_io = BytesIO()
	regular_img.save(img_io, format='JPEG')
	img_content = ContentFile(img_io.getvalue(), path.rsplit('\\', 1)[1])
	return_val = (simple, img_content)
	return return_val

