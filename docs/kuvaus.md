
# modstash

Pekka Väänänen
14.3.2013

## Ongelmakuvaus

Sivusto, jonne käyttäjät voivat ladata tekemiään musiikkikappaleita. Kappaleet ladataan palveluun kahtena versiona, sekä alkuperäistiedostona että MP3-pakattuna audiona. Tämä mahdollistaa eri kappaleiden rakenteiden tarkastelun, jolloin järjestelmä voi löytää kappaleiden väliltä automaattisesti yhteyksiä.

Lisäksi käyttäjät voivat merkitä biiseihinsä myös inspiraationlähteet (jokin muu kappale palvelussa, tai esim. YouTube-linkki) ja myös suoran “isäntäteoksen” jos biisi on selkeästi vain uusi tulkinta aikaisemmasta työstä.

### Tavoitteet
Käyttäjät voivat ladata kappaleita palveluun, ja muokata tietojaan. Kappaleisiin pystyy merkitsemään viitteet muihin kappaleisiin. Vierailijat pystyvät tarkastelemaan kappaleiden ja käyttäjien tietoja, sekä lataamaan teoksia koneelleen.

## Tekninen kuvaus

Alkuperäistiedostolla tarkoitetaan tässä tapauksessa tracker-ohjelmilla tehtyä moduulimusiikkia, jossa nuottidata on eritelty instrumenttien äänistä. Tämä on erityisen kätevää, koska tällöin järjestelmä voi tunnistaa kappaleet joissa on käytetty samoja instrumentteja.

Käyttäjät voivat ladata kappaleita palveluun kirjautumalla käyttäjätunnuksella ja salasanalla. Yksi kirjautumisvaihtoehto on myös OAuth, jolloin palvelussa voitaisiin käyttää Twitter- tai SoundCloud-tunnistautumista.

Vierailijat pystyvät kuuntelemaan palveluun ladattuja kappaleita (eli kaikki on julkista), ja myös lataamaan ne omalle koneellensa.

### Automaattinen instrumenttitunnistus 
Mahdollisena lisäominaisuutena järjestelmä voisi eritellä musiikkitiedostosta ns. “samplet”, eli yksittäiset instrumenttiäänet, ja laskee jokaiselle niistä MD5-tiivisteen, ja sen jälkeen vertaa niitä jo tietokannasta löytyviin sampleihin. Samplet voivat olla toistensa duplikaatteja vaikka tiivisteet eivät täsmäisi (esimerkiksi jos toinen on vain hieman hiljaisempi), ja tällaisia tilanteita varten järjestelmässä pitäisi olla ominaisuus merkitä nämä tiivisteet toistensa duplikaateiksi käsin.

Tietokantatasolla yksittäinen sample voisi siis olla vain kokoelma MD5-tiivisteitä. (Jokainen tiiviste liittyy yhteen sampleen).

## Toteutus

Sovellus toteutetaan Python 3:lla käyttäen apuna CherryPy- sekä psycopg-kirjastoja.Tietokanta on PostgreSQL, ja toteutus ei tule toimimaan muilla tietokannanhallintajärjestelmillä ilman koodimuutoksia.

### Asiakasohjelman vaatimukset
Sivuston peruskäyttö ei vaadi JavaScript-tukea käyttäjän selaimelta, mutta edistyneemmät toiminnot (esim. kappaleen suoratoisto verkkosivulta) saattaa vaatia Flash-selainlisäosan.
