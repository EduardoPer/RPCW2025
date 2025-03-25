import pandas, re, sys

fileBase = '''@prefix : <http://www.rpcw.di.uminho.pt/2025/cinema/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.rpcw.di.uminho.pt/2025/cinema/> .

<http://www.rpcw.di.uminho.pt/2025/cinema> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://www.rpcw.di.uminho.pt/2025/cinema#atuou
:atuou rdf:type owl:ObjectProperty ;
       owl:inverseOf :temAtor .


###  http://www.rpcw.di.uminho.pt/2025/cinema#compôs
:compôs rdf:type owl:ObjectProperty ;
        owl:inverseOf :foiComposta ;
        rdfs:domain :Pessoa ;
        rdfs:range :Obra .


###  http://www.rpcw.di.uminho.pt/2025/cinema#escreveu
:escreveu rdf:type owl:ObjectProperty ;
          owl:inverseOf :foiEscrita ;
          rdfs:domain :Pessoa ;
          rdfs:range :Obra .


###  http://www.rpcw.di.uminho.pt/2025/cinema#foiComposta
:foiComposta rdf:type owl:ObjectProperty .


###  http://www.rpcw.di.uminho.pt/2025/cinema#foiEscrita
:foiEscrita rdf:type owl:ObjectProperty .


###  http://www.rpcw.di.uminho.pt/2025/cinema#realizou
:realizou rdf:type owl:ObjectProperty ;
          owl:inverseOf :temRealizador .


###  http://www.rpcw.di.uminho.pt/2025/cinema#representa
:representa rdf:type owl:ObjectProperty ;
            rdfs:domain :Ator ;
            rdfs:range :Personagem .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temArgumento
:temArgumento rdf:type owl:ObjectProperty ;
              rdfs:domain :Filme ;
              rdfs:range :Argumento .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temAtor
:temAtor rdf:type owl:ObjectProperty ;
         rdfs:domain :Filme ;
         rdfs:range :Pessoa .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temGénero
:temGénero rdf:type owl:ObjectProperty ;
           rdfs:domain :Filme ;
           rdfs:range :Género .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temLíngua
:temLíngua rdf:type owl:ObjectProperty ;
           rdfs:domain :Filme ;
           rdfs:range :Língua .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temPaísOrigem
:temPaísOrigem rdf:type owl:ObjectProperty ;
               rdfs:domain :Filme ;
               rdfs:range :País .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temPersonagem
:temPersonagem rdf:type owl:ObjectProperty ;
               owl:inverseOf :éPersonagem .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temPeçaMusical
:temPeçaMusical rdf:type owl:ObjectProperty ;
                rdfs:domain :Filme ;
                rdfs:range :Peça_Musical .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temRealizador
:temRealizador rdf:type owl:ObjectProperty ;
               rdfs:domain :Filme ;
               rdfs:range :Pessoa .


###  http://www.rpcw.di.uminho.pt/2025/cinema#éPersonagem
:éPersonagem rdf:type owl:ObjectProperty ;
             rdfs:domain :Personagem ;
             rdfs:range :Filme .


#################################################################
#    Data properties
#################################################################

###  http://www.rpcw.di.uminho.pt/2025/cinema#data
:data rdf:type owl:DatatypeProperty ;
      rdfs:domain :Filme ;
      rdfs:range xsd:string .


###  http://www.rpcw.di.uminho.pt/2025/cinema#duração
:duração rdf:type owl:DatatypeProperty ;
         rdfs:domain :Filme ;
         rdfs:range xsd:integer .


###  http://www.rpcw.di.uminho.pt/2025/cinema#temSexo
:temSexo rdf:type owl:DatatypeProperty ;
         rdfs:range xsd:string .


###  http://www.rpcw.di.uminho.pt/2025/cinema#título
:título rdf:type owl:DatatypeProperty ;
        rdfs:domain :Filme ;
        rdfs:range xsd:string .


#################################################################
#    Classes
#################################################################

###  http://www.rpcw.di.uminho.pt/2025/cinema#Argumento
:Argumento rdf:type owl:Class ;
           rdfs:subClassOf :Obra .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Ator
:Ator rdf:type owl:Class ;
      owl:equivalentClass [ owl:intersectionOf ( :Pessoa
                                                 [ rdf:type owl:Restriction ;
                                                   owl:onProperty :atuou ;
                                                   owl:someValuesFrom :Filme
                                                 ]
                                               ) ;
                            rdf:type owl:Class
                          ] ,
                          [ rdf:type owl:Class ;
                            owl:unionOf ( :AtorFeminino
                                          :AtorMasculino
                                        )
                          ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#AtorFeminino
:AtorFeminino rdf:type owl:Class ;
              owl:equivalentClass [ owl:intersectionOf ( :Ator
                                                         [ rdf:type owl:Restriction ;
                                                           owl:onProperty :temSexo ;
                                                           owl:hasValue "F"
                                                         ]
                                                       ) ;
                                    rdf:type owl:Class
                                  ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#AtorMasculino
:AtorMasculino rdf:type owl:Class ;
               owl:equivalentClass [ owl:intersectionOf ( :Ator
                                                          [ rdf:type owl:Restriction ;
                                                            owl:onProperty :temSexo ;
                                                            owl:hasValue "M"
                                                          ]
                                                        ) ;
                                     rdf:type owl:Class
                                   ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Escritor
:Escritor rdf:type owl:Class ;
          owl:equivalentClass [ owl:intersectionOf ( :Pessoa
                                                     [ rdf:type owl:Restriction ;
                                                       owl:onProperty :escreveu ;
                                                       owl:someValuesFrom [ rdf:type owl:Class ;
                                                                            owl:unionOf ( :Argumento
                                                                                          :Livro
                                                                                        )
                                                                          ]
                                                     ]
                                                   ) ;
                                rdf:type owl:Class
                              ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Filme
:Filme rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#FilmesAmericanos
:FilmesAmericanos rdf:type owl:Class ;
                  owl:equivalentClass [ owl:intersectionOf ( :Filme
                                                             [ rdf:type owl:Restriction ;
                                                               owl:onProperty :temPaísOrigem ;
                                                               owl:hasValue :Estados_Unidos
                                                             ]
                                                           ) ;
                                        rdf:type owl:Class
                                      ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#FilmesAventura
:FilmesAventura rdf:type owl:Class ;
                owl:equivalentClass [ owl:intersectionOf ( :Filme
                                                           [ rdf:type owl:Restriction ;
                                                             owl:onProperty :temGénero ;
                                                             owl:hasValue :Aventura
                                                           ]
                                                         ) ;
                                      rdf:type owl:Class
                                    ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#FilmesDramáticos
:FilmesDramáticos rdf:type owl:Class ;
                  owl:equivalentClass [ owl:intersectionOf ( :Filme
                                                             [ rdf:type owl:Restriction ;
                                                               owl:onProperty :temGénero ;
                                                               owl:hasValue :Drama
                                                             ]
                                                           ) ;
                                        rdf:type owl:Class
                                      ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#FilmesInfantis
:FilmesInfantis rdf:type owl:Class ;
                owl:equivalentClass [ owl:intersectionOf ( :Filme
                                                           [ rdf:type owl:Restriction ;
                                                             owl:onProperty :temGénero ;
                                                             owl:hasValue :Infantil
                                                           ]
                                                         ) ;
                                      rdf:type owl:Class
                                    ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#FilmesRomânticos
:FilmesRomânticos rdf:type owl:Class ;
                  owl:equivalentClass [ owl:intersectionOf ( :Filme
                                                             [ rdf:type owl:Restriction ;
                                                               owl:onProperty :temGénero ;
                                                               owl:hasValue :Romance
                                                             ]
                                                           ) ;
                                        rdf:type owl:Class
                                      ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Género
:Género rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Livro
:Livro rdf:type owl:Class ;
       rdfs:subClassOf :Obra .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Língua
:Língua rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Música
:Música rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Músico
:Músico rdf:type owl:Class ;
        owl:equivalentClass [ owl:intersectionOf ( :Pessoa
                                                   [ rdf:type owl:Restriction ;
                                                     owl:onProperty :compôs ;
                                                     owl:someValuesFrom :Obra
                                                   ]
                                                 ) ;
                              rdf:type owl:Class
                            ] .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Obra
:Obra rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#País
:País rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Personagem
:Personagem rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Pessoa
:Pessoa rdf:type owl:Class .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Peça_Musical
:Peça_Musical rdf:type owl:Class ;
              rdfs:subClassOf :Obra .


###  http://www.rpcw.di.uminho.pt/2025/cinema#Realizador
:Realizador rdf:type owl:Class ;
            owl:equivalentClass [ owl:intersectionOf ( :Pessoa
                                                       [ rdf:type owl:Restriction ;
                                                         owl:onProperty :realizou ;
                                                         owl:someValuesFrom :Filme
                                                       ]
                                                     ) ;
                                  rdf:type owl:Class
                                ] .


#################################################################
#    Individuals
#################################################################
'''

