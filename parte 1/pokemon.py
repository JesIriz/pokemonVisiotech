class Pokemon:
    def __init__(self, nivel, nombre, tipo1, tipo2, salud_actual, salud_total,
                 ataque_base, defensa_base, ataque_especial_base,
                 defensa_especial_base, velocidad_base):
        self.nivel = nivel
        self.nombre = nombre
        self.tipo1 = tipo1
        self.tipo2 = tipo2
        self.salud_actual = salud_actual
        self.salud_total = salud_total
        self.ataque_base = ataque_base
        self.defensa_base = defensa_base
        self.ataque_especial_base = ataque_especial_base
        self.defensa_especial_base = defensa_especial_base
        self.velocidad_base = velocidad_base
        self.ataques = []

    def addAtaque(self, ataque):
        if len(self.ataques) >= 4:
            print(f"El pokemon {self.nombre} ya tiene 4 ataques")
        else:
            self.ataques.append(ataque)

    def getAtaque(self, indice):
        if len(self.ataques) > 0:
            return self.ataques[indice]

class Ataque:
    def __init__(self, nombre, tipo, poder):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder