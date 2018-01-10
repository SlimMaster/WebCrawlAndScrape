from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType


from django.core.urlresolvers import reverse
from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify

from comments.models import Comment
# Create your models here.
class Product(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,null=True)
	name = models.CharField(max_length=120,null=True)
	slug = models.SlugField(unique=True,null=True)
	price = models.CharField(max_length=120,null=True)
	image_url = models.CharField(max_length=120,null=True)
	category = models.CharField(max_length=120,null=True)
	sub_category = models.CharField(max_length=120,null=True)
	addr_pr = models.CharField(max_length=120,null=True)
	store = models.CharField(max_length=120,null=True)




	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name
	def __repr__(self):
		return super(self.__class__,self).__repr__().decode('utf8').encode('unicode_escape')
	
	def get_absolute_url(self):
		return reverse("products:detail",kwargs={"slug":self.slug})   #posts/detail/{0}..
	
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
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Product.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "{0}-{1}".format(slug ,instance.id)
		return create_slug(instance , new_slug=new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args , **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver , sender=Product)