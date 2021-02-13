from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  path('register/', views.register, name="registration"),
  path('signin/', views.sign_in, name="signin"),
  path('changepassword/', views.change_password, name="changepassword"),
  path('logout/', views.sign_off, name="logout"),
  path('account/', views.my_account, name="my_account"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
