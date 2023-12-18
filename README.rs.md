# Chatbot za predlaganje pametnih telefona

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)

## Uvod

Popularnost pametnih telefona je u konstantnom rastu, a broj dostupnih modela pametnih telefona svakog dana je veći i veći. Na neki način, ovo je dobro, jer omogućava kupcima da imaju više opcija prilikom izbora pametnog telefona za sebe. Postoje mnogi različiti veb sajtovi koji korisnicima omogućavaju pretragu pametnih telefona, i korisnici uglavnom mogu da nadju pametni telefon koji odgovara njihovim potrebama. Međutim, veći broj opcija može zbuniti korisnike koji ne znaju tačno šta traže. Obično, takvi korisnici kupe telefon koji im ne odgovara u potpunosti i relativno brzo ga zamene. Kako bi se to izbeglo, korisnici mogu da se više informišu o pametnim telefonima, kako bi znali šta je tačno važno za njih, ili bi mogao postojati nekakav pomoćnik koji bi korisnicima pomogao da donesu pravu odluku prilikom kupovine pametnog telefona.

<br />

Cilj ove aplikacije je da kroz chatbot omogući korisnicima da lako pronađu pametni telefon za sebe. Ovo će biti postignuto kreiranjem ontologije za pametne telefone. Nakon toga, ontologija će biti populisana najnovijim pametnim telefonima, kako bi korisnici mogli da nadju one pametne telefone koji odgovaraju njihovim potrebama, postavljanjem pitanja chatbotu.

## Ontologija

