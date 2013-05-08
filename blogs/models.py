from django.core.urlresolvers import reverse

from django.db import models

class Post (models.Model):
	createdAt = models.DateTimeField(verbose_name="Publication date")
	visible = models.BooleanField(default=False, verbose_name="Published")
	title = models.CharField(max_length=128)
	slug = models.CharField(max_length=128)
	text = models.TextField()
	tags = models.ManyToManyField('Tag', related_name='tags', blank=True)

	def url(self):
		if self.slug: 
			return reverse('blogs.views.slug', args=[self.slug])
		else: 
			return reverse('blogs.views.id', args=[self.id])

	def __unicode__(self):
		return self.title	
		
class Tag(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField()
	
	def __unicode__(self):
		return self.name.capitalize()
