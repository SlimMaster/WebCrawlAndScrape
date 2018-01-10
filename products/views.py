# -*- coding: utf-8 -*-
# -*- coding: latin-1 -*-
from django.contrib import messages
#from django.contrib.contenttypes.models import ContentType

from django.contrib.contenttypes.models import ContentType

from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404 , redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from comments.forms import CommentForm
from comments.models import Comment
from .models import Product
import re
from collections import defaultdict

# from .forms import PostForm

# Create your views here.


# def post_create(request):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404

# 	# if not request.user.is_authenticated():
# 	# 	raise Http404

	
# 	form = PostForm(request.POST or None, request.FILES or None)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		#print form.cleaned_data.get("title")
# 		instance.save()
# 		messages.success(request," Your Post has been Successfully Created")
# 		return HttpResponseRedirect(instance.get_absolute_url())#('../detail/{0}/'.format(instance.slug))
# 	# else:
# 	# 	messages.success(request," Error in post's creation . please try again .")
			
# 	context = {
# 		"form": form,
# 		"action":"Register Post"
# 	}
# 	return render(request,"post_form.html",context)

import operator


def product_detail(request, slug=None):
	instance = get_object_or_404(Product, slug=slug)
	my_regex = instance.name.split(" ")

	names = Product.objects.values_list("name")
	red = defaultdict(lambda: 0)
	for i in names:
		for j in "".join(i).split(" "):
			red[j] = red[j]+1

	from collections import OrderedDict
	d_sorted_by_value = OrderedDict(sorted(red.items(), key=lambda x: x[1]))
	blacklist = d_sorted_by_value.keys()
	query = Q(name__iregex=re.escape(my_regex[0]))
	

	for i in range(1, len(my_regex)):
		if my_regex[i] not in blacklist:
			query = query | Q(name__iregex=re.escape(my_regex[i]))
	
	queryset_list = Product.objects.filter(query)
	#print queryset_list

	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}

	comment_form = CommentForm(request.POST or None, initial=initial_data)

	if comment_form.is_valid() and request.user.is_authenticated():
		c_type = comment_form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = comment_form.cleaned_data.get("object_id")
		content_data = comment_form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))

		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
				user = request.user,
				content_type = content_type,
				object_id = obj_id,
				content = content_data,
				parent = parent_obj,
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
		
		# instance_com = comment_form.save(commit=False)
		# instance_com.save()

	# content_type = ContentType.objects.get_for_model(Post)
	# obj_id = instance.id
	# #Post.objects.get(id=instance.id)
	comments = instance.comments#Comment.objects.filter_by_instance(instance)

	context = {
		# "title":instance.name,
		# "url":instance.,
		"list":queryset_list,
		"instance":instance,
		"comments":comments,
		"comment_form":comment_form,
	}

	return render(request,"product_detail.html",context)

def product_list(request):

	for row in Product.objects.all():
		if Product.objects.filter(name=row.name).count() > 1:
			row.delete()

	queryset_list = Product.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(name__icontains=query) |
			Q(category__icontains=query)
			).distinct()

	paginator = Paginator(queryset_list,9)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer deliver the first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of range then deliver last page
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list":queryset,
		"title" : "list",
		"page_request_var":page_request_var
	}
	return render(request,"index.html",context)

def computer_list(request):

	# for row in Product.objects.all():
	# 	if Product.objects.filter(name=row.name).count() > 1:
	# 		row.delete()

	queryset_list = Product.objects.filter(
		Q(sub_category__icontains="Ordinateurs portables")|
		Q(sub_category="Ordinateur de bureau")|
		Q(sub_category="PC Gaming")
		)
	# query = request.GET.get("q")
	# if query:
	# 	queryset_list = queryset_list.filter(
	# 		Q(name__icontains=query) |
	# 		Q(category__icontains=query)
	# 		).distinct()

	paginator = Paginator(queryset_list,9)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer deliver the first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of range then deliver last page
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list":queryset,
		"title" : "list",
		"page_request_var":page_request_var
	}
	return render(request,"categ.html",context)

def tele_list(request):


	queryset_list = Product.objects.filter(
		# Q(category__icontains="IMAGE & SON")|
		Q(sub_category__icontains="Téléviseurs")
		)
	

	paginator = Paginator(queryset_list,9)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer deliver the first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of range then deliver last page
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list":queryset,
		"title" : "list",
		"page_request_var":page_request_var
	}
	return render(request,"categ.html",context)
def smart_list(request):


	queryset_list = Product.objects.filter(
		Q(sub_category__icontains="Smartphone & Mobile")|
		Q(sub_category__icontains="Téléphone Fixe")|
		Q(sub_category__icontains="Smart Watch")
		)
	

	paginator = Paginator(queryset_list,9)
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer deliver the first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of range then deliver last page
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list":queryset,
		"title" : "list",
		"page_request_var":page_request_var
	}
	return render(request,"categ.html",context)

# def post_update(request,slug=None):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404
# 	instance = get_object_or_404(Post, slug=slug)
# 	form = PostForm(request.POST or None,request.FILES or None,instance=instance)
# 	if form.is_valid():
# 		instance = form.save(commit=False)
# 		instance.save()
# 		messages.success(request," Modifications on your post have been saved")
# 		return HttpResponseRedirect(instance.get_absolute_url())
# 	# else:
# 	# 	messages.success(request," Error in Modification . please try again .")
# 	context = {
# 	"title":instance.title,
# 	"instance":instance,
# 	"form":form,
# 	"action":"Save Modification"
# 	}
# 	return render(request,"post_form.html",context)

# def post_delete(request,slug=None):
# 	if not request.user.is_staff or not request.user.is_superuser:
# 		raise Http404
# 	instance = get_object_or_404(Post, slug=slug)
# 	instance.delete()
# 	messages.success(request,"Successfully Deleted")

# 	return redirect("../..")


