from django.db import models

class University(models.Model):
	'''University'''

	name = models.CharField(max_length=128)
	abbreviation = models.CharField(max_length=6)

class Team(models.Model):
	'''Team taking part'''

	slug = models.SlugField()
	name = models.CharField(max_length=128)
	photo = models.FileField(upload_to='teams')
	sponsor_link = models.URLField()
	description = models.TextField()
	university = models.ForeignKey('University')

	long_position = models.DecimalField(max_digits=8, decimal_places=3)
	lat_position = models.DecimalField(max_digits=8, decimal_places=3)

	def __unicode__(self):
		return self.name
