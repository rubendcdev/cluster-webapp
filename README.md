# Cluster Webapp - Plataforma de Gestión

Este proyecto es una aplicación web desarrollada en **Flask** diseñada para la gestión de asociaciones, cursos, casos de éxito y eventos. Proporciona una interfaz para usuarios públicos y un panel de administración para la gestión de la plataforma.

## 🚀 Características Principales

- **Gestión de Asociaciones**: Visualización y administración de asociaciones.
- **Cursos y Eventos**: Catálogo de cursos y gestión de eventos de la plataforma.
- **Casos de Éxito**: Publicación de historias de éxito y proyectos destacados.
- **Panel de Administración**: Gestión de contenido (galería, configuración del sitio) con diferentes roles de usuario (Super Admin, Admin, Asociado).
- **Autenticación Segura**: Integración con Flask-Login y cifrado de contraseñas.

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.11, Flask
- **Base de Datos**: MySQL 8
- **ORM**: Flask-SQLAlchemy, PyMySQL
- **Autenticación**: Flask-Login, Werkzeug Security
- **Migraciones**: Flask-Migrate
- **Entorno Virtual y Variables**: python-dotenv
- **Infraestructura**: Docker y Docker Compose

---

## 📁 Estructura del Proyecto

El proyecto sigue una arquitectura de patrón MVC, utilizando Flask Blueprints para modularizar los controladores.

```text
cluster-webapp/
│
├── app/
│   ├── controllers/      # Controladores y rutas (Flask Blueprints)
│   ├── models/           # Modelos de base de datos (SQLAlchemy)
│   ├── services/         # Lógica de negocio y utilidades
│   ├── static/           # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/        # Vistas HTML (Jinja2)
│
├── .env.example          # Plantilla de variables de entorno
├── run.py                # Punto de entrada de la aplicación
├── requirements.txt      # Dependencias de Python
├── create_super_admin.py # Script para crear el usuario administrador inicial
├── init_default_text.py  # Script para cargar textos por defecto
│
├── Dockerfile            # Configuración para contenedor de la app
└── docker-compose.yml    # Configuración de servicios Docker (App y BD)
```

---

## ⚙️ Configuración del Entorno (Variables)

Antes de ejecutar la aplicación (ya sea con Docker o configuración normal), debes definir tus variables de entorno iniciales.

1. Copia el archivo de ejemplo para crear el archivo real `.env`:
   ```bash
   cp .env.example .env
   ```
2. Configura los valores según sea necesario. Para desarrollo con Docker, el `DATABASE_URL` debe apuntar al nombre del servicio:
   ```env
   # .env
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=tu_clave_secreta_aqui
   
   # Para ejecución local con MySQL local:
   # DATABASE_URL=mysql+pymysql://root:password@localhost:3306/cluster_db
   
   # Para ejecución con Docker Compose (como está configurado aquí):
   DATABASE_URL=mysql+pymysql://root:rootpassword@cluster_mysql:3306/cluster_db
   ```

---

## 🐳 Arranque con Docker (Recomendado)

Utilizar **Docker** es la forma más rápida y consistente de arrancar el proyecto ya que configura automáticamente tanto la aplicación como su base de datos MySQL 8 asociada.

### 1️⃣ Construir y levantar contenedores
En la raíz del proyecto, ejecuta:
```bash
docker compose up --build
```
*(Puedes añadir `-d` al final para ejecutarlo en segundo plano).*

Esto iniciará:
- `cluster-webapp`: La aplicación Flask (Disponible en `http://localhost:5000`)
- `cluster_mysql`: La base de datos MySQL (con volumen persistente)

### 2️⃣ Acceso y comandos útiles
- Acceder a la app: **http://localhost:5000**
- Ver logs: `docker compose logs -f`
- Parar servicios: `docker compose down`
- Entrar a la base de datos (terminal):
  ```bash
  docker exec -it cluster_mysql mysql -u root -p
  ```

---

## 🐍 Arranque Normal con Python (Local)

Si prefieres no usar Docker, puedes ejecutar el proyecto directamente en tu máquina. **Necesitarás tener una instancia de MySQL corriendo localmente.**

### 1️⃣ Preparar el Entorno Virtual
Crea y activa un entorno virtual en la raíz del proyecto:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3️⃣ Configurar la Base de Datos
Asegúrate de que el `.env` tiene la conexión a tu MySQL local correcto:
```env
DATABASE_URL=mysql+pymysql://TU_USUARIO:TU_PASSWORD@localhost:3306/cluster_db
```
*Asegúrate de haber creado la base de datos `cluster_db` en tu gestor MySQL.*

### 4️⃣ Ejecutar la Aplicación
```bash
python run.py
```
*(Al iniciar por primera vez, SQLAlchemy creará las tablas automáticamente)*.

## 🛠️ Scripts Iniciales (Opcional)

Si es la primera vez que configuras la base de datos, puedes correr algunos scripts de inicialización de datos para que el sistema no esté vacío:

- Crear usuario administrador inicial: `python create_super_admin.py`
- Cargar textos por defecto del sitio: `python init_default_text.py`

*(Si usas Docker, puedes ejecutarlos desde dentro del contenedor: `docker exec -it cluster-webapp python create_super_admin.py`)*.
