# Proyecto Docker Compose con FastAPI y Base de Datos

API CRUD desarrollada con FastAPI y Docker Compose, utilizando PostgreSQL como base de datos.

## Requisitos Previos

- Docker instalado
- Docker Compose instalado

## Instalación y Ejecución

### 1. Construir y ejecutar los contenedores

```bash
docker compose up --build
```

Este comando construirá la imagen de la aplicación y levantará ambos contenedores (aplicación y base de datos).

### 2. Verificar que los servicios están corriendo

```bash
docker compose ps
```

### 3. Ver los logs

```bash
# Ver todos los logs
docker compose logs

# Ver logs de un servicio específico
docker compose logs app
docker compose logs db
```

### 4. Detener los contenedores

```bash
docker compose down
```

### 5. Detener y eliminar volúmenes (elimina los datos)

```bash
docker compose down -v
```

## Endpoints de la API

Una vez que la aplicación esté corriendo, estará disponible en `http://localhost:8080`

### TODO: Documentar endpoints

- `GET /estudiantes` - Lista todas las entidades
- `GET /estudiantes/{id}` - Obtiene una entidad por ID
- `POST /estudiantes` - Crea una nueva entidad
- `DELETE /estudiantes/{id}` - Elimina una entidad por ID

## Documentación Interactiva

- **Swagger UI**: `http://localhost:8080/docs`
- **ReDoc**: `http://localhost:8080/redoc`

## Estructura del Proyecto

- `docker-compose.yml`: Configuración de servicios y red
- `Dockerfile`: Configuración de la imagen de la aplicación
- `main.py`: Código de la aplicación FastAPI
- `requirements.txt`: Dependencias de Python

## Notas

- Los datos de la base de datos persisten en un volumen de Docker
- Los contenedores se comunican a través de una red personalizada
- El puerto 8080 está expuesto al host para acceder a la API
