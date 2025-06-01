# EX1

## Queries:
(feitas sobre __historia.ttl__)
```bash
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s a owl:Class .
}
```

```bash
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s a owl:ObjectProperty .
}
```

```bash
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s a owl:NamedIndividual .
}
```

```bash
PREFIX : <http://www.rpcw.di.uminho.pt/2025/historia#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s :fazProduto :Tomates .
}
```

```bash
PREFIX : <http://www.rpcw.di.uminho.pt/2025/historia#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s :contrataTemporários true .
}
```


# EX2.11
```bash
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select (COUNT (?s) as ?c) where {
    ?s a :Disease .
}
```

```bash
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?s WHERE {
    ?s a :Disease ;
       :hasSymptom :Yellowish_Skin .
}
```

```bash
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?s WHERE {
    ?s a :Disease ;
       :hasTreatment :Exercise .
}
```

```bash
PREFIX : <http://www.example.org/disease-ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT ?s ?n WHERE {
    ?s a :Patient ;
       :name ?n;
} ORDER BY ?n
```

## EX2.13
```bash
PREFIX : <http://www.example.org/disease-ontology#>
SELECT ?d (COUNT(?p) as ?np) WHERE {
    ?p :hasDisease ?d .
} GROUP BY ?d
```

## EX2.14
```bash
PREFIX : <http://www.example.org/disease-ontology#>
SELECT ?s (COUNT(?d) as ?nd) WHERE {
    ?d :hasSymptom ?s .
} GROUP BY ?s
```

## EX2.15
```bash
PREFIX : <http://www.example.org/disease-ontology#>
SELECT ?t (COUNT(?d) as ?nd) WHERE {
    ?d :hasTreatment ?t .
} GROUP BY ?t
```