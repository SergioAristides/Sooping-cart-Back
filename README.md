# Demostración de un servicio web REST con FastAPI

## Instalación

Clonar el repositorio.

```
$ git clone https://github.com/jimezam/DemoFastAPI-guia.git

$ cd DemoFastAPI-guia
```

Crear el ambiente virtual.

```
$ python -m venv venv
```

Activar el ambiente virtual.

```
$ source venv/bin/activate
```

Instalar las librerías requeridas.

```
$ pip install -r requirements.txt
```

## Ejecutar el servidor

``` 
$ uvicorn main:app --reload
```

## Acceder a la documentación

Acceder al servicio a través de un navegador y una de las siguientes rutas.

 - http://localhost:8000/docs
 - http://localhost:8000/redoc