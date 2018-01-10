from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView
	)

from posts.models import Post
from .serializers import (
	PostSerializer,
	PostCreateUpdateSerializer
	)

class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer

class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'slug'    #       ===> change the defalut lokkup in url which is the id 


class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	lookup_field = 'slug'    #       ===> change the defalut lokkup in url which is the id 


class PostListAPIView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer




class PostUpdateAPIView(UpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'    #       ===> change the defalut lokkup in url which is the id 


