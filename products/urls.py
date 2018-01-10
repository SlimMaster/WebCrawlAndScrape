from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [  

	url(r'^$', views.product_list, name ='list'),
	# url(r'^create/$', views.post_create),
	url(r'^(?P<slug>[\w-]+)/$', views.product_detail, name='detail'),
	


	# url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update , name='update'),
	# url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
	
	
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