Kako bi se ovaj chatbot asistent realizovao, prvi korak je kreiranje ontologije za pametne telefone. Ovo se postiže korišćenjem [GoodRelations](http://purl.org/goodrelations/) kao osnovne ontologije i proširivanjem nje informacijama o pametnim telefonima. GoodRelations je lagana ontologija za razmenu informacija o elektronskoj trgovini, i može se koristiti u svim RDF sintaksama. Kako bi se dodale informacije o pametnim telefonima, kreira se klasa SmartPhone kao podklasa klase [Individual](http://purl.org/goodrelations/v1#Individual), i svi modeli pametnih telefona su podklase klase SmartPhone. Na primer, model pametnog telefona može biti Samsung Galaxy S23, a individuali ovog tipa bili bi Samsung Galaxy S23+, Samsung Galaxy S23 Ultra itd. Svaki pametni telefon ima proizvodjača, koji se modeluje korišćenjem klase [Brand](http://purl.org/goodrelations/v1#Brand) i dodavanjem objektnog svojstva hasBrand. Informacije o RAM-u, memoriji, kameri, vrsti ekrana, čipsetu i operativnom sistemu modeluju se na isti način, osim što se za svaki od ovih atributa pametnog telefona kreira nova klasa. Kreiranje klasa za ove atribute omogućava postavljanje ograničenja za modele pametnih telefona. Ako koristimo isti model Samsung Galaxy S23 kao primer, pametni telefoni ovog modela mogu imati samo kameru sa 200 ili 50 Mpx. Konačno, za modelovanje informacija o ceni pametnog telefona, datumu prodaje, veličini ekrana, rezoluciji ekrana i boji, koriste se svojstva podataka. Ova ontologija se čuva u fajlu [GoodRelations.owl](./ontology/GoodRelations.owl), unutar "ontology" foldera.

<br />

Kada je ontologija kreirana, sledeći korak je njeno populisanje pametnim telefonima. Korišćenjem programskog jezika Python, sajtu [Mobilni Svet](https://mobilnisvet.com/) se pristupa kako bi se dobile informacije u tu svrhu. Razmatrani su pametni telefoni sledećih proizvodjača:
* [Apple](https://mobilnisvet.com/mobilni-proizvodjac/Apple/22/2)
* [Google](https://mobilnisvet.com/mobilni-proizvodjac/Google/71/2)
* [Huawei](https://mobilnisvet.com/mobilni-proizvodjac/Huawei/35/2)
* [OnePlus](https://mobilnisvet.com/mobilni-proizvodjac/OnePlus/55/2)
* [Poco](https://mobilnisvet.com/mobilni-proizvodjac/Poco/84/2)
* [Samsung](https://mobilnisvet.com/mobilni-proizvodjac/Samsung/6/2)
* [Xiaomi](https://mobilnisvet.com/mobilni-proizvodjac/Xiaomi/52/2)

Za svaki proizvodjač, prikupljaju se linkovi ka detaljnim stranicama za svaki pametni telefon koji je pušten u prodaju 2020. godine ili kasnije. Nakon toga, svaki prikupljeni link se obrađuje kako bi se dobile relevantne informacije o odgovarajućem pametnom telefonu. Python biblioteka [Selenium](https://selenium-python.readthedocs.io/) koristi se za dobijanje HTML izvora za svaku stranicu proizvodjača i za svaku detaljnu stranicu pametnog telefona. Zatim se biblioteka [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) koristi za navigaciju kroz HTML i dobijanje svih relevantnih informacija. Informacije o pametnim telefonima čuvaju se u memoriji, i kada su svi linkovi obrađeni, ontologija se popunjava na osnovu sačuvanih podataka. U tu svrhu koristi se biblioteka [rdflib](https://rdflib.readthedocs.io/en/stable/), koja je Python biblioteka za rad s RDF-om i sadrži parser/serializer za gotovo sve poznate RDF serializacije. Biblioteka sadrži klasu Graph, koja predstavlja RDF graf. Metoda parse() se koristi za parsiranje RDF izvora, dodajući rezultirajuće trojke u graf. Graf se može izmeniti pomoću metode add(), koja prihvata trojke koje predstavljaju subjekt, predikat i objekt. Konačno, metoda serialize() se koristi za serijalizaciju grafa u OWL fajl.

<br />

Opisana funkcionalnost nalazi se unutar fajla [scrape.py](./scrape.py). Populisana ontologija se čuva u fajlu [GoodRelationsPopulated.owl](./ontology/GoodRelationsPopulated.owl). Klasa [OWLManager](./ontology_helpers/OWLManager.py) enkapsulira funkcionalnosti koje pruža biblioteka rdflib.

## Chatbot

Chatbot je implementiran kao konzolna aplikacija koja korisnicima pruža opcije za pretragu pametnih telefona na osnovu njihovih karakteristika. Slika ispod predstavlja dijagram klasa ove aplikacije.

![Chatbot class diagram](/images/class_diagram.png "Chatbot class diagram")

Klasa [Menu](./UI/Menu.py) je odgovorna za:
* korisnički prikaz dostupnih opcija
* dobijanje korisničkog unosa korišćenjem klase [ConsoleUserInterface](./UI/ConsoleUserInteraction.py)
* u zavisnosti od korisničkog unosa, izvršavanje adekvatne komande ([Command](./command_pattern/PhonesCommands.py)) ili prikazivanje poruke o grešci

Postoji 11 predefinisanih opcija, pri čemu svaka pretražuje pametne telefone na osnovu različitih karakteristika. Korisnici mogu da:
* Pretražuju telefone po proizvodjaču, datumu i ceni
* Pretražuju telefone po proizvodjaču i operativnom sistemu
* Pretražuju telefone sa željenom kamerom
* Pretražuju telefone po chipsetu, RAM-u i memoriji
* Pretražuju telefone po veličini ekrana i rezoluciji
* Pretražuju telefone sa željenom bojom
* Pronađu najjeftiniji telefon za proizvođača
* Pronađu najjeftiniji telefon sa najboljom kamerom po proizvodjaču, datumu i maksimalnoj ceni
* Pretražuju telefone sa željenom kamerom mlađe od zadatog datuma
* Pretražuju boje za model telefona
* Pišu upite prirodnim jezikom (eksperimentalno)

Svaka opcija ima odgovarajuću komandu koja koristi ConsoleUserInterface za dobijanje dodatnog korisničkog unosa i [SPARQLManager](./ontology_helpers/SPARQLManager.py) za dobijanje pametnih telefona iz populisane ontologije. Svaka komanda ima 2 metode: description() i execute(). Prva metoda se koristi da opiše šta komanda radi. Ovo se koristi kako bi se korisnicima komande prikazale kao opcije. Druga metoda se koristi za izvršavanje odgovarajuće komande na osnovu korisničkog unosa. Unutar ove metode, dobija se dodatni korisnički unos, koji se koristi kao argument za odgovarajuću metodu iz SPARQLManager klase. Klasa SPARQLManager ima ukupno 10 metoda, koje odgovaraju prvim 10 komandama, i ne koristi se samo prilikom pisanja upita na prirodnom jeziku. Koristi OWLManager za dobijanje individuala i imena klasa iz ontologije, koji se koriste za kreiranje SPARQL upita.

<br />

SPARQL je RDF upitni jezik koji se koristi za dohvat i manipulaciju podacima smeštenim u RDF formatu. SPARQL omogućava da upit sadrži trostruke obrasce, konjunkcije, disjunkcije i opcione obrasce. Najčešće korišćeni SPARQL upit je SELECT upit, koji se koristi za izvlačenje sirovih vrednosti sa SPARQL endpoint-a. SELECT upit se sastoji od nekoliko delova. Počinje sa SELECT klauzulom, koja je praćena imenima promenljivih koje će biti prikazane kada se upit izvrši. Zatim sledi WHERE klauzula koja definiše uslov za selekciju podataka i generiše promenljive. FILTER klauzula ograničava generisanje promenljivih tako da se one generišu samo ako FILTER klauzula vrati TRUE. OPTIONAL je binarni operator koji se koristi za generisanje promenljivih ako imaju vrednost, a ako nemaju, promenljive će biti bez vrednosti. Ovaj operator ne ograničava upit na bilo koji način, već samo dohvata podatke ako postoje.

<br />

U ovoj aplikaciji, svaka metoda u klasi SPARQLManager kreira SPARQL upit u zavisnosti od svojih parametara. Kod ispod prikazuje SPARQL upit za pretraživanje telefona po proizvođaču i operativnom sistemu.

```
SELECT ?name ?brand ?camera ?ram ?chipset ?os ?screen ?storage ?price ?date ?colors ?width ?height ?screen_dimension
WHERE {
    ?name ?hasBrand ?brand .
    ?name ?hasOs ?os .
    OPTIONAL {
        ?name ?hasRam ?ram .
        ?name ?hasChipset  ?chipset .
        ?name ?hasBrand ?brand .
        ?name ?hasOs ?os .
        ?name ?hasScreen ?screen .
        ?name ?hasStorage ?storage .
        ?name ?hasPrice ?price .
        ?name ?hasDate ?date .
        ?name ?hasColors ?colors .
        ?name ?hasWidth ?width .
        ?name ?hasHeight ?height .
        ?name ?hasScreenSize ?screen_dimension .
        ?name ?hasCamera ?camera
    }
}
```

U ovoj aplikaciji, svi SPARQL upiti imaju iste promenljive navedene u SELECT klauzuli. Ove promenljive predstavljaju relevantne informacije o pametnim telefonima koje su smeštene unutar ontologije koja je prethodno opisana. WHERE klauzula se koristi za definisanje uslova, i svaki SPARQL upit ima različitu WHERE klauzulu. U prethodnom kodu, WHERE klauzula definiše uslov koji se koristi za pretragu pametnih telefona određenog proizvođača i operativnog sistema. OPTIONAL operator se koristi za dobavljanje vrednosti koje ne bi trebalo da utiču na upit ni na koji način. Baš kao što je slučaj i sa SELECT klauzulom, u ovoj aplikaciji svi upiti imaju isti OPTIONAL deo. To je učinjeno kako bi se dobile sve dostupne informacije o pametnim telefonima, bez obzira na upit. Zahvaljujući tome, prilikom pretrage pametnih telefona, sve relevantne informacije mogu biti prikazane korisniku, kao što je prikazano na slici ispod.

![Smart phone output](/images/smart_phone_output.png "Smart phone output")

## Upiti na prirodnom jeziku

Najprirodniji način interakcije sa chatbotom bio bi kroz postavljanje pitanja na prirodnom jeziku i dobijanje tačnih informacija kao rezultat. I dok se nekima ovo možda ne čini izvodljivim, [langchain](https://python.langchain.com/docs/get_started/introduction) biblioteka pruža API u tu svrhu. [GraphSparqlQAChain](https://python.langchain.com/docs/use_cases/graph/graph_sparql_qa) omogućava primenu velikih jezičkih modela kao interfejsa na prirodnom jeziku ka graf bazi podataka generisanjem SPARQL upita. Nažalost, ovo je i dalje relativno nova stvar i kao takva ima dosta nedostataka. Ipak, ovaj pristup je isproban u ovoj aplikaciji, a rezultati su dokumentovani u nastavku.

<br />

Kod ispod predstavlja inicijalizaciju chain-a unutar klase NaturalLanguageQuery.

```
self.graph = RdfGraph(
            source_file="ontology/GoodRelationsPopulatedLite.ttl",
            standard="owl",
            serialization="ttl",
            local_copy="ontology/GoodRelationsPopulatedLite.ttl",
        )
self.graph.load_schema()

self.chain = GraphSparqlQAChain.from_llm(
    ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0), graph=self.graph, verbose=True,
)
```

Na početku, ontologija se učitava iz izvornog fajla. Važno je učitati populisanu ontologiju, jer izvršavanje lanca radi na sledeći način:
1. Utvrđuje se namera upita
2. Generiše se i izvršava SPARQL upit nad ontologijom
3. Generiše se izlaz u zavisnosti od rezultata izvršavanja upita

Treba napomenuti da je jedini način za učitavanje grafa korišćenjem turtle sintakse, jer učitavanje fajlova u RDF/XML sintaksi izaziva greške u trenutku pisanja. Nakon što je graf učitan, lanac se kreira korišćenjem OpenAI modela gpt-3.5-turbo-16k, koji prihvata 16 000 tokena u zahtevu, u poređenju sa 4096 tokena koje prihvata podrazumevani gpt-3.5-turbo model. Ovo je važno jer originalna ontologija smeštena unutar fajla GoodRelationsPopulated.owl znatno premašuje ograničenje tokena (ograničenje je 40 000 tokena u minutu, ontologija ima preko 2 miliona tokena). Da bi se prevazišla ova prepreka, iz ontologije su uklonjene sve nekorišćene klase, svojstva i pojedinci, rezultujući ontologijom smeštenom unutar fajla [GoodRelationsPopulatedLite.ttl](./ontology/GoodRelationsPopulatedLite.ttl), koja ne premašuje ograničenje tokena.

<br />

Nakon inicijalizacije lanca, korisnički upiti mogu biti poslati modelu, a rezultati se mogu prikazati. Međutim, kako je ovo i dalje u razvoju, upit koji korisnik unese mora da bude vrlo precizan kako bi dobio željene informacije. Kada se šalje upit bez dodatnih informacija, model nikada ne generiše tačan SPARQL upit. Da bi se rešio ovaj problem, uz upit se šalje dodatni kontekst, koji se koristi kako bi se povećala preciznost modela prilikom generisanja SPARQL upita. Kontekst je prikazan ispod.

```
self.context = """ Use following rules:
                    Don't exclude any results, I want the full list. 
                    Phone must be a rdf:type or rdfs:subClassOf http://www.co-ode.org/ontologies/ont.owl#SmartPhone. 
                    For hasBrand use http://www.co-ode.org/ontologies/ont.owl#hasBrand. 
                    Brand name in query must be written in all lowercase.
                    Brand name represents object for hasBrand. 
                    For hasPrice use http://www.co-ode.org/ontologies/ont.owl#hasPrice.
                    Camera Mpx is type of xsd:double.
                    All prices are in euros."""
```

Kontekst je kreiran eksperimentalno. Bez ovog konteksta, ako rezultat ima mnogo pametnih telefona, model bi prikazao samo 5 od njih. Takođe, ne bi pisao proizvođača malim slovima, čak i ako je to učinjeno u upitu. Zato što se GoodRelations koristi kao osnovna ontologija, koristio bi hasBrand i hasPrice iz nje, umesto onih iz dostavljene ontologije. Pokušan je pristup dodavanja labela i komentara ovim svojstvima, ali to nije promenilo ništa. Međutim, nakon dodavanja konteksta, ako je korisnički upit dovoljno precizan, model bi prikazao tačne rezultate.

<br />

Da bi se testirao ovaj način korišćenja chatbota, uneti su različiti tipovi upita na različite načine. Zaključak je da je ovo i dalje daleko od upotrebljivog za obične korisnike. Glavni razlog za to je što korisnički upiti moraju biti izuzetno precizni kako bi model generisao tačan SPARQL upit. Nivo preciznosti je toliko visok da korisnici koji ne poznaju ontologiju verovatno neće moći da nađu ono što traže. Ovaj faktor sam po sebi čini ovaj pristup praktično neupotrebljivim. Drugi problem je nasumičnost koju uzrokuje model. Zavisno o tome kada je unet korisnički upit, model može generisati različite SPARQL upite za iste korisničke upite. Na kraju, ograničenje tokena postavljeno od strane modela može ograničiti upotrebljivost samo na relativno male ontologije. Kako je ovo i dalje rad u toku, očekuje se da će ovi problemi biti svedeni na minimum ili potpuno otklonjeni u budućnosti.

## Zaključak

Kako bi se kreirao chatbot za predlaganje pametnih telefona, prvo je kreirana ontologija za pametne telefone. GoodRelations ontologija je korišćena kao osnova, i proširena je sa potrebnim klasama, svojstvima i individualima. Zatim je ontologija populisana individualima sa veb sajta [Mobilni Svet](https://mobilnisvet.com/), koristeći programski jezik Python i biblioteke Selenium, BeautifulSoup i rdflib. Nakon toga, chatbot je kreiran kao konzolna aplikacija koja korisnicima omogućava da biraju između 10 predefinisanih načina na koje žele pretraživati pametne telefone. Na kraju, korisnicima je data opcija da unesu upite na prirodnom jeziku, iako je ova funkcionalnost više eksperimentalna nego upotrebljiva.

## Kako pokrenuti
Instalirajte sve zavisnosti iz fajla [requirements.txt](./requirements.txt), unesite važeći OpenAI API ključ unutar fajla .env i pokrenite [main.py](./main.py).