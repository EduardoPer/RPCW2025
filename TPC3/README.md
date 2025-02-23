# TPC2/3: Queries SPARQL em ontologia sobre história de Portugal

## Enunciado e Respostas
### Descarregar o [dataset sobre a História de Portugal](https://epl.di.uminho.pt/~jcr/AULAS/RPCW2025/semana3/HistPT.rdf) e sobre ele responder às seguintes questões:
- a. Quantos triplos existem na Ontologia?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select (count (*) as ?c) {
    ?s ?p ?o .
}
```
- b. Que classes estão definidas?
```
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s rdf:type owl:Class .
}
```
- c. Que propriedades tem a classe "Rei"?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX : <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
select distinct ?prop where {
    ?s a historia:Rei .
    ?s ?prop ?o .
}
```
- d. Quantos reis aparecem na ontologia?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select (count (*) as ?c) {
    ?s rdf:type historia:Rei .
}
```
- e. Calcula uma tabela com o seu nome, data de nascimento e cognome.
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s rdf:type historia:Rei .
    ?s historia:nome ?o .
    ?s historia:nascimento ?n .
    ?s historia:cognomes ?cn .
}
```
- f. Acrescenta à tabela anterior a dinastia em que cada rei reinou.
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select * where {
    ?s rdf:type historia:Rei .
    ?s historia:nome ?o .
    ?s historia:nascimento ?n .
    ?s historia:cognomes ?cn .
    ?s historia:temReinado ?r .
    ?r historia:dinastia ?d .
}
```
- g. Qual a distribuição de reis pelas 4 dinastias?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select (count (?s) as ?c) ?d where {
    ?s rdf:type historia:Rei .
    ?s historia:temReinado ?r .
    ?r historia:dinastia ?d .
}group by ?d
```
- h. Lista os descobrimentos (sua descrição) por ordem cronológica.
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?n where {
    ?s rdf:type historia:Descobrimento .
    ?s historia:notas ?n .
    ?s historia:data ?d .
} order by ?d
```
- i. Lista as várias conquistas, nome e data, juntamento com o nome que reinava no momento.
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?nomeConquista ?dataConquista ?nomeRei where {
    ?s rdf:type historia:Conquista .
    ?s historia:nome ?nomeConquista .
    ?s historia:data ?dataConquista .
    ?s historia:temReinado $r .
    ?r historia:temMonarca ?rei .
    ?rei historia:nome ?nomeRei .
}
```
- j. Calcula uma tabela com o nome, data de nascimento e número de mandatos de todos os presidentes portugueses.
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?nomePresidente ?dataNascimento (count (?mandato) as ?mandatos) where {
    ?s rdf:type historia:Presidente .
    ?s historia:nome ?nomePresidente .
    ?s historia:nascimento ?dataNascimento .
    ?s historia:mandato ?mandato .
} 
group by ?nomePresidente ?dataNascimento
```
- k. Quantos mandatos teve o presidente Sidónio Pais? Em que datas iniciaram e terminaram esses mandatos?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select (count (?mandato) as ?mandatos) ?mandato ?dataInicio ?dataFim where {
    ?s rdf:type historia:Presidente .
    ?s historia:nome "Sidónio Bernardino Cardoso da Silva Pais" .
    ?s historia:mandato ?mandato .
    ?mandato historia:comeco ?dataInicio .
    ?mandato historia:fim ?dataFim .
}
group by ?dataInicio ?dataFim ?mandato
```
- l. Quais os nomes dos partidos políticos presentes na ontologia?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?nomePartido where {
    ?s rdf:type historia:Partido .
    ?s historia:nome ?nomePartido .
}
```
- m. Qual a distribuição dos militantes por cada partido político?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?nomePartido (count (?militante) as ?nMilitantes) where {
    ?s rdf:type historia:Partido .
    ?s historia:nome ?nomePartido .
    ?s historia:temMilitante ?militante .
}group by ?nomePartido
```
- n. Qual o partido com maior número de presidentes militantes?
```
PREFIX historia: <http://www.semanticweb.org/andre/ontologies/2015/6/historia#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
select ?nomePartido (count (?militante) as ?nMilitantes) where {
    ?s rdf:type historia:Partido .
    ?s historia:nome ?nomePartido .
    ?s historia:temMilitante ?militante .
}group by ?nomePartido limit 1
```