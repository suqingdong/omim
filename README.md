# OMIM - Online Mendelian Inheritance in Man


## Installation
```bash
pip3 install omim
```

## Basic Usage
### main
`omim -h`
```
Usage: omim [OPTIONS] COMMAND [ARGS]...

  OMIM - Online Mendelian Inheritance in Man

Options:
  -d, --dbfile TEXT  the path of database file  [default:/usr/local/lib/python3.8/site-packages/omim/data/omim.sqlite3]
  -u, --url TEXT     the url of omim  [default: https://mirror.omim.org]
  --version          Show the version and exit.
  -?, -h, --help     Show this message and exit.

Commands:
  faq     explains of some faq
  query   query something from the database
  stats   statistics of the database
  update  update the database
```

### stats
> OMIM Entry Statistics

`omim stats`
```
***** updated time: 2021-04-20 *****
+--------------------------+-------+
| MIM_TYPE                 | COUNT |
+--------------------------+-------+
| gene                     | 16458 |
| gene/phenotype           | 27    |
| phenotype                | 7578  |
| predominantly phenotypes | 1762  |
| moved/removed            | 1317  |
| TOTAL COUNT              | 27142 |
+--------------------------+-------+
```

### update
> update the database according to the file mim2gene.txt

```
omim update
```

### faq
> explains of some FAQ

`omim faq`
```
***** Explains of MIM PREFIX *****
+--------+---------------------------------------------------------+
| PREFIX | EXPLAIN                                                 |
+--------+---------------------------------------------------------+
|   *    | Gene description                                        |
|   +    | Gene and phenotype, combined                            |
|   #    | Phenotype description, molecular basis known            |
|   %    | Phenotype description or locus, molecular basis unknown |
|        | Other, mainly phenotypes with suspected mendelian basis |
|   ^    | Moved/Removed                                           |
+--------+---------------------------------------------------------+
***** Explains of PHENOTYPE SYMBOL *****
+--------+------------------------------------------------------------------------------------------------------------------------------+
| SYMBOL | EXPLAIN                                                                                                                      |
+--------+------------------------------------------------------------------------------------------------------------------------------+
|  [ ]   | indicate "nondiseases," mainly genetic variations that lead to apparently abnormal laboratory test values                    |
|  { }   | indicate mutations that contribute to susceptibility to multifactorial disorders                                             |
|        | (e.g., diabetes, asthma) or to susceptibility to infection                                                                   |
|   ?    | before the phenotype name indicates that the relationship between the phenotype and gene is provisional.                     |
|        | More details about this relationship are provided in the comment field of the map and in the gene and phenotype OMIM entries |
|  (1)   | the disorder was positioned by mapping of the wildtype gene                                                                  |
|  (2)   | the disease phenotype itself was mapped                                                                                      |
|  (3)   | the molecular basis of the disorder is known                                                                                 |
|  (4)   | the disorder is a chromosome deletion or duplication syndrome                                                                |
+--------+------------------------------------------------------------------------------------------------------------------------------+
```

### **query**
`omim query -h`
```
Usage: omim query [OPTIONS]

  query something from database

Options:
  -K, --keys               list the available keys
  -s, --search TEXT...     the search string
  -l, --limit INTEGER      limit for output
  -F, --format [json|tsv]  the format for output
  -o, --outfile TEXT       the output filename [stdout]
  -?, -h, --help           Show this message and exit.
```

`omim query -K`
```
+------------------+-----------------------+--------------+
| Key              | Comment               | Type         |
+------------------+-----------------------+--------------+
| mim_number       | MIM Number            | VARCHAR(10)  |
| prefix           | The prefix symbol     | VARCHAR(1)   |
| title            | The title             | VARCHAR(50)  |
| references       | The references        | VARCHAR(300) |
| geneMap          | The geneMap data      | VARCHAR(300) |
| phenotypeMap     | The phenotypeMap data | VARCHAR(300) |
| mim_type         | The mim_type          | VARCHAR(20)  |
| entrez_gene_id   | The entrez_gene_id    | VARCHAR(20)  |
| ensembl_gene_id  | The ensembl_gene_id   | VARCHAR(20)  |
| hgnc_gene_symbol | The hgnc_gene_symbol  | VARCHAR(20)  |
| generated        | The generated time    | DATETIME     |
+------------------+-----------------------+--------------+
```

