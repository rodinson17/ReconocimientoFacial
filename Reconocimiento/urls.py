"""Reconocimiento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ReconocimientoFacial import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('listado-estudiantes', views.all_students, name="all_students"),
    path('registrar-estudiante', views.register_student, name="register_student"),
    path('agregar-libro', views.add_book, name="add_book"),
    path('actualizar-libro/<id>', views.update_book, name="update_book"),
    path('eliminar-libro/<id>', views.remove_book, name="remove_book"),
    path('listado-libros/<msg>', views.all_books, name="all_books"),
    path('historial-prestamos', views.loan_history, name="loan_history"),
    path('prestar-libros/<identification>', views.lend_books, name="lend_books"),
    path('deudas', views.deudas, name="deudas"),
    path('informacion-estudiante', views.capture_faces, name="capture_faces"),
    path('guardar-prestamo', views.action_modal, name="action_modal"),
    path('entrenar-red-neuronal', views.train_neural_network_for_recognition, name="train_neural_network_for_recognition"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
