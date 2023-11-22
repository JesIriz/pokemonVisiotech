-- CREATE SCHEMA `pokemonVisiotech`;

-- Creacion de las tablas necesarias
CREATE TABLE pokemon (
	nombre VARCHAR(255) PRIMARY KEY,
	tipo VARCHAR(255),
	salud_total INT,
	ataque_base INT,
	defensa_base INT,
	ataque_especial_base INT,
	defensa_especial_base INT,
	velocidad_base INT
);

CREATE TABLE equipo_pokemon (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nombre_pokemon VARCHAR(255),
    entrenador VARCHAR(255),
    nombre_propio VARCHAR(255),
    nivel INT,
    salud_actual FLOAT,
	FOREIGN KEY (nombre_pokemon) REFERENCES pokemon(nombre)
);

CREATE TABLE ataque (
	nombre VARCHAR(255) PRIMARY KEY,
    tipo VARCHAR(255),
    poder INT
);

CREATE TABLE ataque_pokemon (
    pokemon_id INT,
    ataque_nombre VARCHAR(255),
    PRIMARY KEY (pokemon_id, ataque_nombre),
	FOREIGN KEY (pokemon_id) REFERENCES equipo_pokemon(id),
    FOREIGN KEY (ataque_nombre) REFERENCES ataque(nombre)
);

-- Insercion de datos de ejemplo
-- Crear pokemon de ejemplo
INSERT INTO pokemon (nombre, tipo, salud_total, ataque_base, defensa_base, ataque_especial_base, defensa_especial_base, velocidad_base)
VALUES ("Pikachu", "Electrico", 35, 55, 40, 50, 50, 90);
INSERT INTO pokemon (nombre, tipo, salud_total, ataque_base, defensa_base, ataque_especial_base, defensa_especial_base, velocidad_base)
VALUES ("Squirtle", "Agua", 44, 48, 65, 50, 64, 43);
INSERT INTO pokemon (nombre, tipo, salud_total, ataque_base, defensa_base, ataque_especial_base, defensa_especial_base, velocidad_base)
VALUES ("Arcanine", "Fuego", 90, 110, 80, 100, 80, 95);
INSERT INTO pokemon (nombre, tipo, salud_total, ataque_base, defensa_base, ataque_especial_base, defensa_especial_base, velocidad_base)
VALUES ("Grookey", "Planta", 50, 65, 60, 40, 40, 65);

-- Crear ataques disponibles
INSERT INTO ataque (nombre, tipo, poder)
VALUES ("Placaje", "Normal", 40);
INSERT INTO ataque (nombre, tipo, poder)
VALUES ("Impactrueno", "Electrico", 65);
INSERT INTO ataque (nombre, tipo, poder)
VALUES ("Hidrobomba", "Agua", 110);
INSERT INTO ataque (nombre, tipo, poder)
VALUES ("Nitrocarga", "Fuego", 50);
INSERT INTO ataque (nombre, tipo, poder)
VALUES ("Pirotecnia", "Fuego", 70);
INSERT INTO ataque (nombre, tipo, poder)
VALUES ("Latigo cepa", "Planta", 45);

-- Crear equipo de Jesus
INSERT INTO equipo_pokemon (nombre_pokemon, entrenador, nombre_propio, nivel, salud_actual)
VALUES ("Pikachu", "Jesus", "Pepe", 50, 100);
INSERT INTO equipo_pokemon (nombre_pokemon, entrenador, nombre_propio, nivel, salud_actual)
VALUES ("Squirtle", "Jesus", "Pepito", 50, 100);

-- Crear equipo de Gustavo
INSERT INTO equipo_pokemon (nombre_pokemon, entrenador, nombre_propio, nivel, salud_actual)
VALUES ("Arcanine", "Gustavo", "Gustavin", 50, 100);
INSERT INTO equipo_pokemon (nombre_pokemon, entrenador, nombre_propio, nivel, salud_actual)
VALUES ("Grookey", "Gustavo", "Gustavito", 50, 100);

-- Asignar ataques a los pokemon de Jesus
INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre)
VALUES (
    (SELECT id FROM equipo_pokemon op WHERE op.nombre_pokemon = "Pikachu" AND op.entrenador = "Jesus"),
    "Placaje"
);
INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre)
VALUES (
    (SELECT id FROM equipo_pokemon op WHERE op.nombre_pokemon = "Pikachu" AND op.entrenador = "Jesus"),
    'Impactrueno'
);
INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre)
VALUES (
    (SELECT id FROM equipo_pokemon op WHERE op.nombre_pokemon = "Squirtle" AND op.entrenador = "Jesus"),
    'Placaje'
);
INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre)
VALUES (
    (SELECT id FROM equipo_pokemon op WHERE op.nombre_pokemon = "Squirtle" AND op.entrenador = "Jesus"),
    'Hidrobomba'
);

-- Asignar ataques a los pokemon de Gustavo
INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre)
VALUES (
    (SELECT id FROM equipo_pokemon op WHERE op.nombre_pokemon = "Arcanine" AND op.entrenador = "Gustavo"),
    'Nitrocarga'
);
INSERT INTO ataque_pokemon (pokemon_id, ataque_nombre)
VALUES (
    (SELECT id FROM equipo_pokemon op WHERE op.nombre_pokemon = "Grookey" AND op.entrenador = "Gustavo"),
    'Latigo cepa'
);
