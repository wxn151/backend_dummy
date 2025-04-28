# App back-end (con FastAPI)

Back-end básico construido con FastAPI y autenticación, ideal como base para una aplicación full-stack moderna.

🔗 Demo: https://behemoth-backend.onrender.com/

---

## 👾 Funcionalidades

- Confirmación por correo y recuperación de contraseña vía SMTP (es posible desactivarlo).
- Autenticación con JWT y OAuth2 (session).
- Migración con Alembic (PostgreSQL).
- Cargar articulos favoritos y eliminarlos.

---

## 🛠️ Iniciar sin Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/wxn151/backend_dummy.git
cd back_dummy
```

### 2. Crear y activar el entorno virtual

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear archivo `.env`

Crear un archivo `.env` en la raíz del proyecto con las variables necesarias (ver plantilla al final del documento).
En caso de que el servidor SMTP no lo necesites, define SMTP_CONFIGURATION=deactivate.

### 5. Migracion (con Alembic)

```bash
# Linux / windows 
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### 6. Ejecutar la aplicación

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## 🐳 Iniciar con Docker

### 1. Editar archivo `.env`

Asegurate de incluir también las siguientes variables para Docker:

```env
DATABASE_URL=postgresql://postgres:tu_password@db:5432/tu_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=tu_db
```

### 2. Construir y correr contenedores

Es necesario tener ejecutandose Docker, previo a correr los comandos

```bash
docker compose build
# iniciar el docker
docker compose up -d
```

### 3. Migracion

```bash
docker compose exec backend alembic revision --autogenerate -m "initial"
docker compose exec backend alembic upgrade head
```

### 4. Detener contenedores (opcional)

```bash
# shutdown
docker compose down
```

---

## 🗃️ Documentación

Swagger UI disponible en:

```txt
http://localhost:8000/docs
```

---

## Contribuciones

¿Ideas, errores o mejoras? ¡Son bienvenidas! Abrí un issue o un pull request.

---

## Licencia

MIT – [Ver licencia](https://opensource.org/licenses/MIT)

---

## 📄 Plantilla `.env`

```env
# Info general
TITLE=Behemoth Backend
DESCRIPTION=Documentación de la API

# Base de datos
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/tu_db

# Seguridad
SECRET_KEY=clave_secreta
ALGORITHM=HS256

# SMTP
MAIL=correo@tudominio.com
PASSWORD=contraseña_correo

# Enlaces del front-end
RESET_LINK=https://tu-frontend.com

# STMP opcional (en caso de que desees tener activo el servicio de SMTP, define como activate)
SMTP_CONFIGURATION=deactivate

# Variables Docker
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=tu_db
```
