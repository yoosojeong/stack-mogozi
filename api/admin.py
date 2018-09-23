from django.contrib import admin

# Register your models here.
from api.models import *


class VersionAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostModelAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Version, VersionAdmin)
admin.site.register(UserModel, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostModel, PostModelAdmin)
admin.site.register(Comment, CommentAdmin)
