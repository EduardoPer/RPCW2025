from rdflib import Graph, Namespace, OWL, RDF, Literal
import requests

def query_graphdb(endpoint_url, sparql_query):
    headers = {
        'Accept': 'text/turtle',
    }

    response = requests.get(endpoint_url, params={'query': sparql_query}, headers=headers)

    if response.status_code == 200:
        g = Graph()
        g.parse(data=response.text, format='turtle')
        return g
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
endpoint = "http://localhost:7200/repositories/disease-ontology"
q12 = """
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
CONSTRUCT{
    ?p :hasDisease ?d .
} WHERE {
    {
        ?p :exhibitsSymptom ?s, ?s1, ?s2 .
        ?d :hasSymptom ?s, ?s1, ?s2 .
        FILTER(?s != ?s1 && ?s != ?s2 && ?s1 != ?s2)
    }
}
"""

q_results = query_graphdb(endpoint, q12)

g = Graph()
g.parse("med_doentes.ttl")

n = Namespace("http://www.example.org/disease-ontology#")
g.add((n.hasDisease, RDF.type, OWL.ObjectProperty))

g += q_results

g.serialize(destination="med_final.ttl", encoding='utf-8', format="turtle")