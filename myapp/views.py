from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import datetime, date
from .models import Empleado, Bono
import random, string
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
@login_required
def gestionarEmpleado(request):
    empleados = Empleado.objects.all()
    for empleado in empleados:
        empleado.edad = calcularEdad(empleado.fechaNacimineto)
    return render(request, 'gestionarEmpleado.html', {'empleados': empleados})

def calcularEdad(fechaNacimiento):
    hoy = date.today()
    return hoy.year - fechaNacimiento.year - ((hoy.month, hoy.day) < (fechaNacimiento.month, fechaNacimiento.day))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminarEmpleado(request, empleadoId):
    empleado = get_object_or_404(Empleado, pk=empleadoId)
    usuario = empleado.user

    usuario.delete()
    return redirect('gestionar_empleado')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def actualizarEmpleado(request, empleadoId):
    empleado = get_object_or_404(Empleado, pk=empleadoId)
    nacionalidad=empleado.nacionalidad
    if request.method == 'POST':
        try:
            empleado.nombre = request.POST['nombre']
            empleado.area = request.POST['area']
            empleado.telefono = request.POST['telefono']
            empleado.gradoAcademico = request.POST['gradoAcademico']
            empleado.sueldo = request.POST['sueldo']
            empleado.direccion = request.POST['direccion']
            empleado.nacionalidad = request.POST['nacionalidad']
            empleado.dui = request.POST['dui']
            empleado.save()
            return redirect('gestionar_empleado')
        except ValueError:
            return render(request, 'ingresarEmpleado.html', {'empleado':empleado, 'error': "Error al actualizar los datos", 'es_creacion':False})
    return render(request, 'ingresarEmpleado.html', {'empleado': empleado, 'es_creacion':False, 'nacionalidad':nacionalidad})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def ingresarEmpleado(request):
    if request.method == 'GET':
        return render(request, 'ingresarEmpleado.html', {'es_creacion':True})
    else:
        try:
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
            print (request.POST['nombre'])

            user = User.objects.create_user(username=codigo, password=codigo+'123')
            empleado = Empleado(codigo=codigo, nombre=nombre, apellido=apellido, area=area, telefono = telefono, fechaNacimineto =fechaNac, dui = duui, gradoAcademico=gradoAcad, sueldo =sueldo, direccion = direccion, sexo= sexo, nacionalidad = nacionalidad, user=user)
            empleado.save()
            user.save()
            return redirect('gestionar_empleado')
        except:
            return render(request, 'ingresarEmpleado.html', {'es_creacion':True, 'error': 'Datos no validos'})

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

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('iniciar_sesion')

@login_required
def gestionarBono(request, empleadoId):
    bonos = Bono.objects.all()
    empleado = get_object_or_404(Empleado, pk = empleadoId)
    return render(request, 'gestionarBono.html', {'bonos':bonos, 'empleado':empleado})

def generate_code(length=6):
    characters = string.ascii_uppercase + string.digits
    codigo = ''.join(random.choices(characters, k=length))
    while Bono.objects.filter(codigo = codigo).count() > 0:
        codigo = ''.join(random.choices(characters, k=length))
    
    return codigo

@login_required
@user_passes_test(lambda u: u.is_superuser)
def actualizarBono(request, empleadoId, bonoId):
    bono = get_object_or_404(Bono, pk = bonoId)
    url = reverse('gestionar_bono', args=[empleadoId])
    if request.method == 'POST':
        try:
            bono.justificacion = request.POST['justificacion']
            bono.monto = request.POST['montoBono']
            bono.save()
            return redirect(url)
        except:
            return redirect(url)
    return redirect(url)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crearBono(request, empleadoId):
    if request.method == 'GET':
        return redirect('gestionar_bono/{empleadoId}')
    else:
        try:
            empleado = get_object_or_404(Empleado, pk=empleadoId)
            codigo = generate_code()
            justificacion = request.POST['justificacion']
            monto = request.POST['montoBono']
            bono = Bono(codigo = codigo, justificacion=justificacion, monto=monto, empleado=empleado)
            bono.save()
            return redirect('/gestionar_bono/'+empleadoId)
        except:
            return redirect('/gestionar_bono/'+empleadoId)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminarBono(request, empleadoId, bonoId):
    bono = get_object_or_404(Bono, pk = bonoId)
    url = reverse('gestionar_bono', args=[empleadoId])
    if request.method == 'POST':
        bono.delete()
    return redirect(url)

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)