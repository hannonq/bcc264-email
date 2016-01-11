
from django.conf.urls import url
from django.contrib import admin

from push_email.views import HomePage

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', HomePage.as_view(), name='home'),
]
