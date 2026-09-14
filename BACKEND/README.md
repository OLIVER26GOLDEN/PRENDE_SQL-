# PRENDE_SQL — Backend (FastAPI + SQLAlchemy + MySQL)

API para el login y guardado de progreso de PRENDE_SQL.

## 🐳 Arrancarlo con Docker (recomendado)

Esto evita instalar Python, MySQL, crear entornos virtuales, etc. — todo corre en contenedores aislados con las versiones exactas que ya sabemos que funcionan. Solo necesitas tener [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.

```bash
cp .env.docker.example .env
# edita .env y pon tu propia contraseña de MySQL y tu SECRET_KEY

docker compose up --build
```

Eso levanta dos contenedores: uno con MySQL (con los datos guardados de forma persistente en un volumen, no se pierden al reiniciar) y otro con la API. La primera vez tarda un poco más porque descarga las imágenes y construye el contenedor del backend.

Cuando veas en la terminal algo como:
```
backend-1  | [startup] Conectado a la base de datos (intento 1).
backend-1  | INFO:     Application startup complete.
```
ya está listo en **http://localhost:8000/docs**

Para pararlo: `Ctrl+C`, o en otra terminal `docker compose down` (los datos de MySQL se conservan; usa `docker compose down -v` solo si quieres borrarlos también).

**Nota sobre el puerto de MySQL**: el contenedor de MySQL escucha en el puerto `3307` de tu PC (no el `3306` habitual), para no chocar con un MySQL que ya tengas instalado localmente. Si quieres conectarte a esa base de datos desde MySQL Workbench para inspeccionarla, usa `localhost:3307`.

---

## Endpoints

| Método | Ruta             | Auth | Descripción                          |
|--------|------------------|------|---------------------------------------|
| POST   | `/auth/register` | No   | Crea usuario, devuelve JWT           |
| POST   | `/auth/login`    | No   | Login, devuelve JWT                  |
| GET    | `/auth/me`       | Sí   | Datos del usuario logueado           |
| GET    | `/progress`      | Sí   | Progreso guardado (xp, racha, niveles) |
| PUT    | `/progress`      | Sí   | Guarda/actualiza el progreso         |

Auth = header `Authorization: Bearer <token>`.

## Alternativa: correrlo sin Docker (Python + MySQL locales)

```bash
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edita .env con tu usuario/password de MySQL y una SECRET_KEY tuya
```

Crea la base de datos vacía en MySQL antes de arrancar (las tablas las crea la app solas):

```sql
CREATE DATABASE prende_sql CHARACTER SET utf8mb4;
```

Arranca el servidor:

```bash
uvicorn app.main:app --reload --port 8000
```

Documentación interactiva (Swagger) en: http://localhost:8000/docs

## Desplegarlo en un hosting

Sirve para cualquier proveedor que corra Python (Railway, Render, PythonAnywhere, un VPS con Docker/nginx, etc.). Los pasos generales son siempre los mismos:

1. Sube este proyecto a un repo de GitHub.
2. Crea una base de datos MySQL en el hosting (muchos proveedores la ofrecen ya integrada, p.ej. Railway/Render tienen "MySQL/PostgreSQL add-on").
3. Configura las variables de entorno en el panel del hosting (no subas el `.env` real al repo):
   - `DATABASE_URL` → cadena de conexión que te dé el hosting
   - `SECRET_KEY` → una clave larga y aleatoria (genera una con `openssl rand -hex 32`)
   - `ALLOWED_ORIGINS` → el dominio donde sirvas el HTML del frontend, ej. `https://tudominio.com`
4. Comando de arranque en el hosting: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Con Docker (Railway, Render y la mayoría de hostings lo detectan solos):** como ya tienes el `Dockerfile`, muchos hostings (Railway, Render, Fly.io) detectan automáticamente que el repo tiene uno y lo usan para desplegar sin que tengas que configurar nada de "comando de arranque" — simplemente conectas el repo y ellos construyen la imagen. Solo tienes que rellenar las variables de entorno (`DATABASE_URL`, `SECRET_KEY`, `ALLOWED_ORIGINS`) en su panel.

5. Una vez desplegado, tendrás una URL tipo `https://tu-backend.up.railway.app`. Esa URL es la que hay que poner como `API_BASE_URL` en el HTML del frontend (`sql_trainer.html`, al principio del `<script>`).

## Notas de seguridad

- Las contraseñas se guardan con hash `bcrypt`, nunca en texto plano.
- El JWT expira a los 7 días (`ACCESS_TOKEN_EXPIRE_MINUTES` en `app/auth.py`).
- Cambia `SECRET_KEY` por una clave propia antes de desplegar — la del `.env.example` es solo un placeholder.
