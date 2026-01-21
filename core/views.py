from django.shortcuts import render, redirect
from .models import Categoria, Voto, Nominado

def home(request):
    # Lógica para guardar votos (POST)
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('categoria_'):
                categoria_id = int(key.split('_')[1])
                nominado_id = int(value)
                categoria = Categoria.objects.get(id=categoria_id)
                nominado = Nominado.objects.get(id=nominado_id)
                
                
                #Guarda el voto (Asocia al usuario actual)#
                if request.user.is_authenticated:
                    Voto.objects.update_or_create(
                        usuario=request.user,
                        categoria=categoria,
                        defaults={'nominado': nominado}
                    )
        return redirect('home')

    categorias = Categoria.objects.prefetch_related('nominados').all()

    return render(request, 'core/home.html', {'categorias': categorias})