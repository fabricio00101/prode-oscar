from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100) #Ej: Mejor película
    slug = models.SlugField(unique=True) #Para la URL

    def __str__(self):
        return self.nombre
    
class Nominado(models.Model):
    categoria = models.ForeignKey(Categoria, related_name='nominados', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200) #Ej: Marty Supreme
    detalle = models.CharField(max_length=200, blank=True) #Ej: Josh Safdie

    poster_url = models.URLField(blank=True, null=True)

    es_ganador = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"
    
class Voto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nominado = models.ForeignKey(Nominado, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta: 
        unique_together = ('usuario', 'categoria') # Un usuario, un voto por categoría

    def __str__(self):
        return f"{self.usuario.username} votó por {self.nominado.nombre}"
