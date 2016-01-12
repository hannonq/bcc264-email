
from django.conf.urls import url
from django.contrib import admin

from push_email.views import EmailView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', EmailView.as_view(), name='home'),
]
