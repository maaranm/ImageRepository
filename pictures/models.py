from django.db import models

class Image(models.Model):
	caption = models.CharField(max_length=200)
	image = models.ImageField(upload_to='images')

	def __str__(self):
		return self.caption

class AnnotatedImage(models.Model):
	caption = models.CharField(max_length=200)
	image = models.ImageField(upload_to='images')
	marked_img = models.ImageField(upload_to='images/marked')
	detected_object = models.CharField(max_length=200)
	def __str__(self):
		return self.detected_object

