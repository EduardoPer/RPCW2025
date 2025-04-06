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