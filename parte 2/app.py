from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

PASS_DB = "mysqlpass"
HOST = "127.0.0.1"
USER = "root"
DB_NAME = "pokemonVisiotech"

# Configuración de la conexión a la base de datos
config = {
    'host': HOST,
    'user': USER,
    'password': PASS_DB,
    'database': DB_NAME
}
conn = mysql.connector.connect(**config)

cursor = conn.cursor(dictionary=True)


# Utilidades
def obtener_ataques_por_id_pokemon(pokemon_id):
    query = 'SELECT a.nombre AS nombre_ataque, a.tipo AS tipo_ataque, a.poder AS poder_ataque ' \
            'FROM ataque a JOIN ataque_pokemon ap ON a.nombre = ap.ataque_nombre WHERE ap.pokemon_id = %s;'
    cursor.execute(query, (pokemon_id,))
    ataques = cursor.fetchall()
    return ataques


# Rutas para pokemons base
# Ruta para obtener todos los pokemons base
@app.route('/pokemons', methods=['GET'])
def obtener_pokemons():
    cursor.execute('SELECT * FROM pokemon')
    pokemones = cursor.fetchall()
    if pokemones:
        return jsonify({'pokemons': pokemones})
    else:
        return jsonify({'mensaje': 'No se encontraron pokemons'}), 404


# Ruta para obtener un pokemon base por su Nombre
@app.route('/pokemon/<string:pokemon_nombre>', methods=['GET'])
def obtener_pokemon_por_nombre(pokemon_nombre):
    cursor.execute('SELECT * FROM pokemon WHERE nombre = %s', (pokemon_nombre,))
    pokemon = cursor.fetchone()
    if pokemon:
        return jsonify(pokemon)
    else:
        return jsonify({'mensaje': 'Pokemon no encontrado'}), 404


