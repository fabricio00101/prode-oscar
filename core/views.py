from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Categoria, Voto, Nominado

def home(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login') # Obligar a loguearse para votar
            
        for key, value in request.POST.items():
            if key.startswith('categoria_'):
                categoria_id = int(key.split('_')[1])
                nominado_id = int(value)
                categoria = Categoria.objects.get(id=categoria_id)
                nominado = Nominado.objects.get(id=nominado_id)
                
                Voto.objects.update_or_create(
                    usuario=request.user,
                    categoria=categoria,
                    defaults={'nominado': nominado}
                )
        return redirect('home')

    categorias = Categoria.objects.prefetch_related('nominados').all()
    
    # Calcular puntos del usuario actual para mostrar en el header
    puntos = 0
    if request.user.is_authenticated:
        puntos = Voto.objects.filter(usuario=request.user, nominado__es_ganador=True).count()

    return render(request, 'core/home.html', {'categorias': categorias, 'puntos': puntos})

def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        email = request.POST.get('email')
        clave = request.POST.get('password')
        
        # Validación simple
        if User.objects.filter(username=usuario).exists():
            return render(request, 'registration/registro.html', {'error': 'El usuario ya existe'})
        
        # Crear usuario
        user = User.objects.create_user(username=usuario, email=email, password=clave)
        login(request, user)
        return redirect('home')
    
    return render(request, 'registration/registro.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def leaderboard(request):
    # Calcular puntaje para todos los usuarios
    # Esto cuenta cuántos votos tiene cada usuario donde el nominado es ganador
    usuarios = User.objects.annotate(
        aciertos=Count('voto', filter=Q(voto__nominado__es_ganador=True))
    ).order_by('-aciertos')
    
    return render(request, 'core/leaderboard.html', {'usuarios': usuarios})