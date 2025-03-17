import requests
import json
from query import query_graphdb

endpoint = "https://dbpedia.org/sparql"

dataset = []

with open("desportos.json", "r", encoding='utf-8') as f:
    desportos = json.load(f)

for d in desportos:
    sparql_query = f'''
    SELECT DISTINCT ?nome ?abs WHERE {{
        <{d}> rdfs:label ?nome ;
        dbo:abstract ?abs .
        FILTER(LANG(?abs) = "en" && LANG(?nome) = "en")
    }} LIMIT 100
    '''
    result = query_graphdb(endpoint, sparql_query)
    
    sparql_query_atletas = f'''
    SELECT DISTINCT * WHERE {{
        ?id a schema:Person ;
        dbp:sport <{d}> ;
        
        dbp:name ?nome ;
        dbp:nationality ?origem ;
        dbp:birthDate ?dataNasc .
        FILTER(lang(?nome) = "en" && lang(?origem) = "en")
    }} LIMIT 1000
    '''
    
    result_atletas = query_graphdb(endpoint, sparql_query_atletas)
    
    info_atletas = []
    for a in result_atletas['results']['bindings']:
        info_atletas.append(
            {
                "id": a['id']['value'],
                "nome": a['nome']['value'],
                "origem": a['origem']['value'],
                "dataNasc": a['dataNasc']['value']
            }
        )
    
    dataset.append(
        {
            "id": d,
            "designacao": result['results']['bindings'][0]['nome']['value'],
            "abs": result['results']['bindings'][0]['abs']['value'],
            "atletas": info_atletas
        }
    )
    
with open("dataset.json", "w", encoding='utf-8') as f:
    json.dump(dataset, f, ensure_ascii=False, indent=4)