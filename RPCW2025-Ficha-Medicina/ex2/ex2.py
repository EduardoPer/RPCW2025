import json
import pandas
import re


ds_txt = ""
ds_dict = {}
dd_txt = ""
dd_dict = {}
symptoms_to_add = []

with open("Disease_Syntoms.csv", "r", encoding="utf-8") as f:
    ds_txt = f.read()

ds_txt = ds_txt.split("\n")[1:]

for l in ds_txt:
    l = l.split(",")
    l[0] = l[0].strip().replace(" ", "_").replace("(", "_").replace(")", "_")
    if l[0] not in ds_dict.keys() and l[0] != "":
        ds_dict[l[0]] = []
    for s in l[1:]:
        s = s.strip().replace(" ", "_").replace("(", "_").replace(")", "_")
        if s not in ds_dict[l[0]] and s != "":
            ds_dict[l[0]].append(s)
            s = f":{s} a :Symptom ."
            if s not in symptoms_to_add:
                symptoms_to_add.append(s)

with open("Disease_Description.csv", "r", encoding="utf-8") as f:
    dd_txt = f.read()

dd_txt = dd_txt.split("\n")[1:]

for l in dd_txt:
    l = l.split(",", 1)
    if len(l) > 1:
        if l[0] not in dd_dict.keys():
            dd_dict[l[0]] = []
        dd_dict[l[0]].append(l[1].strip().replace('"', ''))
                
ont_txt = '''@prefix : <http://www.example.org/disease-ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix swrl: <http://www.w3.org/2003/11/swrl#> .
@prefix swrlb: <http://www.w3.org/2003/11/swrlb#> .

<http://www.example.org/disease-ontology> rdf:type owl:Ontology .

# Classes
:Disease a owl:Class .
:Symptom a owl:Class .
:Treatment a owl:Class .
:Patient a owl:Class .

# Properties
:hasSymptom a owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Symptom .

:hasTreatment a owl:ObjectProperty ;
    rdfs:domain :Disease ;
    rdfs:range :Treatment .

:exhibitsSymptom a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Symptom .

:hasDisease a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Disease .

:receivesTreatment a owl:ObjectProperty ;
    rdfs:domain :Patient ;
    rdfs:range :Treatment .

:hasDescription a owl:DatatypeProperty ;
                     rdfs:domain :Disease ;
                     rdfs:range xsd:string .

'''

for k,v in ds_dict.items():
    ont_txt += f''':{k} a :Disease '''
    if v != []:
        ont_txt += ';\n\t:hasSymptom '
        for i in range(0, len(v)):
            if i == 0:
                ont_txt += f''':{v[i]} '''
            else:
                ont_txt += f''', :{v[i]} '''
                
    if dd_dict.get(k) != None:
        descs = dd_dict[k]
        if descs != []:
            ont_txt += ';\n\t:hasDescription '
            for i in range(0, len(descs)):
                if i == 0:
                    ont_txt += f'''"{descs[i]}" '''
                else:
                    ont_txt += f''', "{descs[i]}" '''
    ont_txt += '.\n\n'
    
for sym in symptoms_to_add:
    ont_txt += sym + "\n"
    
with open("med_doencas.ttl", "w", encoding='utf-8') as f:
    f.write(ont_txt)
        
