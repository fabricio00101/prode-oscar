from django.contrib import admin
from .models import Categoria, Nominado, Voto

class NominadoInLine(admin.TabularInline):
    model = Nominado
    extra = 5

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    inlines = [NominadoInLine]
    prepopulated_fields = {'slug': ('nombre',)}

admin.site.register(Voto)