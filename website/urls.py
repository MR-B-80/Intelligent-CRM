from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("home2/", views.home2, name="home2"),
    # path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("record/<int:pk>", views.customer_record, name="record"),
    path("delete_record/<int:pk>", views.delete_record, name="delete_record"),
    path("add_record", views.add_record, name="add_record"),
    path("update_record/<int:pk>", views.update_record, name="update_record"),
    path("upload_audio_file/<int:pk>", views.upload_audio_file, name="upload_audio_file"),
    path("suggestion/<int:pk>", views.suggestion, name="suggestion"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