lastLine = "###  Generated by the OWL API (version 4.5.29.2024-05-13T12:11:03Z) https://github.com/owlcs/owlapi"
ttl_url = '###  http://www.rpcw.di.uminho.pt/2025/cinema#'

def writeOntologyInTTL(outFilename, movies_csv, actors_csv, characters_csv, ttl_base, ttl_last_line, ttl_url, movies_number):
    moviesDF = pandas.read_csv(movies_csv)
    #print(charactersDF[charactersDF["nconst"] == "nm0478475"])
    genres = []
    regions = []
    languages = []
    titles = {}
    actor_characters = {}
    actor_movies = {}

    movies_ttl_all = ""
    movies_ttl_all += ttl_base
    curr_movie_nr = 0
    for row in moviesDF.itertuples(name="row"):
        movie_title = row.primaryTitle.replace(" ", "_").replace(":", "_").replace(".", "_").replace(",", "_").replace(";", "").replace("'", "").replace("?", "").replace("(", "").replace(")", "").replace("!", "").replace("\\", "_").replace("/", "_").replace("&", "and")
        movie_title = re.sub(r'[^A-Za-zÀ-ÖØ-öø-ÿ\_]', r'_', movie_title)
        movie_code = row.tconst
        if titles.get(movie_code) == None:
            titles[movie_code] = movie_title
        else:
            continue
        
        movie_genres = row.genres.split(',')
        for g in movie_genres:
            if g.replace(" ", "_") not in genres:
                genres.append(g.replace(" ", "_"))
        movie_region = row.region.replace(" ", "_").upper()
        if movie_region not in regions:
            regions.append(movie_region)
        movie_lang = row.language.replace(" ", "_").lower()
        if movie_lang not in languages:
            languages.append(movie_lang)
        movie_runtime = int(row.runtimeMinutes)
        movie_year = int(row.startYear)
        
        movie_genre_entry = ""
        for i in range(0, len(movie_genres)):
            g = movie_genres[i].replace(" ", "_")
            if i == 0 and len(movie_genres) == 1:
                movie_genre_entry += f":temGénero :{g} ;"
            elif i == 0:
                movie_genre_entry += f":temGénero :{g} ,\n"
            elif i == (len(movie_genres)-1):
                movie_genre_entry += f"                     :{g} ;"
            else:
                movie_genre_entry += f"                     :{g} ,\n"
        
        movies_ttl_all += f'''
{ttl_url}{movie_title}
:{movie_title} rdf:type owl:NamedIndividual ,
                   :Filme ;
          {movie_genre_entry}
          :temLíngua :{movie_lang} ;
          :temPaísOrigem :{movie_region} ;
          :data "{movie_year}" ;
          :duração {movie_runtime} .
        
'''
        curr_movie_nr += 1
        if curr_movie_nr >= movies_number:
            break
        
    moviesDF = None
    charactersDF = pandas.read_csv(characters_csv)

    for row in charactersDF.itertuples(name="row"):
        character_name = row.characters.replace('["', '').replace('"]', '').replace(" ", "_").replace(" ", "_").replace(":", "_").replace(".", "_").replace(",", "_").replace(";", "").replace("'", "").replace("?", "").replace("(", "").replace(")", "").replace("!", "").replace("\\", "_").replace("/", "_").replace("&", "and")
        character_name = re.sub(r'[^A-Za-zÀ-ÖØ-öø-ÿ\_]', r'_', character_name)
        
        if titles.get(row.tconst) == None:
            continue
        
        movie_name = titles[row.tconst]
        actor_code = row.nconst
        
        
        if actor_characters.get(actor_code) == None:
            actor_characters[actor_code] = [character_name]
        else:
            actor_characters[actor_code] = actor_characters[actor_code].append(character_name)
        
        if actor_movies.get(actor_code) == None:
            actor_movies[actor_code] = [movie_name]
        else:
            actor_movies[actor_code] = actor_movies[actor_code].append(movie_name)
        
        movies_ttl_all += f'''
{ttl_url}{character_name}
:{character_name} rdf:type owl:NamedIndividual ,
               :Personagem ;
      :éPersonagem :{movie_name} .

'''
    charactersDF = None
    actorsDF = pandas.read_csv(actors_csv)

    for row in actorsDF.itertuples(name="row"):
        actor_code = row.nconst
        actor_name = row.primaryName.replace(" ", "_").replace('["', '').replace('"]', '').replace(" ", "_").replace(" ", "_").replace(":", "_").replace(".", "_").replace(",", "_").replace(";", "").replace("'", "").replace("?", "").replace("(", "").replace(")", "").replace("!", "").replace("\\", "_").replace("/", "_").replace("&", "and")
        actor_name = re.sub(r'[^A-Za-zÀ-ÖØ-öø-ÿ\_]', r'_', actor_name)
        
        movs = actor_movies.get(actor_code)
        chars = actor_characters.get(actor_code)
        
        actor_movs_entry = ""
        if movs != None:
            for i in range(0, len(movs)):
                if i == 0 and len(movs) == 1 and chars != None:
                    actor_movs_entry += f" ;\n             :atuou :{movs[i]} ;"
                elif i == 0 and len(movs) == 1:
                    actor_movs_entry += f" ;\n             :atuou :{movs[i]}"
                elif i == 0:
                    actor_movs_entry += f" ;\n             :atuou :{movs[i]} ,\n"
                elif i == (len(movie_genres)-1) and chars != None:
                    actor_movs_entry += f"                     :{movs[i]} ;"
                elif i == (len(movie_genres)-1):
                    actor_movs_entry += f"                     :{movs[i]}"
                else:
                    actor_movs_entry += f"                     :{movs[i]} ,\n"
        
        actor_chars_entry = ""
        if chars != None:
            for i in range(0, len(chars)):
                if i == 0 and len(movs) == 1 and chars != None:
                    actor_chars_entry += f"\n             :representa :{chars[i]}"
                elif i == 0 and len(chars) == 1:
                    actor_chars_entry += f" ;\n             :representa :{chars[i]}"
                elif i == 0:
                    actor_chars_entry += f" ;\n             :representa :{chars[i]} ,\n"
                elif i == (len(movie_genres)-1):
                    actor_chars_entry += f"                     :{chars[i]}"
                else:
                    actor_chars_entry += f"                     :{chars[i]} ,\n"  
        if not(movs == None and chars == None):
            movies_ttl_all += f'''
{ttl_url}{actor_name}
:{actor_name} rdf:type owl:NamedIndividual ,
                    :Pessoa{actor_movs_entry}{actor_chars_entry} .
                    
'''
    actorsDF = None
    
    for r in regions:
        movies_ttl_all += f'''
{ttl_url}{r}
:{r} rdf:type owl:NamedIndividual ,
                         :País .
                         
'''
    for l in languages:
        movies_ttl_all += f'''
{ttl_url}{l}
:{l} rdf:type owl:NamedIndividual ,
                  :Língua .
                  
'''
    
    
    movies_ttl_all += ttl_last_line
    
    with open(outFilename, "w", encoding='utf-8') as f:
        f.write(movies_ttl_all)
        
        

if __name__ == "__main__":
    nMovies = 500
    if len(sys.argv) > 1 and len(sys.argv) < 3:
        nMovies = int(sys.argv[1])
        writeOntologyInTTL("imdb_cinema_info.ttl", "movies.csv", "actors.csv", "principals.csv", fileBase, lastLine, ttl_url, nMovies)
    elif len(sys.argv):
        writeOntologyInTTL("imdb_cinema_info.ttl", "movies.csv", "actors.csv", "principals.csv", fileBase, lastLine, ttl_url, 99999999999)
    else:
        print("Command: python3 tpc5_ontology.py [optional: nMovies]")