from django.template.defaultfilters import slugify
from django.db import models

class Moho (models.Model):
	createdAt = models.DateTimeField(auto_now_add=True)
	
	like = models.BooleanField(db_index=True)
	visible = models.BooleanField(default=False, verbose_name="Published", db_index=True)
	
	title = models.CharField(max_length=128)
	slug = models.SlugField(db_index=True)
	text = models.TextField()
	year = models.PositiveSmallIntegerField(blank=True, db_index=True)
	
	imageURL = models.FileField(upload_to='moho', verbose_name="Film poster", blank=True)
	imdbURL = models.URLField(verbose_name="IMDB link", blank=True)
	genres = models.ManyToManyField('Genre', related_name='genres', blank=True)
	actors = models.ManyToManyField('Actor', related_name='actors', blank=True)
	directors = models.ManyToManyField('Director', related_name='directors', blank=True)
	
	def get_similar(self):
		return Moho.objects.distinct().values(
			'id','title','year','slug','imageURL'
		).filter(
			like=self.like, genres__in = self.genres.all()
		).exclude(id=self.id).order_by('?')[:9]		
	
	def __unicode__(self):
		return self.title.capitalize()

	def save(self, *args, **kwargs):
		self.slug = slugify("{0}".format(self.title))

		super(Moho, self).save(*args, **kwargs)
	
class Genre(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(db_index=True)
	
	def __unicode__(self):
		return self.name.capitalize()
	
class Actor(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(db_index=True)
	
	def __unicode__(self):
		return self.name.title()

class Director(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(db_index=True)
	
	def __unicode__(self):
		return self.name.title()