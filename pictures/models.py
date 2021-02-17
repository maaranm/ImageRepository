from django.db import models

#model used to store uploaded data from the user
class image(models.Model):
	image_name = models.CharField(max_length=200)
	image = models.ImageField(upload_to='images')
	#overriten to provide useful information if needed
	def __str__(self):
		return self.image_name

#model used to store uploaded data and extracted data
class annotated_image(models.Model):
	image_name = models.CharField(max_length=200)
	image = models.ImageField(upload_to='images')
	marked_img = models.ImageField(upload_to='images/marked')
	detected_object = models.CharField(max_length=200)
	#overriten to provide useful information if needed
	def __str__(self):
		return self.detected_object

