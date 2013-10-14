from django.core.urlresolvers import reverse

from django.db import models

class Post (models.Model):
	createdAt = models.DateTimeField(verbose_name="Publication date")
	visible = models.BooleanField(default=False, verbose_name="Published", db_index=True)
	title = models.CharField(max_length=128)
	slug = models.CharField(max_length=128, db_index=True)
	text = models.TextField()
	tags = models.ManyToManyField('Tag', related_name='tags', blank=True)

	def url(self):
		if self.slug: 
			return reverse('blogs.views.slug', args=[self.slug])
		else: 
			return reverse('blogs.views.id', args=[self.id])

	def text_cleaned(self):
		return self.text.replace("&nbsp;", " ")

	def __unicode__(self):
		return self.title	
		
class Tag(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(db_index=True)
	
	def __unicode__(self):
		return self.name.capitalize()
