import random
import json
from pokemon import Pokemon, Ataque


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


def atacar(pokemon_atacante, indice_ataque, pokemon_rival):
    ataque_seleccionado = pokemon_atacante.getAtaque(indice_ataque)
    efectividad_tipo_1 = getEfectividad(ataque_seleccionado.tipo, pokemon_rival.tipo1)
    efectividad_tipo_2 = getEfectividad(ataque_seleccionado.tipo, pokemon_rival.tipo2)
    efectividad_total = efectividad_tipo_1 * efectividad_tipo_2
    random_attack_power = random.randint(85, 100)

    return (((2 * pokemon_atacante.nivel / 5 + 2) * pokemon_atacante.ataque_base * ataque_seleccionado.poder / pokemon_rival.defensa_base) / 50) * efectividad_total * random_attack_power / 100


pikachu = Pokemon(50, "Pikachu", "Electrico", "", 100, 100, 50, 10, 50, 10, 2)
ataque1 = Ataque("Atizar", "Normal", 80)
ataque2 = Ataque("Impactrueno", "Electrico", 60)
pikachu.addAtaque(ataque1)
pikachu.addAtaque(ataque2)

squirtle = Pokemon(5, "Squirtle", "Agua", "", 100, 100, 50, 10, 50, 10, 2)

resultado_ataque = atacar(pikachu, 1, squirtle)

print(f'El daño realizado es: {resultado_ataque}')
