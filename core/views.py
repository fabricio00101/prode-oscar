from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Categoria, Voto, Nominado
from django.contrib import messages
from django.utils import timezone
import datetime

def home(request):

    FECHA_LIMITE = timezone.make_aware(datetime.datetime(2026, 3, 15, 20, 0))
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        

        if timezone.now() > FECHA_LIMITE:
            messages.error(request, "La votación ya ha cerrado.")
            return redirect('home')
        
        # 1. Contamos cuántas categorías existen en total
        total_categorias = Categoria.objects.count()
        
        # 2. Contamos cuántos votos llegaron en este formulario
        # (Filtramos solo las claves que empiezan con 'categoria_')
        votos_enviados = len([k for k in request.POST if k.startswith('categoria_')])
        
        # 3. Comparamos: Si envió menos votos que el total de categorías...
        if votos_enviados < total_categorias:
            messages.error(request, f"Error: Debes votar en TODAS las {total_categorias} categorías para poder guardar.")
            return redirect('home') # <--- Rechazamos y devolvemos al usuario
        # --------------------------------------------

        votos_guardados = False
        
        for key, value in request.POST.items():
            if key.startswith('categoria_'):
                categoria_id = int(key.split('_')[1])
                nominado_id = int(value)
                
                categoria = Categoria.objects.get(id=categoria_id)
                nominado = Nominado.objects.get(id=nominado_id)
                
                # BLINDAJE: Solo guardamos si NO existe un voto previo
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
            messages.info(request, 'No se realizaron cambios (las categorías votadas ya están registradas).')
            
        return redirect('home')

    # --- Lógica GET ---
    categorias = Categoria.objects.prefetch_related('nominados').all()
    puntos = 0
    votos_ids = []
    categorias_votadas_ids = []
    
    if request.user.is_authenticated:
        puntos = Voto.objects.filter(usuario=request.user, nominado__es_ganador=True).count()
        votos_usuario = Voto.objects.filter(usuario=request.user)
        votos_ids = list(votos_usuario.values_list('nominado_id', flat=True))
        categorias_votadas_ids = list(votos_usuario.values_list('categoria_id', flat=True))

    return render(request, 'core/home.html', {
        'categorias': categorias, 
        'puntos': puntos,
        'votos_ids': votos_ids,
        'categorias_votadas_ids': categorias_votadas_ids
    })
def registro(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        email = request.POST.get('email')
        clave = request.POST.get('password')
        
        # Validación: Si el usuario ya existe
        if User.objects.filter(username=usuario).exists():
            return render(request, 'registration/registro.html', {
                'error': 'El usuario ya existe',
                'username_previo': usuario, # <--- Devolvemos el nombre
                'email_previo': email       # <--- Devolvemos el email
            })
        
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
    
    # Agregamos 'username' como segundo criterio de orden (desempate)
    usuarios = User.objects.annotate(
        aciertos=Count('voto', filter=Q(voto__nominado__es_ganador=True))
    ).order_by('-aciertos', 'username') # <--- Orden: Primero aciertos, luego nombre

    if query:
        usuarios = usuarios.filter(username__icontains=query)
    
    return render(request, 'core/leaderboard.html', {'usuarios': usuarios})