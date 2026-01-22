from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Categoria, Voto, Nominado
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
            
        votos_guardados = False
        
        for key, value in request.POST.items():
            if key.startswith('categoria_'):
                categoria_id = int(key.split('_')[1])
                nominado_id = int(value)
                
                categoria = Categoria.objects.get(id=categoria_id)
                nominado = Nominado.objects.get(id=nominado_id)
                
                # BLINDAJE 1: Solo guardamos si NO existe un voto previo en esta categoría
                if not Voto.objects.filter(usuario=request.user, categoria=categoria).exists():
                    Voto.objects.create(
                        usuario=request.user,
                        categoria=categoria,
                        nominado=nominado
                    )
                    votos_guardados = True
        
        if votos_guardados:
            messages.success(request, '¡Tus predicciones se han guardado correctamente!')
        else:
            # Si intentó votar pero no se guardó nada (ej: intentó hackear el HTML para cambiar voto)
            messages.info(request, 'No se realizaron cambios (las categorías votadas están bloqueadas).')
            
        return redirect('home')

    # --- Lógica GET ---
    categorias = Categoria.objects.prefetch_related('nominados').all()
    puntos = 0
    votos_ids = []           # IDs de los nominados (para marcar el check)
    categorias_votadas_ids = [] # IDs de las categorías (para bloquear el grupo entero)
    
    if request.user.is_authenticated:
        puntos = Voto.objects.filter(usuario=request.user, nominado__es_ganador=True).count()
        
        # Recuperamos los votos del usuario
        votos_usuario = Voto.objects.filter(usuario=request.user)
        votos_ids = list(votos_usuario.values_list('nominado_id', flat=True))
        categorias_votadas_ids = list(votos_usuario.values_list('categoria_id', flat=True))

    return render(request, 'core/home.html', {
        'categorias': categorias, 
        'puntos': puntos,
        'votos_ids': votos_ids,
        'categorias_votadas_ids': categorias_votadas_ids # <--- Nueva variable enviada al HTML
    })

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

    query = request.GET.get('q')
    # Calcular puntaje para todos los usuarios
    # Esto cuenta cuántos votos tiene cada usuario donde el nominado es ganador
    usuarios = User.objects.annotate(
        aciertos=Count('voto', filter=Q(voto__nominado__es_ganador=True))
    ).order_by('-aciertos')

    if query:
        usuarios = usuarios.filter(username__contains=query)
    
    return render(request, 'core/leaderboard.html', {'usuarios': usuarios})