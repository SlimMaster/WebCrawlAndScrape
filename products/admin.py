from django.contrib import admin
from .models import Product
# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
	list_display = ["name","price","store"]
	class Meta:
		model = Product



admin.site.register(Product,ProductModelAdmin)