# Ruta para crear un nuevo pokemon base
@app.route('/pokemon', methods=['POST'])
def crear_pokemon():
    nuevo_pokemon = request.json
    query = 'INSERT INTO pokemon ' \
            '(nombre, tipo, salud_total, ataque_base, defensa_base, ataque_especial_base, defensa_especial_base, velocidad_base) ' \
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    values = (nuevo_pokemon['nombre'], nuevo_pokemon['tipo'], nuevo_pokemon['salud_total'],
              nuevo_pokemon['ataque_base'], nuevo_pokemon['defensa_base'], nuevo_pokemon['ataque_especial_base'],
              nuevo_pokemon['defensa_especial_base'], nuevo_pokemon['velocidad_base'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Pokemon creado exitosamente'}), 201


# Ruta para actualizar un pokemon base por su ID
@app.route('/pokemon/<string:pokemon_nombre>', methods=['PUT'])
def actualizar_pokemon(pokemon_nombre):
    datos_actualizados = request.json
    query = 'UPDATE pokemon ' \
            'SET nombre=%s, tipo=%s, salud_total=%s, ataque_base=%s, defensa_base=%s, ataque_especial_base=%s, defensa_especial_base=%s, velocidad_base=%s ' \
            'WHERE nombre=%s'
    values = (datos_actualizados['nombre'], datos_actualizados['tipo'], datos_actualizados['salud_total'],
              datos_actualizados['ataque_base'], datos_actualizados['defensa_base'],
              datos_actualizados['ataque_especial_base'], datos_actualizados['defensa_especial_base'],
              datos_actualizados['velocidad_base'], pokemon_nombre)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Pokemon actualizado exitosamente'})


# Ruta para eliminar un pokemon por su nombre
@app.route('/pokemon/<string:pokemon_nombre>', methods=['DELETE'])
def eliminar_pokemon(pokemon_nombre):
    cursor.execute('DELETE FROM pokemon WHERE nombre = %s', (pokemon_nombre,))
    conn.commit()
    return jsonify({'mensaje': 'Pokemon eliminado exitosamente'})


# Rutas para ataques
# Ruta para obtener todos los ataques
@app.route('/ataques', methods=['GET'])
def obtener_ataques():
    cursor.execute('SELECT * FROM ataque')
    ataques = cursor.fetchall()
    if ataques:
        return jsonify({'ataques': ataques})
    else:
        return jsonify({'mensaje': 'No se encontraron ataques'}), 404


# Ruta para obtener un ataque por su Nombre
@app.route('/ataque/<string:ataque_nombre>', methods=['GET'])
def obtener_ataque_por_nombre(ataque_nombre):
    cursor.execute('SELECT * FROM ataque WHERE nombre = %s', (ataque_nombre,))
    ataque = cursor.fetchone()
    if ataque:
        return jsonify(ataque)
    else:
        return jsonify({'mensaje': 'Ataque no encontrado'}), 404


# Ruta para crear un nuevo ataque
@app.route('/ataque', methods=['POST'])
def crear_ataque():
    nuevo_ataque = request.json
    query = 'INSERT INTO ataque (nombre, tipo, poder) VALUES (%s, %s, %s)'
    values = (nuevo_ataque['nombre'], nuevo_ataque['tipo'], nuevo_ataque['poder'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Ataque creado exitosamente'}), 201


# Ruta para actualizar un ataque por su Nombre
@app.route('/ataque/<string:ataque_nombre>', methods=['PUT'])
def actualizar_ataque(ataque_nombre):
    datos_actualizados = request.json
    query = 'UPDATE ataque SET nombre=%s, tipo=%s, poder=%s WHERE nombre=%s'
    values = (datos_actualizados['nombre'], datos_actualizados['tipo'], datos_actualizados['poder'], ataque_nombre)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Ataque actualizado exitosamente'})


# Ruta para eliminar un ataque por su Nombre
@app.route('/ataque/<string:ataque_nombre>', methods=['DELETE'])
def eliminar_ataque(ataque_nombre):
    cursor.execute('DELETE FROM ataque WHERE nombre = %s', (ataque_nombre,))
    conn.commit()
    return jsonify({'mensaje': 'Ataque eliminado exitosamente'})


# Rutas para el equipo de un entrenador
# Ver el equipo de un entrenador
@app.route('/equipo/<string:nombre_entrenador>', methods=['GET'])
def obtener_equipo(nombre_entrenador):
    query = 'SELECT * FROM equipo_pokemon WHERE entrenador = %s'
    cursor.execute(query, (nombre_entrenador,))
    equipo = cursor.fetchall()

    if equipo:
        for pokemon in equipo:
            ataques = obtener_ataques_por_id_pokemon(pokemon['id'])
            pokemon['ataques'] = ataques
        json = jsonify({'equipo': equipo})
        return json
    else:
        return jsonify({'mensaje': 'No se ha encontrado un equipo'}), 404


# Incluir pokemon en el equipo de un entrenador
@app.route('/equipo/capturar', methods=['POST'])
def capturar_pokemon():
    captura = request.json
    query = 'INSERT INTO equipo_pokemon (nombre_pokemon, entrenador, nombre_propio, nivel, salud_actual) ' \
            'VALUES (%s, %s, %s, %s, %s)'
    values = (captura['nombre_pokemon'], captura['nombre_entrenador'], captura['nombre_propio'],
              captura['nivel'], captura['salud_actual'])
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Pokemon capturado exitosamente'}), 201


# Eliminar pokemon del equipo de un entrenador
@app.route('/equipo/liberar/<string:nombre_entrenador>/<string:nombre_propio_pokemon>', methods=['DELETE'])
def liberar_pokemon(nombre_entrenador, nombre_propio_pokemon):
    query = 'DELETE FROM equipo_pokemon WHERE entrenador=%s AND nombre_propio=%s'
    values = (nombre_entrenador, nombre_propio_pokemon)
    cursor.execute(query, values)
    conn.commit
    return jsonify({'mensaje': 'Pokemon liberado exitosamente'}), 201


# Actualizar pokemon en el equipo de un entrenador
@app.route('/equipo/<string:nombre_entrenador>/<string:nombre_propio_pokemon>', methods=['PUT'])
def actualizar_equipo(nombre_entrenador, nombre_propio_pokemon):
    datos_actualizados = request.json
    query = 'UPDATE equipo_pokemon ' \
            'SET nombre_pokemon=%s, entrenador=%s, nombre_propio=%s, nivel=%s, salud_actual=%s ' \
            'WHERE entrenador=%s AND nombre_propio=%s'
    values = (datos_actualizados['nombre_pokemon'], datos_actualizados['nombre_entrenador'],
              datos_actualizados['nombre_propio'], datos_actualizados['nivel'], datos_actualizados['salud_actual'],
              nombre_entrenador, nombre_propio_pokemon)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Equipo actualizado exitosamente'})


# Ver ataques de un pokemon
@app.route('/entrenamiento/<int:pokemon_id>', methods=['GET'])
def obtener_ataques_de_pokemon(pokemon_id):
    ataques = obtener_ataques_por_id_pokemon(pokemon_id)

    if ataques:
        return jsonify({'ataques': ataques})
    else:
        return jsonify({'mensaje': 'No se han encontrado ataques aprendidos'}), 404


# Incluir ataque en un pokemon
@app.route('/entrenamiento/aprender', methods=['POST'])
def aprender_ataque():
    entrenamiento = request.json
    query = 'INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre) ' \
            'VALUES (%s, %s)'
    values = (entrenamiento['pokemon_id'], entrenamiento['ataque_nombre'])

    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Pokemon entrenado exitosamente'}), 201


# Eliminar ataque de un pokemon
@app.route('/entrenamiento/olvidar/<int:pokemon_id>/<string:ataque_nombre>', methods=['DELETE'])
def olvidar_ataque(pokemon_id, ataque_nombre):
    query = 'DELETE FROM ataque_pokemon WHERE pokemon_id=%s AND ataque_nombre=%s'
    values = (pokemon_id, ataque_nombre)
    cursor.execute(query, values)
    conn.commit
    return jsonify({'mensaje': 'Movimiento olvidado exitosamente'}), 201


# Actualizar ataque de un pokemon
@app.route('/entrenamiento/<int:pokemon_id>/<string:ataque_nombre>', methods=['PUT'])
def actualizar_ataque_aprendido(pokemon_id, ataque_nombre):
    datos_actualizados = request.json
    query = 'UPDATE ataque_pokemon ' \
            'SET pokemon_id=%s, ataque_nombre=%s ' \
            'WHERE pokemon_id=%s AND ataque_nombre=%s'
    values = (datos_actualizados['pokemon_id'], datos_actualizados['ataque_nombre'], pokemon_id, ataque_nombre)
    cursor.execute(query, values)
    conn.commit()
    return jsonify({'mensaje': 'Ataque actualizado exitosamente'})


# Otras rutas utiles
# Obtener ataques con tipo compatible con el pokemon
@app.route('/ataques_compatibles/<string:nombre_pokemon>', methods=['GET'])
def obtener_ataques_compatibles(nombre_pokemon):
    query = 'SELECT a.nombre AS nombre_ataque, a.tipo AS tipo_ataque, a.poder AS poder_ataque ' \
            'FROM ataque a JOIN pokemon p ON a.tipo = p.tipo WHERE p.nombre = %s'
    cursor.execute(query, (nombre_pokemon,))
    ataques = cursor.fetchall()

    if ataques:
        return jsonify({'ataques': ataques})
    else:
        return jsonify({'mensaje': 'No se han encontrado ataques compatibles con ese pokemon'}), 404


# Obtener pokemons que comparten un ataque concreto
@app.route('/ataque_compartido/<string:ataque_nombre>', methods=['GET'])
def obtener_pokemon_con_mismo_ataque(ataque_nombre):
    query = 'SELECT ep.nombre_pokemon, ep.entrenador, ep.nombre_propio ' \
            'FROM ataque_pokemon ap ' \
            'JOIN equipo_pokemon ep ON ap.pokemon_id = ep.id ' \
            'WHERE ap.ataque_nombre = %s'
    cursor.execute(query, (ataque_nombre,))
    pokemons = cursor.fetchall()

    if pokemons:
        return jsonify({'ataques': pokemons})
    else:
        return jsonify({'mensaje': 'No se han encontrado pokemons con ese ataque'}), 404


if __name__ == '__main__':
    app.run(debug=True)
