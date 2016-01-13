from django.contrib import admin

from .models import MyEmail, Copy, Recipient

admin.site.register(MyEmail)
admin.site.register(Copy)
admin.site.register(Recipient)


