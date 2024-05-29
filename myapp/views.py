from django.shortcuts import render,redirect
from .models import Solicitud
from .models import Ausencia,Empleado
from django.contrib.auth.models import User
from datetime import date



# Create your views here.
def crearAusencia(request):
    
    solicitudes=Solicitud.objects.all()
    
    if request.method == 'GET':
        return render(request, 'solicitud.html',{'solicitudes':solicitudes})
    
    else:
        motivoAusencia = request.POST['motivoAusencia']
        descripcion = request.POST.get('descripcion')
        fechaInicio = request.POST.get('fechaInicio')
        fechaFinal = request.POST.get('fechaFinal')
        
        if fechaInicio <= fechaFinal:
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

            redirect('/ausencia/')
    return redirect('/ausencia/')  # Redirigir a la página de lista de solicitudes


def cambiar_estado(request, id_registro):
    if request.method == 'POST':
        render()
        estado_nuevo = request.POST.get('accion')  # 'aprobado' o 'denegado'
        if estado_nuevo in ['Aprobada', 'Denegada']:
            registro = Solicitud.objects.get(numSolicitud=id_registro)
            registro.estadoSolicitud = estado_nuevo
            registro.save()
            return redirect('/ausencia/')
    else:
        return redirect('/ausencia/')
    return redirect('/ausencia/')  # Si hay algún problema o la petición no es POST