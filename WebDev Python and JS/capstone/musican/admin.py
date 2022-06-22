from django.contrib import admin

from .models import AlbumInfo, Artist, SongInfo, User, Genre, Comments, Auction_Listings

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(AlbumInfo)
admin.site.register(Artist)
admin.site.register(SongInfo)
admin.site.register(Comments)
admin.site.register(Auction_Listings)
