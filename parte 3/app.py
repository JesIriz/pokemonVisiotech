import decimal
import json
import random

from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Credenciales de la base de datos
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
def obtener_pokemon_por_nombre_y_entrenador(nombre_propio_pokemon, entrenador):
    query = 'SELECT ep.id, ep.nivel, p.ataque_base, p.tipo, p.defensa_base, ep.salud_actual ' \
            'FROM equipo_pokemon ep JOIN pokemon p ON ep.nombre_pokemon = p.nombre ' \
            'WHERE ep.nombre_propio = %s AND ep.entrenador = %s'
    cursor.execute(query, (nombre_propio_pokemon, entrenador,))
    return cursor.fetchone()


def obtener_pokemon_por_id(pokemon_id):
    query = 'SELECT ep.id, ep.nivel, p.ataque_base, p.tipo, p.defensa_base, ep.salud_actual ' \
            'FROM equipo_pokemon ep JOIN pokemon p ON ep.nombre_pokemon = p.nombre ' \
            'WHERE ep.id = %s'
    cursor.execute(query, (pokemon_id,))
    return cursor.fetchone()


def obtener_id_pokemon_por_nombre_y_entrenador(nombre_propio_pokemon, entrenador):
    return obtener_pokemon_por_nombre_y_entrenador(nombre_propio_pokemon, entrenador)['id']


def obtener_ataque_por_nombre(nombre_ataque):
    query = 'SELECT poder, tipo FROM ataque WHERE nombre = %s'
    cursor.execute(query, (nombre_ataque,))
    return cursor.fetchone()


def obtener_dano(ataque, pokemon_atacante, pokemon_rival):
    nivel_atacante = pokemon_atacante['nivel']
    ataque_base = pokemon_atacante['ataque_base']

    efectividad = getEfectividad(ataque['tipo'], pokemon_rival['tipo'])
    random_attack_power = random.randint(85, 100)

    return (((2 * nivel_atacante / 5 + 2) * ataque_base * ataque['poder'] / pokemon_rival['defensa_base']) / 50) * efectividad * random_attack_power / 100


def getEfectividad(tipo_atacante, tipo_rival):
    f = open('TypeChart.json')
    type_chart = json.load(f)

    for tipo in type_chart:
        if tipo["name"] == tipo_atacante:
            if tipo_rival in tipo["inmune"]:
                return 0
            elif tipo_rival in tipo["debil"]:
                return 0.5
            elif tipo_rival in tipo["fuerte"]:
                return 2
            else:
                return 1

    print(f"No se ha encontrado una relación entre {tipo_atacante} y {tipo_rival} en la tabla de tipos")
    return 1


def obtener_partida_por_id(id_partida):
    query = 'SELECT * FROM partida WHERE id = %s'
    cursor.execute(query, (id_partida,))
    return cursor.fetchone()


# Ruta para obtener el estado de una partida
@app.route('/partida/estado/<int:id_partida>', methods=['GET'])
def obtener_partida(id_partida):
    partida = obtener_partida_por_id(id_partida)

    if partida:
        return jsonify({'partida': partida})
    else:
        return jsonify({'mensaje': 'No se ha encontrado la partida'}), 404


# Ruta para iniciar una nueva partida
@app.route('/partida/iniciar', methods=['POST'])
def iniciar_partida():
    datos_partida = request.json
    query = 'INSERT INTO partida (jugador1, jugador2, pokemon1_jugador1, pokemon2_jugador1, ' \
            'pokemon1_jugador2, pokemon2_jugador2, turno, defensor, estado) ' \
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    values = (
        datos_partida['jugador1'],
        datos_partida['jugador2'],
        obtener_id_pokemon_por_nombre_y_entrenador(datos_partida['pokemon1_jugador1'], datos_partida['jugador1']),
        obtener_id_pokemon_por_nombre_y_entrenador(datos_partida['pokemon2_jugador1'], datos_partida['jugador1']),
        obtener_id_pokemon_por_nombre_y_entrenador(datos_partida['pokemon1_jugador2'], datos_partida['jugador2']),
        obtener_id_pokemon_por_nombre_y_entrenador(datos_partida['pokemon2_jugador2'], datos_partida['jugador2']),
        datos_partida['jugador1'],
        datos_partida['jugador2'],
        'Iniciada'
    )

    cursor.execute(query, values)
    conn.commit()

    partida_id = cursor.lastrowid

    return jsonify({'mensaje': f'Partida iniciada con id: {partida_id}'}), 201


