# Chatbot for suggesting smart phones

## Introduction

The popularity of smart phones is constantly on the rise, and the number of available smart phone models keeps increasing day by day. In a way this is good, because it allows buyers to have more options when choosing a smart phone for themselves. There are many different websites that allow users to search for smart phones, and users can, most of the time, find a smart phone that fits their needs. However, having more options can be confusing for users who don't exactly know what they are looking for. Usually, such users end up buying a phone which doesn't suit them perfectly, and end up replacing it relatively quickly. To avoid this from happening, users can try to learn more about smart phones, so they know what exactly is important for them, or there could be some kind of an assistant helping users make the right decision while purchasing a smart phone.

<br />

The goal of this application is to allow users to easily find a smart phone for them, by providing a chatbot assistant. This will be done by creating an ontology for smart phones. After that, ontology will be populated with the newest smart phones, so that users can find smart phones which fit their needs by asking the chatbot.

## Ontology

In order to create this chatbot assistant, the first step is creating the ontology for smart phones. This is done by using [GoodRelations](http://purl.org/goodrelations/) as a base ontology, and expanding it with smart phone related information. GoodRelations is a lightweight ontology for excahing e-commerce information, and it can be used in all RDF syntaxes. To add smart phone information, a class SmartPhone is created as a subclass of the class [Individual](http://purl.org/goodrelations/v1#Individual), and all smart phone models are subclass of the class SmartPhone. For example, a smart phone model could be Samsung Galaxy S23, and individuals of this type would be Samsung Galaxy S23+, Samsung Galaxy S23 Ultra etc. Each smart phone has a brand, which is modeled using a class [Brand](http://purl.org/goodrelations/v1#Brand) and adding an object property hasBrand. Information about RAM, storage, camera, screen type, chipset and OS is modeled the same way, except that a new class is created for each type of these smart phone attributes. Creating classes for these attributes allows setting restrictions for smart phone models. If we use same Samsung Galaxy S23 model as an example, smart phones of this model can only have camera with either 200 or 50 Mpx. Finally, to model information about smart phone price, sale date, screen size, screen resolution and color, datatype proprties are used. This ontology is stored in a [GoodRelations.owl](./ontology/GoodRelations.owl) file, inside ontology folder.

<br />

Once the ontology is created, next step is populating it with smart phone individuals. Using Python programming language, website [Mobilni Svet](https://mobilnisvet.com/) is scraped to get information for this purpose. Smart phones of the following brands were taken into considerations: 
* [Apple](https://mobilnisvet.com/mobilni-proizvodjac/Apple/22/2)
* [Google](https://mobilnisvet.com/mobilni-proizvodjac/Google/71/2)
* [Huawei](https://mobilnisvet.com/mobilni-proizvodjac/Huawei/35/2)
* [OnePlus](https://mobilnisvet.com/mobilni-proizvodjac/OnePlus/55/2)
* [Poco](https://mobilnisvet.com/mobilni-proizvodjac/Poco/84/2)
* [Samsung](https://mobilnisvet.com/mobilni-proizvodjac/Samsung/6/2)
* [Xiaomi](https://mobilnisvet.com/mobilni-proizvodjac/Xiaomi/52/2)

For each brand, links to detailed pages are collected for every smart phone that is released in 2020 or later. After that, every collected link is processed in order to acquire relevant information for corresponding smart phone. Python library [Selenium](https://selenium-python.readthedocs.io/) is used to get html source for every brand page and for every detailed smart phone page. Then, library [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) is used to navigate through html and to get all relevant information. Information about smart phones is stored in memory, and once all links are processed, ontology is populated based on the stored data. For this purpose, library [rdflib](https://rdflib.readthedocs.io/en/stable/) is used, which is a Python library for working with RDF, that contains parsers/serializers for almost all of the known RDF serializations. The library contains a class named Graph, which represents an RDF graph. Method parse() is used to parse an RDF source, adding the resulting triples to the Graph. Graph can be modified using the method add(), which accepts triplets that represent subject, predicate and object. Finally, method serialize() is used to serialize graph into an OWL file. 

<br />

The described functionality is located inside a [scrape.py](./scrape.py) file. Populated ontology is stored in a [GoodRelationsPopulated.owl](./ontology/GoodRelationsPopulated.owl) file. Class [OWLManager](./ontology_helpers/OWLManager.py) encapsulates functionalities provided by the library rdflib.

## Chatbot

Chatbot is implemented as a console application which gives users options to search smart phones based on their characteristics. Picture below represents the class diagram of this application.

![Chatbot class diagram](/images/class_diagram.png "Chatbot class diagram")

Class [Menu](./UI/Menu.py) is responsible for:
* showing available options to users
* getting their input by using [ConsoleUserInterface](./UI/ConsoleUserInteraction.py) class
* depending on user input, executing correct [Command](./command_pattern/PhonesCommands.py) or displaying an error message

There are 11 predefined options, each searching smart phones based on different characteristics. Users can:
* Search phones by brand, date and price
* Search phones by brand and OS
* Search phones with specified camera
* Search phones by chipset, ram and storage
* Search phones by screen size and resolution
* Search phones with specified color
* Search cheapest phone for brand
* Find cheapest phone with best camera by brand, date and max price
* Search phones with specified camera younger than specified date
* Search colors for phone model
* Write query in natural language (experimental)

Each option has a corresponding command, which uses ConsoleUserInterface to get additional input from user and [SPARQLManager](./ontology_helpers/SPARQLManager.py) to get smart phone individuals from populated ontology. Each command has 2 methods: description() and execute(). The first method is used to describe what the command does. This is used to represent commands as options to users. The second method is used to execute the correct command based on user input. Inside this method, additional input is retrieved from user which is used as an argument for corresponding method from SPARQLManager. Class SPARQLManager has total of 10 methods, which correspond to first 10 commands, and is not used only when writing query in natural language. It uses OWLManager for retrieving individuals and class names from ontology, which are used for creating SPARQL queries.

<br />

SPARQL is an RDF query language, which is used for retrieving and manipulating data stored in RDF format. SPARQL allows for query to consist of triple patterns, conjunctions, disjunctions, and optional patterns. The most used SPARQL query is SELECT query, which is used to extract raw values from a SPARQL endpoint. The SELECT query consists of several parts. It starts with SELECT clause, which is followed by variable names that will be shown when the query is executed. Next is WHERE clause which defines the data selection condition and generates the variables. FILTER clause restricts the variable generation so that variables are generated only if FILTER clause returns TRUE. OPTIONAL is a binary operator which is used for generating variables if they have a value, and if not, variables will be without value. This operator does not restrict query in any way, instead it only retrieves data if it exists. 

<br />

In this application, each method in SPARQLManager creates a SPARQL query based on its parameters. Code below represents SPARQL query for searching phones by brand and OS.

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

In this application, all SPARQL queries have the same variables listed in SELECT clause. These variables represent relevant smart phone information that is stored inside the ontology which was previously described. WHERE clause is used for defining a condition, and each SPARQL query has a different WHERE clause. In the code above, WHERE clause defines a condition which is used for searching smart phones that have certain brand and OS. OPTIONAL operator is used for retrieving values which should not affect query in any way. Just like its the case with SELECT clause, in this application all queries have same OPTIONAL part. This is done so that all available information about smart phones is retrieved, no matter the query. Thanks to this, when searching for smart phones, all relevant information can be displayed to the user, as shown in the image below.

![Smart phone output](/images/smart_phone_output.png "Smart phone output")

## Natural language queries

The most natural way of interacting with the chatbot would be asking questions in natural language, and getting accurate information as a result. While for some this may not sound as possible, [langchain](https://python.langchain.com/docs/get_started/introduction) library provides an API for this purpose. [GraphSparqlQAChain](https://python.langchain.com/docs/use_cases/graph/graph_sparql_qa) allows application of large language models as a natural language interface to a graph database by generating SPARQL. Unfortunately, this is still a relatively new thing, and as such it has quite a few flaws. Nevertheless, this approach is tried out in this application, and results are documentated in the continuation.

<br />

The code below represents initializing langchain chain inside the NaturalLanguageQuery class.

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

Firstly, ontology is loaded from a source file. It is important to load the populated ontology, because running the chain works in a following way: 
1. Determine the intent of the query
2. Generate and run SPARQL query on the provided ontology
3. Generate output based on query results

It should be noted that the only way to load graph is by using turtle syntax, because loading files that are in RDF/XML syntax is throwing errors at the time of writing. After the graph is loaded, the chain is created using OpenAI model gpt-3.5-turbo-16k, which accepts 16 000 tokens in the request, compared to 4096 tokens which are accepted by the default gpt-3.5-turbo model. This is important, because original ontology located inside GoodRelationsPopulated.owl file is exceeding the token limit by a lot (the limit is 40 000 per minute, the ontology has over 2 million tokens). To overcome this obstacle, the ontology is stripped of all unused classes, properties and individuals, resulting in the ontology located inside the [GoodRelationsPopulatedLite.ttl](./ontology/GoodRelationsPopulatedLite.ttl) file, that does not exceed the token limit.

<br />

After initializing the chain, user queries can be sent to the model and results can be displayed. However, as this is still work in progress, query entered by a user needs to be very precise in order to retrieve desired information. When sending query without any additional information, model would never generate a correct SPARQL query. To solve this issue, additional context is sent alongside the query, which is used to increase the accuracy of the model when generating a SPARQL query. The context is shown below.

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

The context was created experimentally. Without this context, if the result has a lot of smart phones, model would only display 5 of them. It would also not write brand in all lowercase, even if it is in lowercase in the query. Because GoodRelations is used as a base ontology, it would use hasBrand and hasPrice from it, instead of those from the provided ontology. The approach of adding labels and comments to these properties was tried out, but did not change anything. However, after adding the context, if the user query is precise enough, the model would display correct results.

<br />

To test this way of using the chatbot, different types of queries were entered in various ways. The conclusion is that this is still far from usable for regular users. The main reason for this is that user queries need to be highly precise for the model to generate a correct SPARQL query. The level of precision is so high that users who don't know the ontology are mostly not going to be able to get what they are looking for. This factor alone makes this approach basically unusable. Another issue is randomness caused by the model. Depending on when the user query was entered, model can generate different SPARQL queries for the same user queries. Finally, the token limit set by the model can restrict usability only to relatively small ontologies. As this is still work in progress, it is expected that these problems will be minimized or completely removed in the future.

## Conclusion

In order to create chatbot for suggesting smart phones, the ontology for smart phones was created first. GoodRelations ontology was used as a base, and it was expanded with required classes, properties and individuals. Next, this ontology was populated with individuals from the website [Mobilni Svet](https://mobilnisvet.com/), by using programming language Python and libraries Selenium, BeautifulSoup and rdflib. After that, chatbot was created as a console application that allows users to chose from 10 predefined ways in which they want to search smart phones. Finally, users were given an option to enter queries in natural language, though this feature was more experimental than usable.

## How to run
Install all dependencies from [requirements.txt](./requirements.txt) file, enter a valid OpenAI API key inside .env file and run [main.py](./main.py).