from django.urls import path
from . import views # import de la vista 
from django.urls import path, include  # librerias nesesarias para hacer la referencia desde url.py del proyecto 

urlpatterns = [
  path('',views.home,name="home"), # vista home 

]
