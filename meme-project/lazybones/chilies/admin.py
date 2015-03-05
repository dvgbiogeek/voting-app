from django.contrib import admin
from chilies.models import Meme, Vote


class MemeAdmin(admin.ModelAdmin):
    pass


class VoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Meme, MemeAdmin)
admin.site.register(Vote, VoteAdmin)
