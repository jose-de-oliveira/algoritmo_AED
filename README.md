<p align="center">
  <img src="https://github.com/jose-de-oliveira/algoritmo_AED/blob/main/c51024d6-1c25-46f5-8c03-b901a18c529e.png" width=30%>
</p>

# Algoritmo para análise exploratória de dados

### Análise Exploratória de Dados

Visto como um dos ramos primordiais da ciência estatística, a análise exploratória de dados é responsável a conceder os primeiros insights em relação a base de dados, possibilitando um delineamento da qualidade dos dados e do perfil atual de cada informação. Mapear índices, medidas resumo e quantificadores de cada base é primordial para a tomada de decisão de um modelo estatístico ou até mesmo de etapas antecessoras de limpeza e transformação de variáveis. 

### O que o Algoritmo faz?

O Algoritmo aqui terá papel inicial de determinar que tipo de variável está sendo utilizada e assim determinar quais medidas serão feitas. Mas antes disso, precisamos de alguns preparativos, no mundo real as variáveis não vem tão dicotomizadas assim. Em minha experiência com o mundo corporativo, conversando com a área de entrada dos dados é possível mapear sinais e indícios das características dos dados. O Algoritmo foi uma ferramenta que criei para acelerar o processo matemático de investigação e análise de dados, o que não substitui uma análise profissional dos dados coletados. 

