CREATE TABLE partida (
	id INT AUTO_INCREMENT PRIMARY KEY,
	jugador1 VARCHAR(255),
    jugador2 VARCHAR(255),
    pokemon1_jugador1 INT,
    pokemon2_jugador1 INT,
    pokemon1_jugador2 INT,
    pokemon2_jugador2 INT,
    turno VARCHAR(255),
    defensor VARCHAR(255),
    estado VARCHAR(255),
	FOREIGN KEY (pokemon1_jugador1) REFERENCES equipo_pokemon(id),
	FOREIGN KEY (pokemon2_jugador1) REFERENCES equipo_pokemon(id),
	FOREIGN KEY (pokemon1_jugador2) REFERENCES equipo_pokemon(id),
	FOREIGN KEY (pokemon2_jugador2) REFERENCES equipo_pokemon(id)
);