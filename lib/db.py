import random
import string


class Data:
    """
    Almacenamiento de valores posibles para la generacion del formulario

    Métodos:
        get_XXX (*parametros): Lee la lista asociada y devuelve el numero de elementos establecidos coo parametros
    """
    nom_masculinos = [
        "Liam", "Noah", "Oliver", "Elijah", "Lucas", "Mason", "Ethan", "Sebastian", "Mateo", "Jack",
        "Alexander", "Jacob", "Michael", "Daniel", "Henry", "Matthew", "Joseph", "Samuel", "David", "John",
        "Wyatt", "Oscar", "Josiah", "Carlos", "Juan", "Diego", "Adam", "Julian", "Max", "Leo",
        "Isaac", "Ian", "Alex", "Anthony", "Victor", "Jesus", "Gabriel", "Benjamin", "Caleb", "Miguel",
        "Ezra", "Andrew", "Aaron", "Evan", "Adrian", "Antonio", "Ayden", "Dominic", "Blake", "Angel",
        "Joel", "Santiago", "Luis", "Chase", "Cole", "Carson", "Jason", "Damian", "Harrison", "Fernando",
        "Zachary", "George", "Kenneth", "Andres", "Brayden", "Jaden", "Jeremiah", "Omar", "Giovanni", "Derek",
        "Cristian", "Collin", "Brady", "Gael", "Ivan", "Martin", "Jared", "Kyle", "Charlie", "Jorge",
        "Jonas", "Landon", "Edwin", "Allen", "Bryce", "Alan", "Timothy", "Peter", "Israel", "Devin",
        "Aiden", "Eduardo", "Tristan", "Felix", "Bryant", "Javier", "Rafael", "Marvin", "Kai", "Brent",
        "Cesar", "Maxwell", "Marco", "Jayce", "Hector", "Riley", "Raymond", "Tony", "Ricardo", "Shane",
        "Pedro", "Axel", "Arthur", "Leonardo", "Edgar", "Elliot", "Sergio", "Armando", "Elias", "Stanley",
        "Brayan", "Randy", "Gerardo", "Enrique", "Malachi", "Nick", "Danny", "Erick", "Mauricio", "Dillon",
        "Griffin", "Emilio", "Finn", "Andy", "Marcus", "Preston", "Marco", "Jesse", "Simon", "Cody",
        "Micah", "Nathaniel", "Diego", "Jaxon", "Ryder", "Yahir", "Caiden", "Zayden", "Jeffrey", "Freddy",
        "Phoenix", "Ronald", "Dante", "Dalton", "Keegan", "Ali", "Jaiden", "Rodrigo", "Zion", "August",
        "Tobias", "Joaquin", "Jamison", "Maximus", "Adan", "Milan", "Phillip", "Alberto", "Gustavo", "Francis"
    ]

    nom_femeninos = [
        "Emma", "Olivia", "Ava", "Sophia", "Isabella", "Mia", "Charlotte", "Amelia", "Harper", "Evelyn",
        "Abigail", "Emily", "Elizabeth", "Sofia", "Avery", "Ella", "Scarlett", "Grace", "Chloe", "Victoria",
        "Madison", "Luna", "Mila", "Lucy", "Zoey", "Stella", "Natalie", "Anna", "Samantha", "Maria",
        "Leah", "Audrey", "Ariana", "Lily", "Aria", "Eva", "Julia", "Savannah", "Gabriella", "Valentina",
        "Nova", "Clara", "Vivian", "Reagan", "Lucia", "Elena", "Alina", "Allison", "Isla", "Sarah",
        "Eden", "Aaliyah", "Adeline", "Ariel", "Alexa", "Kinsley", "Paisley", "Hailey", "Genesis", "Penelope",
        "Naomi", "Alyssa", "Elise", "Serena", "Liliana", "Brielle", "Jade", "Camila", "Delilah", "Catherine",
        "Josephine", "Rose", "Valeria", "Laila", "Nora", "Riley", "Daniela", "Scarlet", "Isabelle", "Annabelle",
        "Molly", "Michelle", "Nicole", "Angela", "Giselle", "Amber", "Christina", "Elisa", "Francesca", "Diana",
        "Claudia", "Alma", "Violeta", "Crystal", "Angie", "Vanessa", "Chelsea", "Daisy", "Eliana", "Mariana",
        "Melissa", "Ashley", "Alondra", "Miranda", "Alejandra", "Sara", "Amy", "Isabel", "Esmeralda", "Paula",
        "Cynthia", "Laura", "Karla", "Sophie", "Linda", "Megan", "Kiara", "Martha", "Andrea", "Teresa",
        "Leticia", "Lizbeth", "Guadalupe", "Jacqueline", "Monica", "Alexandra", "Veronica", "Gabriela", "Yesenia", "Anastasia",
        "Renata", "Brenda", "Fernanda", "Bianca", "Rebecca", "Irene", "Patricia", "Paola", "Daniella", "Juliana",
        "Athena", "Selena", "Regina", "Lena", "Faith", "Ariadna", "Alison", "Esther", "April", "Frances",
        "Helen", "Jamie", "Lyla", "Anahi", "Dulce", "Emilia", "Lorena", "Adriana", "Yaretzi", "Priscilla"
    ]

    apellidos = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris",
        "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright",
        "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall",
        "Rivera", "Campbell", "Mitchell", "Carter", "Roberts",
        "Gomez", "Phillips", "Evans", "Turner", "Diaz",
        "Parker", "Cruz", "Edwards", "Collins", "Reyes",
        "Stewart", "Morris", "Morales", "Murphy", "Cook",
        "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper",
        "Peterson", "Bailey", "Reed", "Kelly", "Howard",
        "Ramos", "Kim", "Cox", "Ward", "Richardson",
        "Watson", "Brooks", "Chavez", "Wood", "James",
        "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes",
        "Price", "Alvarez", "Castillo", "Sanders", "Patel",
        "Myers", "Long", "Ross", "Foster", "Jimenez",
        "Powell", "Jenkins", "Perry", "Russell", "Sullivan",
        "Bell", "Coleman", "Butler", "Henderson", "Barnes",
        "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero",
        "Jordan", "Patterson", "Hughes", "Murray", "Freeman",
        "Wells", "Webb", "Simpson", "Stevens", "Tucker",
        "Porter", "Hunter", "Hicks", "Crawford", "Henry",
        "Boyd", "Mason", "Morales", "Kennedy", "Warren",
        "Dixon", "Ramos", "Reyes", "Burns", "Gordon",
        "Shaw", "Holmes", "Rice", "Robertson", "Hunt",
        "Black", "Daniels", "Palmer", "Mills", "Nichols",
        "Grant", "Knight", "Ferguson", "Rose", "Stone",
        "Hawkins", "Dunn", "Perkins", "Hudson", "Spencer",
        "Gardner", "Stephens", "Payne", "Pierce", "Berry",
        "Matthews", "Arnold", "Wagner", "Willis", "Ray",
        "Watkins", "Olson", "Carroll", "Duncan", "Snyder",
        "Hart", "Cunningham", "Bradley", "Lane", "Andrews",
        "Ruiz", "Harper", "Fox", "Riley", "Armstrong",
        "Carpenter", "Weaver", "Greene", "Lawrence", "Elliott",
        "Chavez", "Sims", "Austin", "Peters", "Kelley",
        "Franklin", "Lawson"
    ]

    paises_ciudades = [
        {"pais": "Ecuador", "ciudad": "Quito"},
        {"pais": "Ecuador", "ciudad": "Guayaquil"},
        {"pais": "Ecuador", "ciudad": "Cuenca"},
        {"pais": "Ecuador", "ciudad": "Loja"},
        {"pais": "Ecuador", "ciudad": "Ambato"},
        {"pais": "Ecuador", "ciudad": "Manta"},
        {"pais": "Ecuador", "ciudad": "Portoviejo"},
        {"pais": "Ecuador", "ciudad": "Machala"},
        {"pais": "Ecuador", "ciudad": "Esmeraldas"},
        {"pais": "Ecuador", "ciudad": "Santo Domingo"},
        {"pais": "Colombia", "ciudad": "Bogota"},
        {"pais": "Colombia", "ciudad": "Medellin"},
        {"pais": "Colombia", "ciudad": "Cali"},
        {"pais": "Colombia", "ciudad": "Barranquilla"},
        {"pais": "Colombia", "ciudad": "Cartagena"},
        {"pais": "Colombia", "ciudad": "Cucuta"},
        {"pais": "Colombia", "ciudad": "Bucaramanga"},
        {"pais": "Colombia", "ciudad": "Ibague"},
        {"pais": "Colombia", "ciudad": "Pereira"},
        {"pais": "Colombia", "ciudad": "Santa Marta"},
        {"pais": "Peru", "ciudad": "Lima"},
        {"pais": "Peru", "ciudad": "Arequipa"},
        {"pais": "Peru", "ciudad": "Trujillo"},
        {"pais": "Peru", "ciudad": "Chiclayo"},
        {"pais": "Peru", "ciudad": "Piura"},
        {"pais": "Peru", "ciudad": "Cusco"},
        {"pais": "Peru", "ciudad": "Huancayo"},
        {"pais": "Peru", "ciudad": "Iquitos"},
        {"pais": "Peru", "ciudad": "Tacna"},
        {"pais": "Peru", "ciudad": "Ica"},
        {"pais": "Argentina", "ciudad": "Buenos Aires"},
        {"pais": "Argentina", "ciudad": "Cordoba"},
        {"pais": "Argentina", "ciudad": "Rosario"},
        {"pais": "Argentina", "ciudad": "Mendoza"},
        {"pais": "Argentina", "ciudad": "Tucuman"},
        {"pais": "Argentina", "ciudad": "La Plata"},
        {"pais": "Argentina", "ciudad": "Mar del Plata"},
        {"pais": "Argentina", "ciudad": "Salta"},
        {"pais": "Argentina", "ciudad": "Santa Fe"},
        {"pais": "Argentina", "ciudad": "San Juan"},
        {"pais": "Brasil", "ciudad": "Sao Paulo"},
        {"pais": "Brasil", "ciudad": "Rio de Janeiro"},
        {"pais": "Brasil", "ciudad": "Salvador"},
        {"pais": "Brasil", "ciudad": "Brasilia"},
        {"pais": "Brasil", "ciudad": "Fortaleza"},
        {"pais": "Brasil", "ciudad": "Belo Horizonte"},
        {"pais": "Brasil", "ciudad": "Manaus"},
        {"pais": "Brasil", "ciudad": "Curitiba"},
        {"pais": "Brasil", "ciudad": "Recife"},
        {"pais": "Brasil", "ciudad": "Porto Alegre"}
    ]

    generos = ["masculino", "femenino"]

    profesiones = [
        "Ingeniero", "Doctor", "Enfermero", "Maestro", "Profesor",
        "Abogado", "Programador", "Cientifico", "Piloto", "Arquitecto",
        "Empresario", "Cocinero", "Musico", "Escritor", "Artista",
        "Actor", "Fotografo", "Periodista", "Psicologo"
    ]

    alergias = [
        "Alergia al polen", "Alergia al polvo", "Alergia a los acaros",
        "Alergia a las picaduras de insectos", "Alergia al moho",
        "Alergia a los alimentos", "Alergia a la leche", "Alergia al gluten",
        "Alergia a los frutos secos", "Alergia a los mariscos",
        "Alergia al latex", "Alergia a los medicamentos", "Alergia a la penicilina",
        "Alergia a los sulfamidas", "Alergia al niquel",
        "Alergia al perfume", "Alergia al jabon", "Alergia al sol",
        "Alergia al frio", "Alergia al calor"
    ]

    deportes = [
        "Futbol", "Baloncesto", "Beisbol", "Voley", "Tenis",
        "Rugby", "Criquet", "Golf", "Hockey", "Natacion",
        "Atletismo", "Gimnasia", "Boxeo", "Ciclismo", "Esqui",
        "Snowboard", "Skateboarding", "Surf", "Escalada", "Equitacion"
    ]

    hobbies = [
        "Jardineria", "Caminar", "Leer", "Escribir", "Pintar",
        "Tocar un instrumento musical", "Viajar", "Fotografia", "Escalada", "Ciclismo",
        "Cocinar", "Nadar", "Acampar", "Dibujar", "Buceo",
        "Bailar", "Tejer", "Juegos de mesa", "Pasear a mascotas", "Pesca",
        "Yoga", "Correr", "Escuchar musica", "Surf", "Futbol",
        "Baloncesto", "Cazar", "Catas de vino", "Senderismo", "Jugar videojuegos",
        "Patinaje", "Artesania", "Ceramica", "Bricolaje", "Coleccionismo",
        "Observacion de aves", "Puzzles", "Meditar", "Equitacion", "Boxeo",
        "Ajedrez", "Juegos de rol", "Parkour", "Vela", "Crossfit",
        "Gimnasia", "Golf", "Magia", "Malabares", "Origami",
        "Canto", "Teatro", "Voley", "Pilates", "Beisbol",
        "Zumba", "Escalada en roca", "Karate", "Ballet", "Astronomia",
        "Aerobic", "Fencing", "Arco y flecha", "Polo", "Rugby",
        "Kung Fu", "Kickboxing", "Pilota", "Rafting", "Esqui acuatico",
        "Paracaidismo", "Judo", "Billar", "Ping-pong",
        "Esgrima", "Inmersiones", "Lanzamiento de disco", "Voleibol de playa", "Triatlon",
        "Maraton", "MMA", "Motocross", "BMX", "Snowboarding",
        "Skateboarding", "Drone racing", "Squash", "Lacrosse", "Criquet",
        "Bowling", "Badminton", "Polo acuatico", "Escalada en hielo", "Skydiving",
        "Bungee jumping", "Parapente", "Windsurfing", "Kitesurfing", "Bodybuilding",
        "Capoeira", "Muay Thai", "Taekwondo", "Wrestling", "Sumo",
        "Bobsleigh", "Skeleton", "Curling", "Biathlon", "Futbol Australiano",
        "Real Tennis", "Sepak Takraw", "Kabaddi", "Netball", "Hockey sobre hielo",
        "Hockey sobre hierba", "Hockey subacuatico", "Rugby subacuatico", "Jai alai", "Pelota vasca",
        "Kickball", "Kin-ball", "Korfball", "Pickleball", "Rounders",
        "Softball", "Stickball", "Stoolball", "Tee-ball", "Tetherball",
        "Three sided football", "Underwater football", "Unicycle hockey", "Unicycle football", "Vigoro",
        "Volata", "Water polo", "Wiffleball", "Xare", "Yukigassen",
        "Padel tennis", "Petanque", "Platform tennis", "Qianball", "Racketlon",
        "Racquets", "Real tennis", "Soft tennis", "Speed-ball", "Squash tennis",
        "Table tennis", "Tennis polo", "Wireball", "Yak polo", "Gateball",
        "Ground billiards", "Croquet", "Roque", "Cycle polo", "Elephant polo",
        "Horseball", "Segway polo", "Yak polo", "Canoe polo", "Kayak polo",
        "Fistball", "Footvolley", "Sepak takraw", "Throwball", "Volleyball",
        "Beach volleyball", "Paralympic volleyball", "Sitting volleyball", "Skater hockey", "Unicycle hockey",
        "Ringette", "Rinkball", "Rossall hockey", "Spongee", "Underwater hockey",
        "Unicycle basketball", "Wheelchair basketball", "Beach handball", "Czech handball", "Field handball",
        "Torball", "Tchoukball", "Beach rugby", "Snow rugby", "Tag rugby",
        "Touch rugby", "Wheelchair rugby", "Arm wrestling", "Basque pelota", "Jai alai",
        "Box lacrosse", "Field lacrosse", "Women's lacrosse", "Inter crosse", "Softcrosse"
    ]

    colores = [
        "Rojo", "Azul", "Verde", "Amarillo", "Morado",
        "Naranja", "Rosa", "Negro", "Blanco", "Gris",
        "Marron", "Beige", "Turquesa", "Dorado", "Plateado",
        "Celeste", "Coral", "Lavanda", "Oliva", "Fucsia"
    ]

    estados_civiles = [
        "Soltero", "Casado", "Divorciado", "Viudo", "Separado",
        "Union libre", "Comprometido"
    ]

    modelos_autos = [
        "Chevrolet Onix", "Hyundai Accent", "Volkswagen Gol", "Toyota Hilux", "Ford F-150",
        "Nissan Versa", "Honda Civic", "Renault Kwid", "Kia Rio", "Mazda 3",
        "Fiat Palio", "Peugeot 208", "Suzuki Swift", "Mercedes-Benz Clase A", "BMW Serie 3",
        "Audi A3", "Citroën C3", "Dacia Sandero", "Opel Corsa", "Seat Ibiza"
    ]

    profesiones = [
        "Ingeniero", "Medico", "Enfermero", "Abogado", "Arquitecto",
        "Profesor", "Policia", "Bombero", "Carpintero", 
        "Pintor", "Electricista", "Mecanico", "Dentista", "Veterinario",
        "Peluquero", "Periodista", "Fotografo", "Cocinero", "Panadero",
        "Psicologo", "Contador", "Programador", "Agricultor", "Pescador",
        "Ninguno"
    ]

    enfermedades_raras = [
        "Sindrome de Patau", "Sindrome de Edwards", "Fibrosis quistica",
        "Enfermedad de Huntington", "Distrofia muscular de Duchenne",
        "Sindrome de Prader-Willi", "Sindrome de Marfan", "Enfermedad de Gaucher",
        "Sindrome de Rett", "Progeria",
        "Sindrome de Sturge-Weber", "Sindrome de Guillain-Barre",
        "Enfermedad de Wilson", "Hipertension pulmonar primaria",
        "Esclerosis lateral amiotrofica (ELA)", "Enfermedad de Tay-Sachs",
        "Enfermedad de Niemann-Pick", "Sindrome de Angelman",
        "Sindrome de Tourette", "Histiocitosis de celulas de Langerhans",
        "Ninguna"
    ]

    mascotas = [
        "Perro", "Gato", "Pajaro", "Pez", "Conejo",
        "Hamster", "Tortuga", "Iguana", "Serpiente", "Rata",
        "Chinchilla", "Tarantula", "Huron", "Cuy", "Erizo",
        "Cerdito miniatura", "Rana", "Geco", "Axolote", "Ninguno"
    ]

    equipos_futbol = [
        "Boca Juniors (Argentina)", "River Plate (Argentina)", "Independiente (Argentina)",
        "Flamengo (Brasil)", "Palmeiras (Brasil)", "Sao Paulo FC (Brasil)",
        "Atletico Nacional (Colombia)", "Independiente Santa Fe (Colombia)", "Millonarios FC (Colombia)",
        "Universitario (Peru)", "Alianza Lima (Peru)", "Sporting Cristal (Peru)",
        "Liga de Quito (Ecuador)", "Barcelona SC (Ecuador)", "Emelec (Ecuador)",
        "America (Mexico)", "Chivas Guadalajara (Mexico)", "Cruz Azul (Mexico)", "Ninguno"
    ]

    lenguajes_programacion = [
        "Python", "Java", "C#", "JavaScript", "TypeScript",
        "Kotlin", "Go", "Rust", "Ruby", "PHP",
        "Swift", "Dart", "Scala", "Perl", "Haskell",
        "MATLAB", "R", "Julia", "Lua", "Shell",
        "C++", "C", "Objective-C", "Groovy", "SQL",
        "Ninguno"
    ]

    idiomas = [
        "Ingles", "Portugues", "Frances", "Aleman",
        "Italiano", "Holandes", "Ruso", "Mandarin", "Japones",
        "Coreano", "arabe", "Turco", "Griego", "Hebreo",
        "Sueco", "Noruego", "Danes", "Finnes", "Polaco",
        "Hungaro", "Checo", "Hindi", "Bengali", "Tamil",
        "Ninguno"
    ]

    bases_datos = [
        "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQLite",
        "MariaDB", "Microsoft SQL Server", "Redis", "Cassandra", "Couchbase",
        "Elasticsearch", "Firebase", "InfluxDB", "Neo4j", "DynamoDB",
        "CouchDB", "HBase", "Riak", "Memcached", "DB2",
        "Ninguno"
    ]

    paises = [
        "Afganistan", "Albania", "Alemania", "Andorra", "Angola",
        "Antigua y Barbuda", "Arabia Saudita", "Argelia", "Argentina", "Armenia",
        "Australia", "Austria", "Azerbaiyan", "Bahamas", "Banglades",
        "Barbados", "Barein", "Belgica", "Belice", "Benin",
        "Bielorrusia", "Birmania", "Bolivia", "Bosnia y Herzegovina", "Botsuana",
        "Brasil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
        "Butan", "Cabo Verde", "Camboya", "Camerun", "Canada",
        "Catar", "Chad", "Chile", "China", "Chipre",
        "Ciudad del Vaticano", "Colombia", "Comoras", "Corea del Norte", "Corea del Sur",
        "Costa de Marfil", "Costa Rica", "Croacia", "Cuba", "Dinamarca",
        "Dominica", "Ecuador", "Egipto", "El Salvador", "Emiratos arabes Unidos",
        "Eritrea", "Eslovaquia", "Eslovenia", "Estados Unidos",
        "Estonia", "Etiopia", "Filipinas", "Finlandia", "Fiyi",
        "Francia", "Gabon", "Gambia", "Georgia", "Ghana",
        "Granada", "Grecia", "Guatemala", "Guyana", "Guinea",
        "Guinea ecuatorial", "Guinea-Bisau", "Haiti", "Honduras", "Hungria",
        "India", "Indonesia", "Irak", "Iran", "Irlanda",
        "Islandia", "Islas Marshall", "Islas Salomon", "Israel", "Italia",
        "Jamaica", "Japon", "Jordania", "Kazajistan", "Kenia",
        "Kirguistan", "Kiribati", "Kuwait", "Laos", "Lesoto",
        "Letonia", "Libano", "Liberia", "Libia", "Liechtenstein",
        "Lituania", "Luxemburgo", "Madagascar", "Malasia", "Malaui",
        "Maldivas", "Mali", "Malta", "Marruecos", "Mauricio",
        "Mauritania", "Mexico", "Micronesia", "Moldavia", "Monaco",
        "Mongolia", "Montenegro", "Mozambique", "Namibia", "Nauru",
        "Nepal", "Nicaragua", "Niger", "Nigeria", "Noruega",
        "Nueva Zelanda", "Oman", "Paises Bajos", "Pakistan", "Palaos",
        "Panama", "Papua Nueva Guinea", "Paraguay", "Peru", "Polonia",
        "Portugal", "Reino Unido", "Republica Centroafricana", "Republica Checa", "Republica de Macedonia",
        "Republica del Congo", "Republica Democratica del Congo", "Republica Dominicana", "Republica Sudafricana", "Ruanda",
        "Rumania", "Rusia", "Samoa", "San Cristobal y Nieves", "San Marino",
        "San Vicente y las Granadinas", "Santa Lucia", "Santo Tome y Principe", "Senegal", "Serbia",
        "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia",
        "Sri Lanka", "Suazilandia", "Sudan", "Sudan del Sur", "Suecia",
        "Suiza", "Surinam", "Tailandia", "Tanzania", "Tayikistan",
        "Timor Oriental", "Togo", "Tonga", "Trinidad y Tobago", "Tunez",
        "Turkmenistan", "Turquia", "Tuvalu", "Ucrania", "Uganda",
        "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam",
        "Yemen", "Yibuti", "Zambia", "Zimbabue", "Ninguno"
    ]

    habilidades_tecnicas = [
        "Programacion",  "Analitica web", "Marketing digital", "SEO/SEM",
        "Redes y seguridad informatica", "Manejo de bases de datos", "Desarrollo web", "Desarrollo movil", "Edicion de video",
        "Administracion de sistemas", "Inteligencia artificial", "Machine learning", "Blockchain",
        "Arquitectura de software", "Testing de software", "Analisis de datos", "Ingenieria de hardware", "Ciberseguridad",
        "Cloud computing (AWS, Google Cloud, etc.)", "Desarrollo de videojuegos", "Manejo de CRM", "Desarrollo de realidad virtual y aumentada", "Ninguno"
    ]

    habilidades_personales = [
        "Comunicacion efectiva", "Resolucion de problemas", "Trabajo en equipo", "Creatividad", "Proactividad",
        "Empatia", "Organizacion", "Adaptabilidad", "Liderazgo", "Capacidad de aprendizaje",
        "Gestion del tiempo", "Toma de decisiones", "Auto motivacion", "Responsabilidad", "Pensamiento critico",
        "Flexibilidad", "Habilidad de negociacion", "Manejo de conflictos", "Iniciativa", "Optimismo",
        "Perseverancia", "Honestidad", "Gestion del estres", "Habilidades interpersonales", "Ninguno"
    ]

    habilidades_varias = [
        "Idiomas", "Cocina", "Deportes", "Artes marciales", "Primeros auxilios",
        "Conocimientos de vino", "Jardineria", "Carpinteria", "Mecanica basica", "Fotografia",
        "Escritura creativa", "Tocar un instrumento musical", "Dibujo y pintura", "Ceramica", "Costura",
        "Meditacion", "Yoga", "Escalada", "Buceo", "Ninguno"
    ]

    religiones = ["Cristianismo", "Islam", "Hinduismo", "Budismo", "Sijismo",
                  "Judaismo", "Taoismo", "Confucianismo", "Jainismo", "Espiritismo", "Ninguna"]

    posturas_politicas = ["Izquierda", "Derecha", "Centro", "Anarquismo", "Comunismo",
                          "Socialismo", "Liberalismo", "Conservadurismo", "Fascismo", "Populismo", "Ninguna"]

    def get_genero(self):
        generos = ["Masculino", "Femenino"]
        return random.choice(generos)

    def get_nombres(self, genero):
        if genero == "Masculino":
            return f"{random.choice(self.nom_masculinos)} {random.choice(self.nom_masculinos)}"
        elif genero == "Femenino":
            return f"{random.choice(self.nom_femeninos)} {random.choice(self.nom_femeninos)}"
        else:
            return None

    def get_apellidos(self):
        return f"{random.choice(self.apellidos)} {random.choice(self.apellidos)}"

    def get_lugarnacimiento(self):
        elemento = random.choice(self.paises_ciudades)
        return f"{elemento['pais']}, {elemento['ciudad']}"

    def get_profesiones(self):
        num_profesiones = random.randint(0, 3)
        return random.sample(self.profesiones, num_profesiones)

    def get_hobbies(self):
        num_hobbies = random.randint(1, 5)
        return random.sample(self.hobbies, num_hobbies)

    def get_colores(self):
        num_colores = random.randint(1, 3)
        return random.sample(self.colores, num_colores)

    def get_estado_civil(self):
        return random.choice(self.estados_civiles)

    def get_modelos_autos(self):
        num_modelos = random.randint(0, 4)
        return random.sample(self.modelos_autos, num_modelos)

    def get_enfermedades_raras(self):
        num_enfermedades = random.randint(0, 3)
        return random.sample(self.enfermedades_raras, num_enfermedades)

    def get_mascotas(self):
        num_mascotas = random.randint(0, 5)
        return random.sample(self.mascotas, num_mascotas)

    def get_lenguajes_programacion(self):
        num_lenguajes = random.randint(0, 10)
        return random.sample(self.lenguajes_programacion, num_lenguajes)

    def get_idiomas(self):
        num_idiomas = random.randint(0, 5)
        return random.sample(self.idiomas, num_idiomas)

    def get_bases_de_datos(self):
        num_bases_datos = random.randint(0, 10)
        return random.sample(self.bases_datos, num_bases_datos)

    def get_paises(self):
        num_paises = random.randint(0, 20)
        return random.sample(self.paises, num_paises)

    def get_habilidades_tecnicas(self):
        num_habilidades = random.randint(0, 5)
        return random.sample(self.habilidades_tecnicas, num_habilidades)

    def get_habilidades_personales(self):
        num_habilidades = random.randint(0, 5)
        return random.sample(self.habilidades_personales, num_habilidades)

    def get_habilidades_varias(self):
        num_habilidades = random.randint(0, 5)
        return random.sample(self.habilidades_varias, num_habilidades)

    def get_equipo_futbol(self):
        return random.sample(self.equipos_futbol, 1)

    def get_religion(self):
        return random.choice(self.religiones)

    def get_postura_politica(self):
        return random.choice(self.posturas_politicas)

    def get_identificador_pasaporte(self):
        codigos_paises = ['ECU', 'USA', 'MEX', 'PER', 'COL']
        codigo_pais = random.choice(codigos_paises)
        numeros = random.choices(string.digits, k=7)
        return ''.join([codigo_pais] + numeros)

    def get_edad(self):
        return random.randint(18, 105)

    def get_alergias(self):
        return random.sample(self.alergias, k=random.randint(0, 4))

    def get_deportes(self):
        return random.sample(self.deportes, k=random.randint(0, 3))
