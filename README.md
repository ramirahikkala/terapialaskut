# Terapialaskut

## Mitä se tekee?

Kirjoittaa Kelan ku205.pdf ja ku206.pdf tiedostoihin asiakkaan, käyntien ja terapeutin tiedot. Kaikki nämä tallennetaan paikalliseen tietokantaan mahdollista tulevaa käyttöä varten.

## Miten se toimii?

1. Syötä terapeutin tiedot terapeutti-välilehdellä. Tuplaklikkaus taulukon ylimällä rivillä päästää sinut muokkaamaan tietoja.
2. Lisää asiakkaat asiakkaat-välilehdellä. Lisää asiakas -nappi lisää asiakkaan ja muokkaaminen onnistuu kuten terapeutille.
3. Lisää käynnit käynnit-välilehdellä. Valitse käyntipäivä, asiakas ja muut tiedot ja paina lisää käynti -nappia.
4. Luo laskut -nappi luo laskut. Huom! Laskut tehdään vain niille käynneille, joita ei ole aiemmin laskutettu. Tämä tarkoittaa myös sitä, että käynnit katoaa käyntinäkymästä, kun laskutus on tehty. Ohjelmassa ei ole vielä mahdollisuutta peruuttaa laskutusta, joten ole tarkkana, että kaikki käynnit on lisätty ja oikein ennen laskujen luomista. Laskut ja asiakastiedot löytyy kelalomakkeet-hakemistosta.

## Tietokanta

Käytettävä tietokonta on sqlite. Se täytyy olla asennettuna tietokoneellesi, jotta ohjelma toimii. Voit käyttää tietokantaselainta täydentemään toiminnallisuutta, mm. tekemään laskutuksen uudelleen merkkaamalla käyntejä laskuttamattomaksi.

## Asennus

Lisään tarkemman ohjeen ja Windows-asennuspaketin, kun ehdin. Tällä hetkellä näin:
1. Asenna sqlite
2. Asenna vaaditut pip-modulit requirements-txt -tiedoston mukaan.
3. Käynnistä therapy.py
