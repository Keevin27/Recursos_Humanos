from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, date
from .models import Empleado
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.shortcuts import render,redirect
from .models import Solicitud
from .models import Ausencia,Empleado,Reporte
from django.contrib.auth.models import User
from datetime import date
from django.http import HttpResponse



# Create your views here.

def crearReporte(request):
    reportes = Reporte.objects.all()

    if request.method == 'GET':
        return render(request, 'reportes.html', {'reportes':reportes})
    
    else:
        descripcionReporte = request.POST.get('descripcion')
        if descripcionReporte == '':
            return JsonResponse({'status':'error','messagge':'agregue una descripcion'},status=400)
        else:
            if Reporte.objects.exists() == False:
                numReporte=1
                empleado=Empleado.objects.get(id=2)
                reporte = Reporte(numReporte=numReporte,descripcionReporte=descripcionReporte,empleado=empleado)
                reporte.save()
            
            else:
                num = Reporte.objects.all().order_by('numReporte').last()
                numReporte=num.numReporte + 1
                empleado=Empleado.objects.get(id=2)
                reporte = Reporte(numReporte=numReporte,descripcionReporte=descripcionReporte,empleado=empleado)
                reporte.save()
    return redirect('/reportes/')

@csrf_exempt
def eliminarReporte(request, reporte_id):
    if request.method == 'DELETE':
        try:
            reporte = Reporte.objects.get(id=reporte_id)
            reporte.delete()
            return JsonResponse({'message': 'Reporte eliminado correctamente'}, status=200)
        except Reporte.DoesNotExist:
            return JsonResponse({'error': 'Reporte no encontrado'}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

def crearAusencia(request):
    
    solicitudes=Solicitud.objects.all()
    
    if request.method == 'GET':
        return render(request, 'solicitud.html',{'solicitudes':solicitudes})
    
    else:
        motivoAusencia = request.POST['motivoAusencia']
        descripcion = request.POST.get('descripcion')
        fechaInicio = request.POST.get('fechaInicio')
        fechaFinal = request.POST.get('fechaFinal')
        # comprobante = request.FILES.get('comprobante ')
        
        
        if fechaInicio <= fechaFinal :
            ausencia = Ausencia(motivoAusencia= motivoAusencia, descripcion = descripcion, fechaInicio=fechaInicio,fechaFin=fechaFinal)
            ausencia.save()

            if Solicitud.objects.exists() == False:
                numSolicitud= 1
            else: 
                soli=Solicitud.objects.all().order_by('numSolicitud').last()
                numSolicitud=soli.numSolicitud+1
            
            empleado=Empleado.objects.get(id=2)
            solicitud= Solicitud(numSolicitud=numSolicitud,ausencia=ausencia,solicitante=empleado)
            solicitud.save()

        else:

            return JsonResponse({'status': 'error','message':'conflicto en fechas'}, status=400)
    return redirect('/ausencia/')  # Redirigir a la página de lista de solicitudes

# def ver_comprobante(request, numSolicitud):
#     solicitud = get_object_or_404(Solicitud, numSolicitud=numSolicitud)
#     comprobante_url = solicitud.ausencia.comprobante.url
#     return render(request, 'ver_comprobante.html', {'comprobante_url': comprobante_url})

def cambiar_estado(request):
    if request.method == "POST":
        registro_id = request.POST.get('registro_id')
        accion = request.POST.get('accion')

        if not registro_id or not accion:
            return JsonResponse({'status': 'error', 'message': 'Datos faltantes'}, status=400)

        try:
            registro_id = int(registro_id)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'ID de registro inválido'}, status=400)

        solicitud = get_object_or_404(Solicitud, numSolicitud=registro_id)
        solicitud.estadoSolicitud = accion
        solicitud.save()

        return JsonResponse({'status': 'success', 'new_state': solicitud.estadoSolicitud})
    else:
        return JsonResponse({'status': 'error'}, status=405)
    

def gestionarEmpleado(request):
    empleados = Empleado.objects.all()
    for empleado in empleados:
        empleado.edad = calcularEdad(empleado.fechaNacimineto)
    return render(request, 'gestionarEmpleado.html', {'empleados': empleados})

def calcularEdad(fechaNacimiento):
    hoy = date.today()
    return hoy.year - fechaNacimiento.year - ((hoy.month, hoy.day) < (fechaNacimiento.month, fechaNacimiento.day))

def eliminarEmpleado(request, empleadoId):
    empleado = get_object_or_404(Empleado, pk=empleadoId)
    usuario = empleado.user

    usuario.delete()
    return redirect('gestionar_empleado')

def actualizarEmpleado(request, empleadoId):
    empleado = get_object_or_404(Empleado, pk=empleadoId)
    if request.method == 'POST':
        try:
            empleado.nombre = request.POST['nombre']
            empleado.area = request.POST['area']
            empleado.telefono = request.POST['telefono']
            empleado.gradoAcademico = request.POST['gradoAcademico']
            empleado.sueldo = request.POST['sueldo']
            empleado.direccion = request.POST['direccion']
            empleado.nacionalidad = request.POST['nacionalidad']
            empleado.save()
            return redirect('gestionar_empleado')
        except ValueError:
            return render(request, 'ingresarEmpleado.html', {'empleado':empleado, 'error': "Error al actualizar los datos", 'es_creacion':False})
    return render(request, 'ingresarEmpleado.html', {'empleado': empleado, 'es_creacion':False})

def ingresarEmpleado(request):
    if request.method == 'GET':
        return render(request, 'ingresarEmpleado.html', {'es_creacion':True})
    else:
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        area = request.POST['area']
        telefono = request.POST['telefono']
        fechaNac = request.POST['fechaNacimiento']
        duui = request.POST['dui']
        gradoAcad = request.POST['gradoAcademico']
        sueldo = request.POST['sueldo']
        direccion = request.POST['direccion']
        sexo = request.POST['sexo']
        nacionalidad = request.POST['nacionalidad']
        codigo = generar_codigo_empleado(apellido, fechaNac)

        user = User.objects.create_user(username=codigo, password=codigo+'123')
        empleado = Empleado(codigo=codigo, nombre=nombre, apellido=apellido, area=area, telefono = telefono, fechaNacimineto =fechaNac, dui = duui, gradoAcademico=gradoAcad, sueldo =sueldo, direccion = direccion, sexo= sexo, nacionalidad = nacionalidad, user=user)
        empleado.save()
        user.save()
        login(request, user)
        return redirect('gestionar_empleado')

def generar_codigo_empleado(apellidos, fechaNacimiento):
    fecha_nac = datetime.strptime(fechaNacimiento, '%Y-%m-%d').date()
    apellido_list = apellidos.split()
    if len(apellido_list) < 2:
        iniciales = apellidos[:2].upper()
    else:
        iniciales = apellido_list[0][0].upper() + apellido_list[1][0].upper()
    ano_nacimiento = fecha_nac.year
    ano = str(ano_nacimiento)[-2:]
    numero = random.randint(100, 999)
    codigo = f"{iniciales}{ano}{numero}"
    while Empleado.objects.filter(codigo=codigo).count() > 0:
        numero = random.randint(100, 999)
        codigo = f"{iniciales}{ano}{numero}"
    
    return codigo

def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarSesion.html', {
            'form':AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'iniciarSesion.html', {
                'form':AuthenticationForm,
                'error': 'Usuario o contrasena son incorrectos' 
            })
        else:
            login(request, user)
            return redirect('gestionar_empleado')

def cerrarSesion(request):
    logout(request)
    return redirect('iniciar_sesion')