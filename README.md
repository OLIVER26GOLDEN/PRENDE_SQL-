# PRENDE_SQL-
# 🐘 PRENDE_SQL

**API REST en FastAPI para aprender SQL de forma progresiva e interactiva.**
100 ejercicios reales, corregidos automáticamente, desde `SELECT` básico hasta *window functions* — con motor de ejecución en SQLite y sistema de XP/progreso.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-in--memory-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/status-en%20desarrollo-yellow)

---

## 📖 ¿Qué es esto?

PRENDE_SQL es el backend de una plataforma de práctica de SQL: en vez de leer teoría, el usuario escribe consultas reales contra datos reales (basados en Sakila, World y Northwind) y recibe corrección instantánea, explicación de la solución y progreso gamificado (XP, rachas, certificados por nivel).

Este repositorio contiene **solo el backend** (API REST), diseñado para conectarse a cualquier frontend (web, móvil, CLI...).

## ✨ Características

- **100 niveles** organizados en **10 unidades progresivas**:
  `SELECT` → `WHERE` → `ORDER BY / LIMIT` → `GROUP BY` → `HAVING` → `JOIN` → `LEFT JOIN` → Subconsultas → CTEs (`WITH`) → *Window functions*
- **Motor de ejecución real**: cada consulta se ejecuta contra una base de datos SQLite en memoria, aislada por petición.
- **Corrección automática**: compara el resultado del usuario contra la solución esperada (ignorando orden de columnas, y de filas salvo que la consulta use `ORDER BY`).
- **Sistema de progreso**: XP por nivel superado, rachas, y 3 certificados por tramo (Básico / Intermedio / Profesional).
- **Modo práctica libre**: repite niveles ya completados o cualquiera al azar.
- **Asistente**: desglose de las cláusulas SQL usadas en la solución de cada ejercicio.
- **Stateless**: no persiste usuarios; el progreso se envía y devuelve en cada petición, listo para integrarse con tu propio sistema de auth/DB.

## 🛠️ Stack técnico

| Componente        | Tecnología          |
|--------------------|---------------------|
| Framework API      | FastAPI             |
| Validación de datos| Pydantic v2         |
| Motor de ejercicios| SQLite (`:memory:`) |
| Servidor ASGI      | Uvicorn             |

## 🚀 Instalación y uso

```bash
git clone https://github.com/OLIVER26GOLDEN/PRENDE_SQL.git
cd PRENDE_SQL

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Documentación interactiva (Swagger) disponible en:
👉 `http://localhost:8000/docs`

## 📡 Endpoints principales

| Método | Endpoint                       | Descripción                                      |
|--------|---------------------------------|---------------------------------------------------|
| GET    | `/api/units`                   | Lista de las 10 unidades temáticas                |
| GET    | `/api/levels`                  | Resumen de los 100 niveles                        |
| GET    | `/api/levels/{id}`             | Detalle de un nivel (enunciado, pista, esquema)   |
| POST   | `/api/levels/{id}/run`         | Ejecuta y corrige una consulta SQL                |
| POST   | `/api/practice/random`         | Nivel aleatorio para práctica libre               |
| GET    | `/api/assistant/{id}`          | Explicación de la solución de un nivel            |
| POST   | `/api/certificates/check`      | Progreso hacia los 3 certificados                 |

### Ejemplo: corregir una consulta

```bash
curl -X POST http://localhost:8000/api/levels/0/run \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT title, rating FROM film"}'
```

## 📂 Estructura del proyecto
