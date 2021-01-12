import os
import pictures.features.object_detector as object_detector
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from .forms import image_form
from .models import AnnotatedImage
import tensorflow_hub as hub
from django.core.files.uploadedfile import InMemoryUploadedFile

module_handle = "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"

detector = hub.load(module_handle).signatures['default']

# Create your views here.
def view_all(request):
	path = settings.MEDIA_ROOT
	img_list = os.listdir(path + '/images')
	context = {'images' : img_list}
	print(img_list)
	return render(request, "pictures/index.html", context)

def image_upload_view(request):
	"""Process images uploaded by users"""
	if request.method == 'POST':
		form = image_form(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			# Get the current instance object to display in the template
			img_obj = form.instance
			detection_data = object_detector.runDetector(detector, img_obj.image.path)
			for obj_in_img in detection_data[0]:
				AnnotatedImage.objects.create(caption=img_obj.caption, image=img_obj.image, marked_img=detection_data[1], detected_object=obj_in_img.decode("ascii"))

			return render(request, 'pictures/upload.html', {'form': form, 'img_obj': img_obj})
	else:
		form = image_form()
	return render(request, 'pictures/upload.html', {'form': form})

def image_with_object_view(request):
	images_with_objects = AnnotatedImage.objects.filter(detected_object='Table')
	img_list = []
	for image in images_with_objects:
		img_list.append('marked/' + image.marked_img.name.rsplit('/', 1)[1])
		print(image.marked_img.url)
		print(image.marked_img.name)


	print(img_list)
	context = {'images' : img_list}
	return render(request, "pictures/index.html", context)

def object_input(request):
	return render(request, "pictures/search_form.html")

