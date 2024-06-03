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
from myapp.views import iniciarSesion, cerrarSesion, ingresarEmpleado, gestionarEmpleado, actualizarEmpleado, eliminarEmpleado, gestionarBono, crearBono, actualizarBono, eliminarBono
from myapp.views import crearAusencia,cambiar_estado,crearReporte,eliminarReporte,planilla_view,actualizar_datos_empleado,administrarTitulo,Personal_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', iniciarSesion, name='iniciar_sesion'),
    path('cerrar_sesion/', cerrarSesion, name='cerrar_sesion'),
    path('gestionar_empleado/', gestionarEmpleado, name='gestionar_empleado'),
    path('gestionar_empleado/ingresar_empleado/', ingresarEmpleado, name='ingresar_empleado'),
    path('gestionar_empleado/actualizar_empleado/<empleadoId>', actualizarEmpleado, name='actualizar_empleado'),
    path('gestionar_empleado/eliminar_empleado/<empleadoId>', eliminarEmpleado, name="eliminar_empleado"),
    path('gestionar_bono/<empleadoId>', gestionarBono, name='gestionar_bono'),
    path('gestionar_bono/crear/<empleadoId>', crearBono, name='crear_bono'),
    path('gestionar_bono/actualizar/<empleadoId>/<bonoId>', actualizarBono, name='actualizar_bono'),
    path('gestionar_bono/eliminar/<empleadoId>/<bonoId>', eliminarBono, name='eliminar_bono'),
    path('gestionar_empleado/eliminar_empleado/<empleadoId>', eliminarEmpleado, name="eliminar_empleado"),
    path('ausencia/', crearAusencia),
    path('cambiar_estado/', cambiar_estado,name='cambiar_estado'),
    path('reportes/<empleadoId>/',crearReporte, name='crearReporte'),
    path('reportes/eliminar_reporte/<int:reporte_id>/',eliminarReporte, name='eliminar_reporte'),
    path('gestionar_empleado/planilla/',planilla_view,name='planilla'),
    path('actualizar_datos_empleado/', actualizar_datos_empleado, name='actualizar_datos_empleado'),
    path('gestionar_empleado/expediente/<int:empleadoId>/', Personal_view, name='expediente_empleado'),
    path('gestionar_empleado/expediente/<int:empleadoId>/administrarTitulo/', administrarTitulo, name='administrar_titulo'),
    
]
