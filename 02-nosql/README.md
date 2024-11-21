# NoSQL experiment

## Setup

1. Start MongoDB en MongoExpress via
`docker compose up` in de folder van deze README.

> Navigeren naar een folder kan je doen met het commando `cd`.
> Tip: gebruik de Tab-toets om het pad aan te vullen.
> 
> Bijvoorbeeld, als je naar de folder `C:\Users\me\Downloads\02-nosql` wil gaan, 
> en je staat al in `C:\Users\me`, dan typ je `cd Downloads\02-nosql`.
> Het volstaat waarschijnlijk om `cd Dow<tab>\02<tab>` te typen.

2. Surf naar [http://localhost:8081](http://localhost:8081) en login als `admin` met wachtwoord `pass`

3. Open de database `movie_db` en vervolgens de collectie `movies`.

> Als je later opnieuw wil beginnen met de originele database,
> - stop je de database (Ctrl-C)
> - verwijder je de folder `mongo_data` die aangemaakt wordt
> - start je de database opnieuw (`docker compose up`)
> De originele database wordt dan opnieuw aangemaakt.

## Oefeningen

### Oefening 1

Bekijk de gegevens in de movies-collectie. Wat valt op vergeleken met de SQL tabellen (in het bijzonder qua normalisatie)?

> **Oplossing**
>
> De gegevens zijn niet genormaliseerd. Bijvoorbeeld, de naam van de regisseurs en acteurs staan in het JSON-document van een film.

### Oefening 2
Zoek alle films met als genre (key) de waarde Sci-Fi. Kijk goed naar het resultaat; hebben deze films ook nog een ander genre? Hoe zou je dit in een SQL database moeten doen?

> **Oplossing**
>
> Zoekopdracht met
> - key: genre
> - value: Sci-Fi
> 
> Deze films hebben ook andere genres.
> In een SQL database zou dit een many-to-many relatie zijn, en zou er dus een junction tabel gebruikt moeten worden.


### Oefening 3

Zoek alle films waarin `Leonardo DiCaprio` een rol speelde.

> *Hint: als key gebruik je `cast.actor.name`, als value de naam van de acteur. Dit geeft aan dat je wil zoeken op de naam van de acteur van de cast van de film.*

> **Oplossing**
>
> Zoekopdracht met
> - key: cast.actor.name
> - value: Leonardo DiCaprio


### Oefening 4

In MongoDB kan je een query beschrijven als een JSON-object.
Bekijk onderstaande query; wat denk je dat die doet?

```
{
    genre: "Sci-Fi",
    release_year: { $gt: 1995 },
    $or: [
        { "cast.actor.name": "Leonardo DiCaprio" },
        { "cast.actor.name": "Keanu Reeves" }
    ]
}
```

Een query kan ook een `projection`-deel hebben. Dat geeft aan welke delen van het document je wil terugkrijgen. Bijvoorbeeld:
```
{
    title: 1, 
    release_year: 1,
    "director.name": 1,
    "cast.actor.name": 1
}
```

Ga naar de tab `Advanced` en voer bovenstaande query en projection in. Bekijk het antwoord, en ga na of dat aan de query voldoet.

> **Oplossing**
>
> De query zoekt films die voldoen aan al onderstaande voorwaarden:
> - het genre is Sci-Fi
> - de films zijn uitgekomen na 1995
> - Leonardo DiCaprio of Keanu Reeves spelen erin mee
> 
> Van de twee films die hieraan voldoen krijgen we (via de projection) de titel, jaar, regisseur, en alle acteurs (dus niet enkel de acteurs die voldoen aan de query).
