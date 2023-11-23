# pokemonVisiotech

Esta es el desarrollo de la prueba técnica de la empresaVisiotech, la cual consiste en un pequeño simulador de Pokemon.

## Instalación

El proyecto se ha desarrollado en python versión 3.10, con base de datos mysql. Para instalar las librerias de python necesarias, sería necesario ejecutar los siguientes comandos:

- pip install mysql-connector-python 

## Parte 1

Para el desarrollo de esta parte se ha optado por un enfoque sencillo, sin utilizar aun bases de datos ni estructuras de datos complejas.
El código se compone de los siguientes ficheros:
- __main.py:__  
Fichero principal. Contiene dos métodos:
  - __getEfectividad()__  
  Obtiene la efectividad de un ataque (Con un tipo de daño concreto) contra un pokemon (Con uno o dos tipos asociados) en base a la tabla de tipos de pokemon proporcionada en el ejercicio.
  - __atacar()__  
  Simula un ataque de un pokemon a otro dados el pokemon atacante, el índice del ataque seleccionado en su lista de ataques, y un pokemon rival
- __pokemon.py__  
Contiene las estructuras de datos necesarias para representar tanto un Pokemon, como un Ataque.
- __TypeChart.json__  
Contiene codificada la tabla de efectividades de los tipos de pokemon, conteniendo para cada tipo de ataque la efectividad (inmune, debil o fuerte)

### Ejecución

Para ejecutar una prueba, habría que posicionarse dentro de la carpeta "parte 1" y escribir por consola el siguiente comando:
- python3 main.py  

Si se quieren probar otras combinaciones, bastaría con modificar las variables bajo el comentario de "Ejemplo de simulación"

## Parte 2

Para el desarrollo de esta parte, al tratarse de una API CRUD, se ha optado por utilizar sistemas más solidos.  
- Por un lado, se ha construido una base de datos mysql. Para configurarla, es necesario seguir los siguientes pasos:
  - Construir la base de datos utilizando el script ***script_bdd.sql***, presente en la carpeta "parte 2".
  - Sustituir las credenciales presentes al inicio del fichero ***app.py*** por las credenciales de acceso a la base de datos mysql construida.
- Para la exposición de los endpoints de la API, se ha optado por utilizar la librería **Flask**. 
  - Para instalarla basta con escribir el siguiente comando por consola:  
    - pip install Flask
  - Una vez instalada, para lanzar la API habría que escribir lo siguiente por consola:
    - flask run
- Para la ejecución de las pruebas, se adjunta una colección de Postman que contiene todos los endpoints disponibles junto a una breve descripción de ellos y un ejemplo funcional. Se encuentra en la carpeta "parte 2/coleccion postman".

## Parte 3

Para el desarrollo de esta parte, se utilizan bases asentadas en la parte 1 y 2 para implementar un simulador de combate pokemon:
- Se utiliza la misma base de datos empleada en la parte 2, más una nueva tabla definida en el script ***script_bdd.sql***, presente en la carpeta "parte 3".
- Se implementan unos nuevos endpoints, utilizando igualmente Flask. Para lanzar la API es necesario ejecutar el mismo comando que en la parte 2, pero esta vez desde dentro de la carpete "parte 3".
- Se incluye una nueva colección de Postman en la carpeta "parte 3/coleccion postman".
