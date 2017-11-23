from django.conf.urls import url
from .views import MathFunctions

urlpatterns = [
    url(r'^mathFunctions/$', MathFunctions.as_view(), name='gapi-math-functions'),
]