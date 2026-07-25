from django.contrib import admin
from .models import Category,Post,About,Contact

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category' )
    search_fields = ('title', 'content')
    list_filter = ('category','created_at')
admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(About)
admin.site.register(Contact)