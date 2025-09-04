# 🐾 Clinica Veterinaria Backend API

## Descripción

Este es el backend de la aplicación **Clinica Veterinaria**, desarrollado con **FastAPI**. Proporciona una API RESTful para gestionar información relacionada con pacientes, citas, médicos y más, facilitando la administración de una clínica veterinaria.

## Tecnologías Utilizadas

```

- **FastAPI**: Framework web moderno y de alto rendimiento para construir APIs con Python 3.6+.
- **Python 3.10+**: Lenguaje de programación utilizado para el desarrollo del backend.
- **Supabase**: Plataforma de backend como servicio que proporciona una base de datos PostgreSQL, autenticación, almacenamiento y funciones en tiempo real.
- **python-dotenv**: Carga de variables de entorno desde un archivo `.env`.
- **python-jose**: Biblioteca para trabajar con JSON Web Tokens (JWT) y autenticación.
- **Uvicorn**: Servidor ASGI para ejecutar aplicaciones FastAPI.

```

## Estructura del Proyecto
Clinica-Veterinaria-Backend/
```
├── app/
│   ├── main.py              # Punto de entrada de la aplicación FastAPI
│   ├── models/              # Modelos de datos y esquemas Pydantic
│   ├── routers/             # Rutas y controladores de la API
│   └── services/            # Lógica de negocio y servicios
├── .env                     # Variables de entorno (no incluir en el repositorio)
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación del proyecto

```


## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/M41k80/Clinica-Veterinaria-Backend-
   cd Clinica-Veterinaria-Backend-
   ```

2.	Crea y activa un entorno virtual:
   ```
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3.	Instala las dependencias:

   ```
    pip install -r requirements.txt
   ```

4.	Configura las variables de entorno:
Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

```
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
SECRET_KEY=una_clave_secreta_para_jwt

```

Uso

Para ejecutar la aplicación en modo de desarrollo:

```
uvicorn app.main:app --reload
```

La API estará disponible en http://localhost:8000. La documentación interactiva se puede acceder en http://localhost:8000/docs.


## Endpoints Principales
	•	GET /patients/: Obtiene la lista de pacientes.
	•	POST /patients/: Crea un nuevo paciente.
	•	GET /appointments/: Obtiene la lista de citas.
	•	POST /appointments/: Crea una nueva cita.

# Contribuciones

### Las contribuciones son bienvenidas. Si deseas colaborar, por favor sigue estos pasos:
	1.	Haz un fork del repositorio.
	2.	Crea una rama para tu característica (git checkout -b feature/nueva-caracteristica).
	3.	Realiza tus cambios y haz commit (git commit -am 'Añadir nueva característica').
	4.	Haz push a tu rama (git push origin feature/nueva-caracteristica).
	5.	Abre un pull request.

# Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
