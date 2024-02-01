# Algoritmo para análise exploratória de dados

### Análise Exploratória de Dados

Visto como um dos ramos primordiais da ciência estatística, a análise exploratória de dados é responsável a conceder os primeiros insights em relação a base de dados, possibilitando um delineamento da qualidade dos dados e do perfil atual de cada informação. Mapear índices, medidas resumo e quantificadores de cada base é primordial para a tomada de decisão de um modelo estatístico ou até mesmo de etapas antecessoras de limpeza e transformação de variáveis. O Algoritmo aqui terá papel inicial de determinar que tipo de variável está sendo utilizada e assim determinar quais medidas serão feitas. Mas antes disso, precisamos de alguns preparativos, no mundo real as variáveis não vem tão dicotomizadas assim. Em minha experiência com o mundo coorporativo, conversar com a área de entrada dos dados é possível mapear sinais e indícios das características dos dados.

### O que você precisa saber antes de utilizar esse código

Os limites inferiores


### Etapas Pré-Análise

Antes de mais nada vamos nos concentrar em detectar o tipo de variável utilizada. O Algoritmo cobre e realiza diferentes métricas em variáveis Qualitativas, Quantitativas e Temporais.

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

#### A Lógica pela função check_input()

A função check_input() realiza comparativos de acordo com o nome da variável passada e um dicionário pré-estabelecido (sim, aqui estamos falando do datafreme input_dados), basicamente associamos a esse dicionário um nome de variável, um tipo e caso haja sentido, um limite inferior. A seguir, passando por cada variável do dataframe alvo, vamos vendo o quão proximas são um determinado nome de uma variável do dicionário, da variável alvo.

Como isso é feito? Aguerde que logo logo eu irei explicar sobre o algoritmo utilizado para realização deste passo.

Disso podemos ter uma coluna que pre-avalia a viabilidade de cada informação obtida. 

### Tratativas de Variáveis Quantitativas

Para variáveis quantitativas
