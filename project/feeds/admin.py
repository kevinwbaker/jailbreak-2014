from django.contrib import admin

from feeds.models import Feed
from feeds.models import Post

admin.site.register(Feed)
admin.site.register(Post)
