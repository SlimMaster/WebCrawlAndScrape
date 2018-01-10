from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [  

	url(r'^$', views.PostListAPIView.as_view(), name ='list'),
	url(r'^create/$', views.PostCreateAPIView.as_view(),name='create'),
	url(r'^(?P<slug>[\w-]+)/$', views.PostDetailAPIView.as_view(), name='detail'),

	url(r'^(?P<slug>[\w-]+)/edit/$', views.PostUpdateAPIView.as_view() , name='update'),
	url(r'^(?P<slug>[\w-]+)/delete/$', views.PostDeleteAPIView.as_view(), name='delete'),
	
	
# 	url(r'^accounts/login/$', e_compare_views.login),
# 	url(r'^accounts/logout/$', e_compare_views.logout),
# 	url(r'^accounts/auth/$', e_compare_views.auth_view),
# 	url(r'^accounts/loggedin/$', e_compare_views.loggedin),
# 	url(r'^accounts/invalid/$', e_compare_views.invalid_login),
    

#    url(r'^login/', login_view,name='login'),
#   url(r'^logout/', logout_view,name='logout'),
#    url(r'^register/', register_view,name='register'),
#    url(r'^', home_view,name='home'),





]
