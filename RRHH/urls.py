"""
URL configuration for RRHH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myapp.views import iniciarSesion, cerrarSesion, ingresarEmpleado, gestionarEmpleado, actualizarEmpleado, eliminarEmpleado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iniciarSesion, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrarSesion, name='cerrar_sesion'),
    path('gestionar_empleado/', gestionarEmpleado, name='gestionar_empleado'),
    path('gestionar_empleado/ingresar_empleado/', ingresarEmpleado, name='ingresar_empleado'),
    path('gestionar_empleado/actualizar_empleado/<empleadoId>', actualizarEmpleado, name='actualizar_empleado'),
    path('gestionar_empleado/eliminar_empleado/<empleadoId>', eliminarEmpleado, name="eliminar_empleado")
]
