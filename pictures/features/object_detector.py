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
from io import BytesIO, StringIO

moduleHandle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"
detector = hub.load(moduleHandle).signatures['default']


def draw_bounding_box(image, yMin, xMin, yMax, xMax, color, font, thickness=4, displayStrList=()):
	draw = ImageDraw.Draw(image)
	og_width, og_height = image.size

	(left, right, top, bottom) = (xMin*og_width, xMax*og_width, yMin*og_height, yMax*og_height)

	draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)

	displayStrHeights = [font.getsize(ds)[1] for ds in displayStrList]

	totalDisplayStrHeight = (1+2*0.05) * sum(displayStrHeights)

	if top > totalDisplayStrHeight:
		textBottom = top
	else:
		textBottom = top+totalDisplayStrHeight

	for displayStr in displayStrList[::-1]:
		print(displayStr)
		textWidth, textHeight = font.getsize(displayStr)
		margin = np.ceil(0.05*textHeight)

		draw.rectangle([(left, textBottom - textHeight - 2 * margin),
						(left + textWidth, textBottom)],
						fill=color)
		draw.text((left+margin, textBottom - textHeight - margin),
					displayStr,
					fill="black",
					font=font)
		textBottom -= textHeight - 2*margin

def draw_boxes(image, boxes, class_names, scores, maxBoxes=10, minScore=0.1):
	colors = list(ImageColor.colormap.values())

	font = ImageFont.load_default()

	for i in range(min(boxes.shape[0], maxBoxes)):
		if scores[i] >= minScore:
			yMin, xMin, yMax, xMax = tuple(boxes[i])
			displayStr = "{}: {}%".format(class_names[i].decode("ascii"), int(100*scores[i]))

			color = colors[hash(class_names[i]) % len(colors)]
			imagePil = Image.fromarray(np.uint8(image)).convert("RGB")

			draw_bounding_box(
				imagePil,
				yMin,
				xMin,
				yMax,
				xMax,
				color,
				font,
				displayStrList=[displayStr])

			np.copyto(image, np.array(imagePil))

	return image

def simplify_result(full_result):
	return set(full_result['detection_class_entities'])

def load_img(path):
	img = tf.io.read_file(path)
	img = tf.image.decode_jpeg(img, channels=3)
	return img

def runDetector(detector, path):
	img = load_img(path)
	convertedImg = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
	result = detector(convertedImg)
	result = {key:value.numpy() for key,value in result.items()}
	simple = simplify_result(result)
	numpyImg = draw_boxes(img.numpy(), result["detection_boxes"], result["detection_class_entities"], result["detection_scores"])
	regularImg = Image.fromarray(numpyImg)
	img_io = BytesIO()
	regularImg.save(img_io, format='JPEG')
	img_content = ContentFile(img_io.getvalue(), path.rsplit('\\', 1)[1])
	returnVal = (simple, img_content)
	return returnVal