from django.contrib import admin
from mof_network.models import *


# @admin.register(Apatite, Comment)
# class AuthorAdmin(admin.ModelAdmin):
#     pass
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Mof)
admin.site.register(Connection)
