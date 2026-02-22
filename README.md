# 🏆 Prode Oscars 2026

Una aplicación web interactiva desarrollada en Django para predecir los ganadores de los Premios de la Academia 2026. Los usuarios pueden registrarse, armar sus predicciones en distintas categorías y competir en una tabla de posiciones global.

## ✨ Características Principales

* **Sistema de Autenticación:** Registro de usuarios y login seguro nativo de Django.
* **Votación Inteligente:** * **Validación "Todo o Nada":** Los usuarios deben completar obligatoriamente todas las categorías para poder guardar sus predicciones.
  * **Seguridad de Voto:** Una vez enviado el formulario, las predicciones quedan bloqueadas (visualizadas con un candado) para evitar cambios de último momento.
* **Fecha Límite (Hard Deadline):** Cierre automático del sistema de votación configurado mediante `timezone` para el 15 de marzo de 2026 a las 20:00 hs.
* **Leaderboard Dinámico:** Tabla de posiciones en tiempo real que calcula los puntos automáticamente (1 acierto = 1 punto). Incluye criterio de desempate alfabético y buscador de usuarios.
* **Diseño UI/UX:** Interfaz moderna y responsiva estilo *Cinematic Dark & Gold* utilizando Tailwind CSS, con feedback visual (notificaciones toast, estados de error y éxito).

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3, Django 5.x
* **Base de Datos:** SQLite3 (ideal para despliegues locales y portabilidad)
* **Frontend:** HTML5, Tailwind CSS (vía CDN), Google Fonts (Be Vietnam Pro), Material Symbols.

---

## 🚀 Guía de Instalación Local

Sigue estos pasos para ejecutar el proyecto en tu computadora.

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/prode-oscar.git](https://github.com/TU_USUARIO/prode-oscar.git)
cd prode-oscar
```

### 2. Crear y activar el Entorno Virtual
Es una buena práctica aislar las dependencias del proyecto.

**En Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```
*(Nota: Si usas Git Bash en Windows, el comando es `source venv/Scripts/activate`)*

**En Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar las dependencias
Con el entorno virtual activado, instala Django y demás librerías necesarias:
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
Ejecuta las migraciones para generar el archivo `db.sqlite3` y las tablas necesarias:
```bash
python manage.py migrate
```

### 5. Ejecutar el Servidor
Inicia el servidor de desarrollo de Django:
```bash
python manage.py runserver
```
Visita `http://127.0.0.1:8000/` en tu navegador para ver la página y comenzar a jugar.

---

## 🎮 ¿Cómo funciona el juego?

1. **Configuración Inicial:** El Administrador carga las Categorías (ej: "Mejor Película") y los Nominados, asociando sus pósters oficiales.
2. **Participación:** Los jugadores se registran, ingresan al Home y seleccionan a sus favoritos. Deben votar en todas las categorías para que el sistema acepte la boleta.
3. **Cierre:** El sistema cierra automáticamente la votación en la fecha límite programada.
4. **Resultados:** Durante la ceremonia, el Administrador marca a los ganadores en el sistema.
5. **Ranking:** El Leaderboard actualiza los puntajes instantáneamente, mostrando quién acertó más ganadores.

---

## 📂 Estructura del Proyecto

```text
prode_oscar/
│
├── config/                 # Configuración principal de Django (settings, urls)
├── core/                   # Aplicación principal del juego
│   ├── models.py           # Modelos de BD (Categoria, Nominado, Voto)
│   ├── views.py            # Lógica de negocio (Validaciones, Deadline, Ranking)
│   └── templates/
│       ├── core/           # Plantillas del juego (home.html, leaderboard.html)
│       └── registration/   # Plantillas de autenticación (login.html, registro.html)
├── db.sqlite3              # Base de datos local
├── requirements.txt        # Lista de dependencias
└── manage.py               # Script de gestión de Django
```

---

*Desarrollado para los Oscars 2026.* 🍿🎬