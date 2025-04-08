import json


ds_txt = ""
ds_dict = {}
dd_txt = ""
dd_dict = {}
symptoms_to_add = []
dt_txt = ""
dt_dict = {}
treatments_to_add = []

with open("Disease_Syntoms.csv", "r", encoding="utf-8") as f:
    ds_txt = f.read()

ds_txt = ds_txt.split("\n")[1:]

for l in ds_txt:
    l = l.split(",")
    l[0] = l[0].strip().replace(" ", "_").replace("(", "_").replace(")", "_").strip("_").replace("__", "_").lower()
    l[0] = l[0].title()
    if l[0] not in ds_dict.keys() and l[0] != "":
        ds_dict[l[0]] = []
    for s in l[1:]:
        s = s.strip().replace(" ", "_").replace("(", "_").replace(")", "_").strip("_").replace("__", "_").lower()
        s = s.title()
        if s not in ds_dict[l[0]] and s != "":
            ds_dict[l[0]].append(s)
            if s not in symptoms_to_add:
                symptoms_to_add.append(s)

with open("Disease_Description.csv", "r", encoding="utf-8") as f:
    dd_txt = f.read()

dd_txt = dd_txt.split("\n")[1:]

for l in dd_txt:
    l = l.split(",", 1)
    l[0] = l[0].strip().replace(" ", "_").replace("(", "_").replace(")", "_").strip("_").replace("__", "_").lower()
    l[0] = l[0].title()
    if len(l) > 1:
        if l[0] not in dd_dict.keys():
            dd_dict[l[0]] = []
        dd_dict[l[0]].append(l[1].strip().replace('"', ''))
        
with open("Disease_Treatment.csv", "r", encoding="utf-8") as f:
    dt_txt = f.read()

dt_txt = dt_txt.split("\n")[1:]

for l in dt_txt:
    l = l.split(",", 4)
    l[0] = l[0].strip().replace(" ", "_").replace("(", "_").replace(")", "_").strip("_").replace("__", "_").lower()
    l[0] = l[0].title()
    if l[0] not in dt_dict.keys() and l[0] != "":
        dt_dict[l[0]] = []
    for s in l[1:]:
        s = s.strip().replace(" ", "_").replace("(", "_").replace(")", "_").strip("_").replace("__", "_").lower()
        s = s.title()
        if s not in dt_dict[l[0]] and s != "":
            dt_dict[l[0]].append(s)
            if s not in treatments_to_add:
                treatments_to_add.append(s)

doentes_json = []
doentes_ont = ""
with open("doentes.json", "r", encoding='utf-8') as f:
    doentes_json = json.load(f)

doente_id = 1
for d in doentes_json:
    doentes_ont += f':Patient{doente_id} a :Patient '
    if "nome" in d.keys():
        doentes_ont += f';\n\t:name "{d["nome"]}" '
    if "sintomas" in d.keys():
        sintomas_added = []
        for sint in d["sintomas"]:
            sint = sint.strip().replace(" ", "_").replace("(", "_").replace(")", "_").strip("_").replace("__", "_").lower()
            sint = sint.title()
            if (sint not in sintomas_added) and (sint in symptoms_to_add):
                sintomas_added.append(sint)
                doentes_ont += f';\n\t:exhibitsSymptom :{sint} '
    doentes_ont += '.\n\n'
    doente_id += 1

                
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

:name a owl:DatatypeProperty ;
                     rdfs:domain :Patient ;
                     rdfs:range xsd:string .

#Disease instances
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
    
    if dt_dict.get(k) != None:
        treats = dt_dict[k]
        if treats != []:
            ont_txt += ';\n\t:hasTreatment '
            for i in range(0, len(treats)):
                if i == 0:
                    ont_txt += f''':{treats[i]} '''
                else:
                    ont_txt += f''', :{treats[i]} '''
                    
    ont_txt += '.\n\n'

ont_txt += '#Symptoms instances\n'
for sym in symptoms_to_add:
    ont_txt += f":{sym} a :Symptom .\n"
ont_txt += '\n#Treatments instances\n'
for treat in treatments_to_add:
    ont_txt += f":{treat} a :Treatment .\n"
ont_txt += '\n#Patient instances\n' + doentes_ont

with open("med_doentes.ttl", "w", encoding='utf-8') as f:
    f.write(ont_txt)
        
