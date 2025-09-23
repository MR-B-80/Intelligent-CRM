from django.contrib import admin
from django.urls import path, include
from website import views

handler404 = 'website.views.custom_404'
# handler500 = 'views.custom_500'



urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("website.urls"))
]
