from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Empleado(models.Model):
    codigo = models.CharField(max_length=7)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    area = models.CharField(max_length=25)
    telefono = models.CharField(max_length=9)
    fechaNacimineto = models.DateField()
    dui = models.CharField(max_length=10)
    gradoAcademico = models.CharField(max_length=50)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    direccion = models.TextField()
    sexo = models.CharField(max_length=9)
    nacionalidad = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Ausencia(models.Model):
    motivoAusencia = models.TextField()
    descripcion = models.TextField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField()


class Solicitud(models.Model):
    numSolicitud = models.IntegerField()
    fechaSolicitud = models.DateField(auto_now_add=True)
    estadoSolicitud = models.CharField(max_length=8)
    solicitante = models.ForeignKey(Empleado,on_delete=models.CASCADE)
    ausencia = models.ForeignKey(Ausencia, on_delete=models.CASCADE)

class ControlDeAusencia(models.Model):
    numeroDeAusencias = models.IntegerField()
    fecha = models.DateField()

class Planilla(models.Model):
    mes= models.DateField()
    anyo = models.DateField()



class DetallePlanilla(models.Model):
    sueldoNeto = models.DecimalField(max_digits=10, decimal_places=2)
    descuentoAfp = models.DecimalField(max_digits=10, decimal_places=2)
    descuentoIsss = models.DecimalField(max_digits=10, decimal_places=2)
    descuentoAusencia = models.DecimalField(max_digits=10, decimal_places=2)
    totalDescuentos = models.DecimalField(max_digits=10, decimal_places=2)
    horaExtraDia = models.DecimalField(max_digits=10, decimal_places=2)
    horaExtraNoche = models.DecimalField(max_digits=10, decimal_places=2)
    sueldoBruto = models.DecimalField(max_digits=10, decimal_places=2)
    empleado = models.ForeignKey(Empleado,on_delete=models.SET_NULL,null=True)
    planilla = models.ForeignKey(Planilla,on_delete=models.CASCADE)

class Reporte(models.Model):
    numReporte = models.IntegerField()
    descripcionReporte = models.TextField()
    fechaReporte = models.DateField(auto_now_add=True)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL,null=True)

class Bono(models.Model):
    codigo = models.CharField(max_length=6)
    justificacion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL,null=True)


class Usuario(models.Model):
    usuario = models.CharField(max_length=25)
    paswword = models.CharField(max_length=25)
    user = models.ForeignKey(User, on_delete=models.CASCADE)