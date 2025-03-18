import requests
import json
from query import query_graphdb
from collections import Counter

endpoint = "https://dbpedia.org/sparql"


# nao encontro genero nem data
sparql_query_movies = f'''
SELECT distinct ?m ?titulo ?abstrato ?país ?realizador WHERE {{
    ?m a <http://schema.org/Movie> ;
       rdfs:label     ?titulo ;
       dbo:abstract   ?abstrato .
    FILTER(lang(?titulo) = "en")
    FILTER(lang(?abstrato) = "en")
}} LIMIT 10
'''
result_movies = query_graphdb(endpoint, sparql_query_movies)['results']['bindings']
actors = []
movies = []

for m in result_movies:
    auxMovie = {}
    auxMovie['id'] = m['m']['value']
    auxMovie['titulo'] = m['titulo']['value']
    auxMovie['abstrato'] = m['abstrato']['value']
    auxMovie['país'] = []
    auxMovie['realizador'] = []
    
    sparql_query_paises = f'''
    SELECT distinct ?país WHERE {{
        <{m['m']['value']}> dbp:country ?país .
        FILTER(lang(?país) = "en")
    }}
    '''
    result_movie_paises = query_graphdb(endpoint, sparql_query_paises)['results']['bindings']
    for p in result_movie_paises:
        auxMovie['país'].append(p['país']['value'])
    
    sparql_query_realizadores = f'''
    SELECT distinct ?realizador WHERE {{
        <{m['m']['value']}> dbo:director/rdfs:label ?realizador .
        FILTER(lang(?realizador) = "en")
    }}
    '''
    result_movie_realizadores = query_graphdb(endpoint, sparql_query_realizadores)['results']['bindings']
    for p in result_movie_realizadores:
        auxMovie['realizador'].append(p['realizador']['value'])
        
    sparql_query_movie_actors = f'''
    SELECT distinct ?actor WHERE {{
        <{m['m']['value']}> dbo:starring ?actor .
        
    }}
    '''
    result_movie_actors = query_graphdb(endpoint, sparql_query_movie_actors)['results']['bindings']
    movie_actors_ids = []
    for a in result_movie_actors:
        movie_actors_ids.append(a['actor']['value'])
        auxActor = {}
        auxActor['id'] = a['actor']['value']
        name_placeHolder = a['actor']['value'].split('/')[-1].replace("_", " ")
        sparql_query_actor = f'''
        SELECT distinct ?nome ?dataNasc ?origem  WHERE {{
            OPTIONAL {{ <{a['actor']['value']}> rdfs:label ?nome }}
            OPTIONAL {{ <{a['actor']['value']}> dbo:birthDate ?dataNasc }}
            OPTIONAL {{ <{a['actor']['value']}> dbp:birthPlace ?origem }}
            FILTER(lang(?nome) = "en")
            }}
        '''
        
        result_actor = query_graphdb(endpoint, sparql_query_actor)['results']['bindings']
        auxActor['nome'] = (result_actor[0]['nome']['value'] if result_actor[0].get('nome') != None else name_placeHolder)
        auxActor['dataNasc'] = (result_actor[0]['dataNasc']['value'] if result_actor[0].get('dataNasc') != None else name_placeHolder)
        auxActor['origem'] = (result_actor[0]['origem']['value'] if result_actor[0].get('origem') != None else name_placeHolder)
        
        if auxActor not in actors:
            actors.append(auxActor)

    auxMovie['elenco'] = movie_actors_ids
    if auxMovie not in movies:
        movies.append(auxMovie)

with open('dados_autores.json', 'w', encoding='utf-8') as f:
    json.dump(actors, f, ensure_ascii=False, indent=4)

with open('dados_filmes.json', 'w', encoding='utf-8') as f:
    json.dump(movies, f, ensure_ascii=False, indent=4)