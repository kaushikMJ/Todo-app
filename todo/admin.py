from django.contrib import admin
from .models import Todo
# Register your models here.


class showUpCreatedDate(admin.ModelAdmin):
	readonly_fields = ('dateCreated',)


admin.site.register(Todo,showUpCreatedDate)

