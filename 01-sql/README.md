# Oefeningen SQL

## Setup

1. Download en installeer Beekeeper Studio Community Edition: [https://www.beekeeperstudio.io/get-community](https://www.beekeeperstudio.io/get-community). *Je hoeft geen mail-adres in te geven; klik op 'Skip to the download'.*
Beekeeper is een eenvoudige GUI om SQL uit te voeren op een database (maar dat kan bv. evengoed via een Python-programma).

2. Open een commandoprompt in de folder waarin dit README.md bestand staat (01-sql), en start de database met het commando
`docker compose up`.

3. Open Beekeeper en maak een nieuwe verbinding
- type: Postgres
- host: localhost
- port: 5432
- username: postgres
- wachtwoord: postgres

De database gaat over films; je ziet links in Beekeeper een lijst met de tabellen in de database.

4. Verken eerst de database manueel door op de verschillende tabelnamen te (dubbel)klikken.

5. Maak op papier een grafisch overzicht van de verschillende tabellen en hoe ze relateren (onderlinge verwijzingen).
   Vind je ergens one-to-many, many-to-one, many-to-many relaties terug?
   Welke tabellen zijn 'junction tables'?

> **Oplossing**
>
> One-to-many/many-to-one:
> - `movies` (many) - (one) `directors`
> - `movies` (many) - (one) `studio`
> - `movies` (many) - (one) `rating`
>
> Many-to-many:
> - `movies` (many) - (many) `actors`, met als junction table `movie_actor`

6. Zie je ergens een mogelijkheid om de database verder te normaliseren?

> **Oplossing**
>
> Het genre in de `movies`-tabel zou verder genormaliseerd kunnen worden.

> Als je later opnieuw wil beginnen met de originele database,
> - stop je de database (Ctrl-C)
> - verwijder je de folder `postgres_data` die aangemaakt wordt
> - start je de database opnieuw (`docker compose up`)
> De originele database wordt dan opnieuw aangemaakt.

## Oefeningen deel 1: SELECT

### Oefening 1
Selecteer alle films.

> **Oplossing**
>
> ```sql
> SELECT * FROM movies;
>```


### Oefening 2
Selecteer de titel en jaar van alle films die **na** het jaar 2000 uitgebracht zijn.

> **Oplossing**
>
> ```sql
> SELECT * FROM movies WHERE release_year > 2000;
>```

| title           | release_year |
| --------------- | ------------ |
| Avatar          | 2009         |
| Inception       | 2010         |
| The Dark Knight | 2008         |

### Oefening 3
Selecteer de titel en het jaar alle films die **voor** het jaar 2000 uitgebracht zijn, **en** die het genre 'Sci-Fi' hebben, gesorteerd op titel.

> **Oplossing**
>
> ```sql
> SELECT * FROM movies WHERE release_year < 2000 AND genre = 'Sci-Fi';
>```

| title      | release_year |
| ---------- | ------------ |
| The Matrix | 1999         |


## Oefeningen deel 2: JOIN

### Oefening 4
Selecteer van alle films de titel, de naam van hun regisseur, en hun jaartal, gesorteerd op naam van de regisseur en vervolgens op jaartal.

> **Oplossing**
>
> ```sql
> SELECT title, name, release_year FROM movies LEFT JOIN directors ON movies.director_id = directors.director_id ORDER BY name, release_year;
>```


| name                 | release_year | title                    |
| -------------------- | ------------ | ------------------------ |
| Christopher Nolan    | 2008         | The Dark Knight          |
| Christopher Nolan    | 2010         | Inception                |
| David Fincher        | 1999         | Fight Club               |
| Francis Ford Coppola | 1972         | The Godfather            |
| Frank Darabont       | 1994         | The Shawshank Redemption |
| James Cameron        | 1997         | Titanic                  |
| James Cameron        | 2009         | Avatar                   |
| Quentin Tarantino    | 1994         | Pulp Fiction             |
| Steven Spielberg     | 1993         | Jurassic Park            |
| The Wachowskis       | 1999         | The Matrix               |


### Oefening 5
Selecteer van alle films en alle ratings (dus ook de ratings zonder film in de database) de titel van de film en de rating.

> **Oplossing**
>
> ```sql
> SELECT title, rating FROM movies FULL OUTER JOIN ratings ON movies.rating_id = ratings.rating_id;
>```
> Aangezien er geen films zonder rating zijn, zou een `RIGHT JOIN` hetzelfde resultaat geven.


| title                    | rating |
| ------------------------ | ------ |
| null                     | G      |
| null                     | NC-17  |
| null                     | PG     |
| Avatar                   | PG-13  |
| Inception                | PG-13  |
| Jurassic Park            | PG-13  |
| The Dark Knight          | PG-13  |
| Titanic                  | PG-13  |
| Fight Club               | R      |
| Pulp Fiction             | R      |
| The Godfather            | R      |
| The Matrix               | R      |
| The Shawshank Redemption | R      |

### Oefening 6
Selecteer alle films de titel en de actor_id van de acteurs die erin meespelen.

> **Oplossing**
>
> ```sql
> SELECT title, actor_id FROM movies LEFT JOIN movie_actor ON movies.movie_id = movie_actor.movie_id;
>```


| title                    | actor_id |
| ------------------------ | -------- |
| Avatar                   | 22       |
| Avatar                   | 24       |
| Avatar                   | 23       |
| Fight Club               | 19       |
| Fight Club               | 20       |
| Fight Club               | 21       |
| Inception                | 3        |
| Inception                | 2        |
| Inception                | 1        |
| Inception                | 4        |
| Jurassic Park            | 7        |
| Jurassic Park            | 6        |
| Jurassic Park            | 5        |
| Pulp Fiction             | 11       |
| Pulp Fiction             | 12       |
| Pulp Fiction             | 13       |
| The Dark Knight          | 10       |
| The Dark Knight          | 8        |
| The Dark Knight          | 9        |
| The Godfather            | 17       |
| The Godfather            | 18       |
| The Godfather            | 16       |
| The Matrix               | 28       |
| The Matrix               | 26       |
| The Matrix               | 27       |
| The Shawshank Redemption | 15       |
| The Shawshank Redemption | 14       |
| Titanic                  | 25       |
| Titanic                  | 1        |

### Oefening 7
Selecteer alle films de titel en naam van de acteurs die erin meespelen.
Bijvoorbeeld:

> **Oplossing**
>
> ```sql
> SELECT title, name FROM movies LEFT JOIN movie_actor ON movies.movie_id = movie_actor.movie_id LEFT JOIN actors on movie_actor.actor_id = actors.actor_id;
>```

| title                    | name                 |
| ------------------------ | -------------------- |
| Avatar                   | Sam Worthington      |
| Avatar                   | Sigourney Weaver     |
| Avatar                   | Zoe Saldana          |
| Fight Club               | Brad Pitt            |
| Fight Club               | Edward Norton        |
| Fight Club               | Helena Bonham Carter |
| Inception                | Elliot Page          |
| Inception                | Joseph Gordon-Levitt |
| Inception                | Leonardo DiCaprio    |
| Inception                | Tom Hardy            |
| Jurassic Park            | Jeff Goldblum        |
| Jurassic Park            | Laura Dern           |
| Jurassic Park            | Sam Neill            |
| Pulp Fiction             | John Travolta        |
| Pulp Fiction             | Samuel L. Jackson    |
| Pulp Fiction             | Uma Thurman          |
| The Dark Knight          | Aaron Eckhart        |
| The Dark Knight          | Christian Bale       |
| The Dark Knight          | Heath Ledger         |
| The Godfather            | Al Pacino            |
| The Godfather            | James Caan           |
| The Godfather            | Marlon Brando        |
| The Matrix               | Carrie-Anne Moss     |
| The Matrix               | Keanu Reeves         |
| The Matrix               | Laurence Fishburne   |
| The Shawshank Redemption | Morgan Freeman       |
| The Shawshank Redemption | Tim Robbins          |
| Titanic                  | Kate Winslet         |
| Titanic                  | Leonardo DiCaprio    |

### Oefening 8
Selecteer alle films met een 'PG-13' of 'R'-rating. Geef van elke film de titel, naam van de regisseur, en de rating terug.

> **Oplossing**
>
> ```sql
> SELECT title, name, rating FROM movies LEFT JOIN directors ON movies.director_id = directors.director_id LEFT JOIN ratings ON movies.rating_id = ratings.rating_id;
>```


## Oefeningen deel 3: INSERT, UPDATE, DELETE

### Oefening 9
Voeg je favoriete film en acteurs toe aan de database.

> *Opgelet: je moet de gegevens invoeren in de juiste volgorde, zodat je geen verwijzingen creëert naar niet-bestaande rijen.
Dus eerst acteurs en regisseurs, dan de film zelf, en helemaal op het einde de rijen in de junction tables.*

> **Oplossing**
>
> ```sql
> INSERT INTO directors(name, birth_year) VALUES ('Favorite Director', 1970); -- ID 9
> INSERT INTO actors(name) VALUES ('Favorite Actor'); -- ID 29
> INSERT INTO movies(title, release_year, genre, studio_id, director_id, rating_id) VALUES ('Favorite Movie', 2010, 'Tech', 1, 9, 1); -- ID 11
> INSERT INTO movie_actor(movie_id, actor_id) VALUES (11, 29)
>```


### Oefening 10
Pas de beschrijving van de rating 'G' aan naar 'Everyone'.

> **Oplossing**
>
> ```sql
> UPDATE ratings SET description='Everyone' WHERE rating = 'G';
>```


### Oefening 11
Verwijder alle films van voor 1995 uit de tabel.

> **Oplossing**
>
> ```sql
> DELETE FROM movies WHERE release_year < 1995;
>```
> Merk op dat de database zo geconfigureerd is dat deze films ook automatisch uit de `movie_actor` tabel verwijderd werden, om geen verwijzingen te hebben naar niet-bestaande films.