# Ruta para jugar una ronda
@app.route('/partida/jugar', methods=['PUT'])
def jugar_ronda():
    # Obtener datos iniciales
    datos_jugada = request.json
    id_partida = datos_jugada['id_partida']
    partida = obtener_partida_por_id(id_partida)

    if not partida:
        return jsonify({'mensaje': 'No se ha encontrado la partida'}), 404

    jugador_atacante = partida['turno']
    jugador_rival = partida['defensor']

    # Obtener datos del enfrentamiento de esta ronda
    ataque = obtener_ataque_por_nombre(datos_jugada['ataque_seleccionado'])
    pokemon_atacante = obtener_pokemon_por_nombre_y_entrenador(datos_jugada['pokemon_atacante'], jugador_atacante)
    pokemon_rival = obtener_pokemon_por_nombre_y_entrenador(datos_jugada['pokemon_objetivo'], jugador_rival)

    # Comprobar que ninguno de los dos pokemon este muerto
    if pokemon_atacante['salud_actual'] <= 0:
        return jsonify({'mensaje': 'El pokemon no puede atacar porque está debilitado'}), 201
    elif pokemon_rival['salud_actual'] <= 0:
        return jsonify({'mensaje': 'El pokemon al que intentas atacar ya está debilitado'}), 201

    # Calcular dano infligido
    dano = obtener_dano(ataque, pokemon_atacante, pokemon_rival)
    dano_decimal = decimal.Decimal(str(dano))
    salud_rival_decimal = decimal.Decimal(str(pokemon_rival['salud_actual']))
    nueva_salud_rival = salud_rival_decimal - dano_decimal

    # Actualizar vida rival
    query_actualizar_vida = 'UPDATE equipo_pokemon SET salud_actual = %s ' \
                            'WHERE entrenador = %s AND nombre_propio = %s'
    values_actualizar_vida = (nueva_salud_rival, jugador_rival, datos_jugada['pokemon_objetivo'])
    print(query_actualizar_vida)
    print(values_actualizar_vida)
    cursor.execute(query_actualizar_vida, values_actualizar_vida)
    conn.commit()

    # Comprobar si el jugador ya ha ganado
    # Obtener la salud del otro pokemon rival
    if partida['jugador1'] == jugador_rival:
        if pokemon_rival['id'] == partida['pokemon1_jugador1']:
            otro_pokemon_rival = obtener_pokemon_por_id(partida['pokemon1_jugador1'])
        else:
            otro_pokemon_rival = obtener_pokemon_por_id(partida['pokemon2_jugador1'])
    elif partida['jugador2'] == jugador_rival:
        if pokemon_rival['id'] == partida['pokemon1_jugador2']:
            otro_pokemon_rival = obtener_pokemon_por_id(partida['pokemon1_jugador2'])
        else:
            otro_pokemon_rival = obtener_pokemon_por_id(partida['pokemon2_jugador2'])
    salud_otro_rival = otro_pokemon_rival['salud_actual']

    print(salud_otro_rival)
    print(nueva_salud_rival)

    # Si los dos pokemon rivales estan muertos, acaba la partida
    if nueva_salud_rival <= 0 and salud_otro_rival <= 0:
        # Actualizar el estado de la partida
        query_actualizar_partida = 'UPDATE partida SET estado = %s ' \
                                   'WHERE id = %s'
        values_actualizar_partida = ('Finalizada', id_partida)
        cursor.execute(query_actualizar_partida, values_actualizar_partida)
        conn.commit()

        return jsonify({'mensaje': f'{datos_jugada["pokemon_atacante"]} hace {dano} de daño a '
                                   f'{datos_jugada["pokemon_objetivo"]} con {datos_jugada["ataque_seleccionado"]}. '
                                   f'Los dos pokemon de {jugador_rival} están muy debilitados. {jugador_atacante} '
                                   f'ha ganado la partida!'}), 201

    # Cambiar rival y jugador en la partida
    query_actualizar_partida = 'UPDATE partida SET turno = %s, defensor = %s ' \
                               'WHERE id = %s'
    values_actualizar_partida = (jugador_rival, jugador_atacante, id_partida)
    cursor.execute(query_actualizar_partida, values_actualizar_partida)
    conn.commit()

    return jsonify({'mensaje': f'{datos_jugada["pokemon_atacante"]} hace {dano} de daño a '
                               f'{datos_jugada["pokemon_objetivo"]} con {datos_jugada["ataque_seleccionado"]}'}), 201


@app.route('/partida/eliminar/<int:id_partida>', methods=['DELETE'])
def eliminar_partida(id_partida):
    query = 'DELETE FROM partida WHERE id = %s'
    cursor.execute(query, (id_partida,))
    conn.commit
    return jsonify({'mensaje': 'Partida eliminada exitosamente'}), 201


if __name__ == '__main__':
    app.run(debug=True)
