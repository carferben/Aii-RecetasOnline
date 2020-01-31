from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator

class Categoria(models.Model):
    categoria_id = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)

class Receta(models.Model):
    id_receta = models.IntegerField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    pdf_url = models.CharField(max_length=255)
    dificultad = models.CharField(max_length=255)
    cocina = models.CharField(max_length=255)
    vegetariana = models.CharField(max_length=2000)
    celiacos = models.CharField(max_length=2000)
    foto = models.CharField(max_length=2000)
    ingredientes = models.CharField(max_length=2000)
    pasos = models.CharField(max_length=2000)

class Usuario(models.Model):
    choices = [("m", "M"), ("f", "F")]
    id_usuario = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1,choices=choices)     

class Valoracion(models.Model):
    puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)