`omim query -s hgnc_gene_symbol BMPR2`
```
phenotypeMap	references	prefix	mim_number	generated	ensembl_gene_id	mim_type	geneMap	title	hgnc_gene_symbol	entrez_gene_id
None	16429403, 10051328, 17425602, 18548003, 10903931, 21920918, 12571257, 3291115, 12358323, 10973254, 16429395, 11115378, 14583445, 18626305, 18321866, 11484688, 18496036, 18792970, 7644468, 12045205, 12446270, 15965979, 24446489, 11015450, 19620182	*	600799	2021-04-14	ENSG00000204217	gene	[{"Location": "2q33.1-q33.2", "Phenotype": "Pulmonary hypertension, familial primary, 1, with or without HHT", "Phenotype MIM number": "178600", "Inheritance": "AD", "Phenotype mapping key": "3"}, {"Location": "2q33.1-q33.2", "Phenotype": "Pulmonary hypertension, primary, fenfluramine or dexfenfluramine-associated", "Phenotype MIM number": "178600", "Inheritance": "AD", "Phenotype mapping key": "3"}, {"Location": "2q33.1-q33.2", "Phenotype": "Pulmonary venoocclusive disease 1", "Phenotype MIM number": "265450", "Inheritance": "AD", "Phenotype mapping key": "3"}]	BONE MORPHOGENETIC PROTEIN RECEPTOR, TYPE II; BMPR2	BMPR2	659
```

`omim query -s hgnc_gene_symbol BMPR2 -F json`
```json
[
  {
    "phenotypeMap": null,
    "references": "16429403, 10051328, 17425602, 18548003, 10903931, 21920918, 12571257, 3291115, 12358323, 10973254, 16429395, 11115378, 14583445, 18626305, 18321866, 11484688, 18496036, 18792970, 7644468, 12045205, 12446270, 15965979, 24446489, 11015450, 19620182",
    "prefix": "*",
    "mim_number": "600799",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000204217",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "2q33.1-q33.2",
        "Phenotype": "Pulmonary hypertension, familial primary, 1, with or without HHT",
        "Phenotype MIM number": "178600",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "2q33.1-q33.2",
        "Phenotype": "Pulmonary hypertension, primary, fenfluramine or dexfenfluramine-associated",
        "Phenotype MIM number": "178600",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "2q33.1-q33.2",
        "Phenotype": "Pulmonary venoocclusive disease 1",
        "Phenotype MIM number": "265450",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "BONE MORPHOGENETIC PROTEIN RECEPTOR, TYPE II; BMPR2",
    "hgnc_gene_symbol": "BMPR2",
    "entrez_gene_id": "659"
  }
]
```

