from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal, ROUND_HALF_UP
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
    horaExtraDia = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,default=0.0)
    horaExtraNoche = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True,default=0.0)
    monto_total_bonos = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    def total_ingresos(self):
        sueldo = float(self.sueldo)
        hora_extra_diurna = float(self.horaExtraDia * Decimal('1.5')) if self.horaExtraDia is not None else 0.0
        hora_extra_nocturna = float(self.horaExtraNoche * Decimal('2')) if self.horaExtraNoche is not None else 0.0
        total_ingresos = sueldo + hora_extra_diurna + hora_extra_nocturna
        return total_ingresos

    def iss(self):
        return float(self.sueldo * Decimal('0.03'))

    def afp(self):
        return float(self.sueldo * Decimal('0.0725'))

    def renta_mensual(self):
        return float((self.sueldo - Decimal(self.iss()) - Decimal(self.afp())) * Decimal('0.1'))

    def total_descuentos(self):
        return float(self.iss() + self.afp() + self.renta_mensual())

    def sueldo_neto(self):
        return float(self.total_ingresos() - self.total_descuentos())
    
    

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.codigo}"

class Ausencia(models.Model):
  
    motivoAusencia = models.CharField(max_length=50)
    descripcion = models.TextField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    comprobante = models.ImageField(upload_to='comprobantes/', null=True, blank=True)

class Solicitud(models.Model):
   
    numSolicitud = models.IntegerField()
    fechaSolicitud = models.DateField(auto_now_add=True)
    estadoSolicitud = models.CharField(max_length=20, default='revision')
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

class Titulo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,related_name='titulos',default=1)
    tipo = models.CharField(max_length=100)
    nombre_especialidad = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    anio_titulacion = models.IntegerField()

    def __str__(self):
      return f"{self.tipo} - {self.nombre_especialidad} ({self.anio_titulacion})"