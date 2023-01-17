from django.contrib import admin
from .models import PublicationModel,Tags,TypeOfRequest,Status,StatusMessage,StatusChat,TypeOfChat,FullStateOfChat

class PublicationAdmin(admin.ModelAdmin):
    list_display = ("name","author","date_of_create","time_of_create","date_of_update","time_of_update")
admin.site.register(PublicationModel,PublicationAdmin)
admin.site.register(Tags)
admin.site.register(TypeOfRequest)
admin.site.register(Status)
admin.site.register(StatusMessage)
admin.site.register(StatusChat)
admin.site.register(TypeOfChat)
admin.site.register(FullStateOfChat)