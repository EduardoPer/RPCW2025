# TPC5: Preenchimento de uma ontologia com dados de cinema

## Dataset(s)
Tirados de: <https://developer.imdb.com/non-commercial-datasets/>

Utilizados:
- title.basics.tsv.gz
- title.akas.tsv.gz
- title.principals.tsv.gz
- name.basics.tsv.gz

## Filtrar os ficheiros tsv
```bash
python3 tpc5_filter_datasets.py
```

## Criar uma ontologia com os dados
```bash
python3 tpc5_filter_datasets.py <nMovies>
```