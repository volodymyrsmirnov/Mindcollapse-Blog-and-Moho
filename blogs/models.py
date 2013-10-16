from django.core.urlresolvers import reverse
from softhyphen.html import hyphenate

from django.db import models
from django.db.models.signals import post_save

from django.core.cache import cache

from blogs.helpers import make_template_fragment_key

class Post(models.Model):
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
		return hyphenate(self.text.replace("&nbsp;", " "), language="ru-ru")

	def __unicode__(self):
		return self.title	
		
class Tag(models.Model):
	name = models.CharField(max_length=50)
	slug = models.SlugField(db_index=True)
	
	def __unicode__(self):
		return self.name.capitalize()

def clear_template_cache(sender, **kwargs):
	post = kwargs.get("instance")

	key = make_template_fragment_key("posts", [post.id])

	if key:
		cache.delete(key)

post_save.connect(clear_template_cache, sender=Post)
