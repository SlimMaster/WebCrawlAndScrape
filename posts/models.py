from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from django.core.urlresolvers import reverse
from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify

from comments.models import Comment

# Create your models here.

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,null=True)
	title = models.CharField(max_length=120,null=True)
	slug = models.SlugField(unique=True,null=True)
	content = models.TextField(null=True)
	url = models.CharField(max_length=150,null=True)
	image = models.FileField(null=True, blank=True)
	update = models.DateTimeField(auto_now = True,auto_now_add = False,null=True)
	timestamp = models.DateTimeField(auto_now = False,auto_now_add = True,null=True)


	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail",kwargs={"slug":self.slug})   #posts/detail/{0}..
	
	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type


def create_slug(instance,new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "{0}-{1}".format(slug ,instance.id)
		return create_slug(instance , new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args , **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver , sender=Post)