`omim query -s geneMap '%Pulmonary hypertension%' -F json`
```json
[
  {
    "phenotypeMap": null,
    "references": "16429403, 10051328, 17425602, 18548003, 10903931, 21920918, 12571257, 3291115, 12358323, 10973254, 16429395, 11115378, 14583445, 18626305, 18321866, 11484688, 18496036, 18792970, 7644468, 12045205, 12446270, 15965979, 24446489, 11015450, 19620182",
    "prefix": "*",
    "mim_number": "600799",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000204217",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "2q33.1-q33.2",
        "Phenotype": "Pulmonary hypertension, familial primary, 1, with or without HHT",
        "Phenotype MIM number": "178600",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "2q33.1-q33.2",
        "Phenotype": "Pulmonary hypertension, primary, fenfluramine or dexfenfluramine-associated",
        "Phenotype MIM number": "178600",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "2q33.1-q33.2",
        "Phenotype": "Pulmonary venoocclusive disease 1",
        "Phenotype MIM number": "265450",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "BONE MORPHOGENETIC PROTEIN RECEPTOR, TYPE II; BMPR2",
    "hgnc_gene_symbol": "BMPR2",
    "entrez_gene_id": "659"
  },
  {
    "phenotypeMap": null,
    "references": "22474227, 18237401, 11498544, 9837809, 9662443, 9801158, 16973879, 10079111, 25898808, 29562231, 2541345, 1360410, 15539149, 18211975, 16051704, 1512286, 22328087, 10988071, 15353589, 16001074, 11739396, 11457855, 8552590, 7608210, 26176221, 21610094, 11358800, 21654750, 17178917, 9741627, 16890161, 9717814, 16670769, 12177436, 19487814",
    "prefix": "*",
    "mim_number": "601047",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000105974",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "7q31.2",
        "Phenotype": "?Lipodystrophy, congenital generalized, type 3",
        "Phenotype MIM number": "612526",
        "Inheritance": "AR",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "7q31.2",
        "Phenotype": "Lipodystrophy, familial partial, type 7",
        "Phenotype MIM number": "606721",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "7q31.2",
        "Phenotype": "Pulmonary hypertension, primary, 3",
        "Phenotype MIM number": "615343",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "CAVEOLIN 1; CAV1",
    "hgnc_gene_symbol": "CAV1",
    "entrez_gene_id": "857"
  },
  {
    "phenotypeMap": null,
    "references": "18250325, 9312005, 12198146, 11749039, 9721223, 23883380, 10575216, 16574908, 32499642",
    "prefix": "*",
    "mim_number": "603220",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000171303",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "2p23.3",
        "Phenotype": "Pulmonary hypertension, primary, 4",
        "Phenotype MIM number": "615344",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "POTASSIUM CHANNEL, SUBFAMILY K, MEMBER 3; KCNK3",
    "hgnc_gene_symbol": "KCNK3",
    "entrez_gene_id": "3777"
  },
  {
    "phenotypeMap": null,
    "references": "9371779, 18548003, 21920918, 19419974, 21898662, 26122142, 10583507, 24076600, 19211612, 9205116",
    "prefix": "*",
    "mim_number": "603295",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000120693",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "13q13.3",
        "Phenotype": "Pulmonary hypertension, primary, 2",
        "Phenotype MIM number": "615342",
        "Inheritance": "AD",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "SMAD FAMILY MEMBER 9; SMAD9",
    "hgnc_gene_symbol": "SMAD9",
    "entrez_gene_id": "4093"
  },
  {
    "phenotypeMap": null,
    "references": "6208196, 11474210, 18063578, 2991113, 9711878, 12655559, 21120950, 1840546, 9107685, 8486760, 7590739, 25410056, 3545062, 29801986, 28538732, 19793055, 17310273, 20154341, 16708072, 30842655, 206435, 2991241, 11407344, 6249820, 15465784, 8382576, 21767969, 7587391, 14718356, 12853138, 4944634",
    "prefix": "*",
    "mim_number": "608307",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000021826",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "2q34",
        "Phenotype": "{Pulmonary hypertension, neonatal, susceptibility to}",
        "Phenotype MIM number": "615371",
        "Inheritance": "",
        "Phenotype mapping key": "3"
      },
      {
        "Location": "2q34",
        "Phenotype": "Carbamoylphosphate synthetase I deficiency",
        "Phenotype MIM number": "237300",
        "Inheritance": "AR",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "CARBAMOYL PHOSPHATE SYNTHETASE I; CPS1",
    "hgnc_gene_symbol": "CPS1",
    "entrez_gene_id": "1373"
  },
  {
    "phenotypeMap": null,
    "references": "21255763, 15779907, 16163389, 24034276",
    "prefix": "*",
    "mim_number": "612804",
    "generated": "2021-04-14",
    "ensembl_gene_id": "ENSG00000104835",
    "mim_type": "gene",
    "geneMap": [
      {
        "Location": "19q13.2",
        "Phenotype": "Hyperuricemia, pulmonary hypertension, renal failure, and alkalosis",
        "Phenotype MIM number": "613845",
        "Inheritance": "AR",
        "Phenotype mapping key": "3"
      }
    ],
    "title": "SERYL-tRNA SYNTHETASE 2; SARS2",
    "hgnc_gene_symbol": "SARS2",
    "entrez_gene_id": "54938"
  },
  {
    "phenotypeMap": null,
    "references": "19165231",
    "prefix": "%",
    "mim_number": "612862",
    "generated": "2021-04-15",
    "ensembl_gene_id": "",
    "mim_type": "phenotype",
    "geneMap": [
      {
        "Location": "6p21.3",
        "Phenotype": "{Pulmonary hypertension, chronic thromboembolic, without deep vein thrombosis, susceptibility to}",
        "Phenotype MIM number": "612862",
        "Inheritance": "",
        "Phenotype mapping key": "2"
      }
    ],
    "title": "PULMONARY HYPERTENSION, CHRONIC THROMBOEMBOLIC, WITHOUT DEEP VEIN THROMBOSIS, SUSCEPTIBILITY TO",
    "hgnc_gene_symbol": "",
    "entrez_gene_id": "100302516"
  }
]
```

## Use omim in Python
```python
import omim
from omim import util
from omim.db import Manager, OMIM_DATA


manager = Manager(dbfile=omim.DEFAULT_DB)

# show columns
print(util.get_columns_table())


# show stats
generated, table = util.get_stats_table(manager)
print(generated)
print(table)

# count the database
manager.query(OMIM_DATA).count()

# query with key-value
res = manager.query(OMIM_DATA, 'prefix', '*')
res = manager.query(OMIM_DATA, 'mim_number', '600799')
res = manager.query(OMIM_DATA, 'hgnc_gene_symbol', 'BMPR2')
res = manager.query(OMIM_DATA, 'geneMap', '%Pulmonary hypertension%')  # fuzzy query

# fetch query result
item = res.first()
items = res.all()

# content of result
print(item.mim_number, item.title)
print(item.as_dict)
```
