from django.contrib import admin
from .models import Post,Category,Contact
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}

class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','email','number','subject']


admin.site.register(Post, PostAdmin)
admin.site.register(Contact)
admin.site.register(Category, CategoryAdmin)

