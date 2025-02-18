<p align="center">
<strong>
Pacote para transformação de vazão em ENA de acordo com as regras de negócio do ONS.
</strong>
</p>
<p align="center">
<a href="https://pypi.org/project/ena-ons/0.0.0/" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/missil.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

## Instalação

```bash
pip install ena-ons
```

## Por que usar?
Transformar vazão em Energia Natural Afluente (ENA) é uma tarefa comum em estudos de planejamento energético. O cálculo da ENA é feito de acordo com as regras de negócio do Operador Nacional do Sistema (ONS). Este pacote visa facilitar a transformação de vazão em ENA, seguindo as regras de negócio do ONS.

Vale ressaltar também que nesse pacote existem as regras de negócio para criação de todas
as vazões artificiais do sistema. A adição dessas vazões deve ser feita para que os cálculos
sejam feitos em conformidade com o ONS, sendo possível a comparação dos resultados obtidos pelo
próprio operador.

## Utilização
Este pacote foi desenvolvido em cima de uma única classe principal, que recebe como parâmetros
de inicialização um dataframe contendo as vazões e outro contendo as produtibilidades.

Exemplos de todas os dataframes utilizados estão disponíveis na pasta `data`.

Há 3 métodos principais na classe `VazaoENA`:
- `adicionar_vazoes_artificiais`: Adiciona as vazões artificiais ao dataframe de vazões.
- `calcular_ena`: Calcula a ENA de acordo com as regras de negócio do ONS.
- `agrupar`: Soma a ENA a partir de um agrupamento passado como parâmetro.

### Vazões
Dataframe passado na inicialização da classe. Deve conter um índice do tipo datetime e 
as colunas com os códigos dos postos. As vazões serão os valores das células.

Exemplo:
| data | 1 | 3 |
|------|---|---|
| 2025-01-01 | 100 | 200 |
| 2025-01-02 | 150 | 250 |
| 2025-01-03 | 200 | 300 |

### Produtibilidades
Dataframe passado na inicialização da classe. Deve conter uma coluna `codigo` contendo os códigos dos postos e uma coluna `produtibilidade` contendo os valores das produtibilidades.

Exemplo:
| codigo | produtibilidade |
|--------|-----------------|
| 1 | 0.9 |
| 3 | 0.15 |

### Hidrograma
Dataframe utilizado no método `adicionar_vazoes_artificiais`. Deve conter coluna `mes`
com os meses do ano e `vazao` com os valores do hidrograma de Belo Monte que deseja utilizar.

Exemplo:
| mes | vazao |
|-----|-------|
| 1 | 1100 |
| 2 | 1600 |
| 3 | 2000 |


### Agrupamento
Dataframe utilizado no método `agrupar`. Deve conter uma coluna `codigo` com os códigos dos postos e uma coluna (que não precisa de nome definido) com os valores do grupo de cada posto.

Exemplo:
| codigo | subsistema |
|--------|------------|
| 1 | seco |
| 3 | n |
| 4 | s |


### Exemplo de uso
```python
import pandas as pd

from ena_ons import VazaoENA

vazao = pd.read_csv("data/vazao.csv", index_col="data", parse_dates=True)
vazao.columns = vazao.columns.astype(float)

produtibilidade = pd.read_csv("data/produtibilidade.csv")

ena = VazaoENA(vazao, produtibilidade)

hidrograma = pd.read_csv("data/hidrograma.csv")

vazoes_com_artificiais = ena.adicionar_vazoes_artificiais(hidrograma)
df_ena = ena.calcular_ena(vazoes_com_artificiais)

agrupamentos = pd.read_csv("data/agrupamento.csv")
subsistema = agrupamentos.loc[:, ["codigo", "subsistema"]]

df_ena_agrupado = ena.agrupar(df_ena, subsistema)
```

## Licença
Este projeto está licenciado sob a licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.