
from django.conf.urls import url
from django.contrib import admin

from push_email.views import EmailView, EmailLoginView

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^email/$', EmailView.as_view(), name='email'),

    url(r'^$', EmailLoginView.as_view(), name='login'),
]