Você pode encontrar o algoritmo [aqui](https://github.com/jose-de-oliveira/algoritmo_AED/blob/main/dataquality%201.4.py)

### O que você precisa saber antes de utilizar esse código

Os limites definidos como bounds para as análises podem E DEVEM ser adaptados para uma carga de base de acordo com a natureza de dados, o objetivo é fornecer um algoritmo, isto é, uma forma automatizada de executar passos e não um modelo. Considerar uma variável com 95% de completude ou qualquer outro valor tende a considerar o viés que suas interpretações podem conter. O Algoritmo é uma ferramenta e não uma inteligência por si só! Para rodar utilizando python, certifique-se de atualizar os programas e bibliotecas necessários.

### Etapas Pré-Análise

Antes de mais nada, vamos nos concentrar em detectar o tipo de variável utilizada. O Algoritmo cobre e realiza diferentes métricas em variáveis Qualitativas, Quantitativas e Temporais.

```python
# Verify if the variable is qualitative
def is_qualitative(column):
    return column.dtype == 'object'

# Verify if the variable is time-based (recently the format datetime64[ns] has changed to datetime64[ns])
# must be checked
def is_timebased(column):
    return column.dtype == 'datetime64[ns]'

# Verify if the variable is quantitative and not a datetime variable
def is_quantitative(column):
    if column.dtype != 'datetime64[ns]':
        return np.issubdtype(column.dtype, np.number) 
```

Esses parênteses ao lado de *datetime64* indicam a precisão que os dados estão colocados, aqui a precisão está indo até nanosegundos (ns) já que os dados que trabalhei tem o formato *'2024-02-01 00:00:00.000'*.

#### A Lógica pela função check_input()

A função *check_input()* realiza comparativos de acordo com o nome da variável passada e um dicionário pré-estabelecido (sim, aqui estamos falando do dataframe input_dados), basicamente associamos a esse dicionário um nome de variável, um tipo e caso faça sentido, um limite inferior. A seguir, passando por cada variável do data frame alvo, analisamos o quão próximas são um determinado nome de uma variável do dicionário em relação à variável alvo.

```python
input_dados = {
    'Nome da Variável': [
        'patrimônio contábil','data','numero de investidores','cnpj'
    ],

    'Tipo da Variável': [
        'float64', 'datetime64[ns]', 'int64', 'object'
    ],
    'Bound': [
        0.0, '1900-01-01 00:00:00.000', 0, None
    ],
}
```

Como isso é feito? Aguarde que logo logo eu irei explicar sobre o algoritmo utilizado para realização deste passo.

Dessa forma, podemos ter uma coluna que avalia a viabilidade de cada informação obtida. 

#### Variáveis Proibidas

Algumas variáveis não fazem sentido de serem extremamente dissecadas. Por exemplo, uma moda numa variável de nome social não agrega muita informação. 

```python
# Forbidden variables are variables that must be checked but does not contribute for the dataset evaluation
# or can be used in further analysis
Forbidden_variables = ['nome','fantasia','cnpj','razao']

# By doing so, eligible variables are those ones which are not forbidden =)
eligible_variables = [coluna for coluna in df.columns if not any(palavra in coluna for palavra in Forbidden_variables)]
```

Com o uso de palavras chave, variáveis com esse perfil podem ser excluídas da análise, criando o grupo de variáveis proibidas (Forbidden Variables). Variáveis elegíveis (Eligible Variables) seguem as análises abaixo conforme o tipo.

### Tratativas de Carga de Dados

Nesse ponto, analisamos a completude de cada variável, considerando uma variável com 5% de nulos, um indicador suspeito. Analisa-se também a quantidade de fatores que mostram a quantidade de observações distintas na coluna da variável. Este passo é executado em todas as variáveis do dataset.

### Tratativas de Variáveis Quantitativas

Para variáveis quantitativas, que indicam **quanti**dade ou que "contam" alguma coisa, executam-se algumas medidas resumo como, média, mediana, mínimo, máximo, desvio-padrão, coeficiente de variação e coeficiente de assimetria. Algumas variáveis no mundo real podem medir valores aberrantes de assimetria devido a características atípicas, porém inerentes ao contexto em que estão inseridas. Para isso, utilizamos a distância entre a mediana e o mínimo e a distância entre a mediana e o máximo para descrever tambem sobre a assimetria da variavel alvo. Alterações nessas medidas em múltiplas execuções da base podem alertar melhor sobre o perfil da distribuição dos dados. Além disso, conta-se a quantidade de observações fora do túnel de média e 3 desvios padrões para cima e para baixo.

### Tratativas de Variáveis Qualitativas

Para variáveis qualitativas, que indicam **quali**dade ou que "qualificam" alguma coisa, executam-se algumas medidas como moda e frequência modal. Pensando em uma forma de mostrar a homogeneidade dessas variáveis, eu criei um *coeficiente de homogeneidade*. A ideia é transformar a carga de frequências de cada fator num conjunto de números e a partir deste realizar o seu coeficiente de variação, em uma base que possuam frequências próximas, o coeficiente é próximo de zero e quanto mais aberrante for a frequência de algum fator, maior o coeficiente de homogeneidade, indicando alta heterogeneidade.

### Tratativas de Variáveis Temporais

Para variáveis que correspondem a datas, um coeficiente de homogeneidade de datas foi criado de maneira análoga ao coeficiente de homogeneidade para variáveis qualitativas.

### Nota e avaliação do dataset

As colunas contendo o nome Avaliação, fazem uma classificação entre aa saidas *ok* e *verificar*. Pela quantidade de fatores avaliados como *ok*, uma nota ponderada classifica o estado da base. 

```python
# Based on the generated features, compute the final metric.
# Here the dataset will receive a value, a percentage of quality.
valid_counts = output_df[output_df.columns[output_df.columns.str.contains('Avaliação')]].apply(lambda x: x.value_counts().get('Ok', 0))
total_counts = valid_counts + output_df[output_df.columns[output_df.columns.str.contains('Avaliação')]].apply(lambda x: x.value_counts().get('Verificar', 0))
num_factor = sum(~np.isnan(valid_counts/total_counts))
nota_final = np.nansum((1/num_factor)*(valid_counts/total_counts))
```

Convém lembrar que a nota é intrínseca aos valores colocados como pontos de corte dos indicadores citados acima. Variáveis proibidas não contribuem para nota da base.

### Saídas

A primeira saída é um dataset de avaliação de cada variável, basicamente um boletim. Assim, é possível ver de maneira generalizada o estado de cada indicador.

```python
# Show the Final Dataset:
print("DataFrame de Saída:")
print(output_df)
```

A segunda saída é uma base de valores duplicados, aqui um valor repetido é simplesmente uma réplica perfeita de quaisquer linha de todo um dataset.

```python
# Show Duplicates
duplicates_df = df[df.duplicated(keep=False)]
print("\nDataFrame de Linhas Duplicadas:")
print(duplicates_df)
print(f"\nDimensão do DataFrame de Linhas Duplicadas: {duplicates_df.shape[0]} linhas x {duplicates_df.shape[1]} colunas")
```

A terceira saída é uma base que aponta os outliers com uma coluna motivo, descrevendo em que variável aquela linha apresentou informação aberrante, bem como os limites utilizados para tal avaliação. 

```python
# Show Outliers
list_outliers_df = list_outliers
print("\Data Frame de Valores aberrantes")
print(list_outliers_df)
```

### Adaptação ao Dataiku

Caso haja necessidade, é possível plugar o core do código em uma fórmula de *python* do Dataiku. Alterações podem ser necessárias para adequar a versão instalada com o código. O pacote *textdistance* precisa estar instalado para que o código funcione corretamente. As bases de saídas devem ser criadas na criação da receita.
