import os
import pictures.features.object_detector as object_detector
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from .forms import image_form
from .forms import search_form
from .models import annotated_image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
import threading

#Used to view all uploaded images
def view_all(request):
	#create a list of images in the media directory and then pass them to the html to load/display
	path = settings.MEDIA_ROOT
	img_list = os.listdir(path + '/images')
	context = {'images' : img_list}
	return render(request, "pictures/index.html", context)

#Used to upload an image
def image_upload_view(request):
	#Same view is used for the intial get request and the post request made when uploading
	#post means the image is being uploaded
	if request.method == 'POST':
		#save the form to db if valid
		form = image_form(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			#get the current object for processing
			img_obj = form.instance
			#start a background task to extract features and save the manipulated image
			background = threading.Thread(target=create_and_save_annotated, args=[img_obj.image.path, img_obj])
			background.setDaemon(True)
			background.start()
			#render the same page with the image this time
			return render(request, 'pictures/upload.html', {'form': form, 'img_obj': img_obj})

	#first time coming to the upload page provide a blank form
	else:
		form = image_form()
	return render(request, 'pictures/upload.html', {'form': form})

#view to search for images
def object_input(request):
	#similar to #image_upload_view where same view is used for post and get
	if request.method == 'POST':
		#validate form and process info
		form = search_form(request.POST)
		if form.is_valid():
			#extract user input
			object_to_find = form.cleaned_data['object_name']
			#query db for matching images
			images_with_objects = annotated_image.objects.filter(detected_object=object_to_find)
			img_list = []
			#make a list of just the names of the images so we can reuse index.html
			for image in images_with_objects:
				img_list.append('marked/' + image.marked_img.name.rsplit('/', 1)[1])
			context = {'images' : img_list}
			return render(request, "pictures/index.html", context)
	else:
		form = search_form()

	return render(request, 'pictures/search_form.html', {'form': form})

#helper function made to make creating a thread simpler
def create_and_save_annotated(path, img_obj):
	detection_data = object_detector.run_detector(path)
	#create and save entries to the annotated_image table in the db
	for obj_in_img in detection_data[0]:
		annotated_image.objects.create(image_name=img_obj.image_name, image=img_obj.image, marked_img=detection_data[1], detected_object=obj_in_img.decode("ascii"))