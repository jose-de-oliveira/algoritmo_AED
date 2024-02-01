#############################################################################################################################################
#############################################################################################################################################
#                                                Implementação do Algoritmo de Análise Exploratória de Dados
#                                                                 Revisor: José de Oliveira
#############################################################################################################################################
#############################################################################################################################################

# Importing packages for the main code, in dataiku enviroment, the package textdistance must be installed
import pandas as pd
import numpy as np
import textdistance

# Load the dataset (Change the text between '' to the desired filepath, tha dataset must be in xlsx)
# In the dataiku implementation the code must set to the same object (df) to ensure execution
df =  pd.read_excel('minha_base_exemplo.xlsx')

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

# This function check the input rule for any variable by comparsions between a preseted dictionary
# the comparsion is done by using the jaro_winkler distance and measuring a similarity between the
# candidate variable and the dictionary.
def check_input(candidate, rules, test_variable):
    max_val = 0
    final_name = None
    for row, column in rules.iterrows():
        cand_data = rules.iloc[row]
        cand_name = cand_data['Nome da Variável']
        dist = textdistance.jaro_winkler(cand_name, candidate)
        if dist > max_val:
            max_val = dist
            final_name = cand_data['Nome da Variável']

    comparsion = rules[rules['Nome da Variável'] == final_name]
    comparsion_bound = comparsion['Bound'].values[0]
    comparsion_type = comparsion['Tipo da Variável'].values[0]

    # At this point the similarity has been done and the informations are combined
    # The output is a string that explains the state of the variable
    if is_quantitative(test_variable) or is_timebased(test_variable):
        if test_variable.dtype == comparsion_type and (test_variable >= comparsion_bound).any():
            motivo_forb = "Ok" 
        if test_variable.dtype != comparsion_type:
            motivo_forb = "A variável não está no formato correto" 
        if test_variable.dtype == comparsion_type and (test_variable < comparsion_bound).any():
            motivo_forb = "Alguma observação foi preenchida de maneira incorreta"         
    else:        
        if test_variable.dtype != comparsion_type:
            motivo_forb = "A variável não está no formato correto" 
        else:
            motivo_forb = "Ok" 
    return motivo_forb

# The dictionary is composed by three informations: The name of the variable, The type of the variable
# and, if makes sense, an lowerbound for the information. as for example id is int64 and has no bound.
# This list can be expanded to increase the accuracy of the algorithm in detection of data types.

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


input_rule = pd.DataFrame(input_dados)

# Initializing the output dataset (of measurements)
output_df = pd.DataFrame(columns=[
    'Nome da variável', 'Tipo da variável', 'Checagem de Entrada','Classificação', 'Qtd de Nulos', 'Completude',
     'Avaliação de Nulos', 'Mediana', 'Mínimo', 'Distância Med-Inf', 'Média' ,'Máximo', 'Distância Med-Sup', 'Desvio Padrão', 
     'Valores distintos', 'Coeficiente de Homogeneidade','Avaliação do CH', 'Moda', 'Frequência Modal', 'Avaliação de Frequências',
      'Filtro de Desvios', 'Avaliação de Filtro', 'Coeficiente de Variação', 'Coeficiente de Assimetria', 'Avaliação do CA',
      'Coef de Homogeneidade de Datas', 'Avaliação de Datas'
])

# Forbidden variables are variables that must be checked but does not contribute for the dataset evaluation
# or can be used in futher analysis
Forbidden_variables = ['nome','fantasia','cnpj','razao']

# By doing so, eligible variables are those ones which are not forbidden =)
eligible_variables = [coluna for coluna in df.columns if not any(palavra in coluna for palavra in Forbidden_variables)]

list_outliers = pd.DataFrame()

# For each variable on the dataset, do the following analysis
for column in df.columns:
    # For each forbidden variable:
    if column not in eligible_variables:
        col_data = df[column]
        motivo = check_input(col_data.name, input_rule, col_data)
        num_null = col_data.isnull().sum()
        num_total = len(col_data)
        num_distinct = col_data.nunique()
        completude = f"{(1 - (num_null / num_total)):.2%}"

        # Null Check
        # Here we shall verify if the number of null is greater than 5% of the number of available observations
        null_check = 'Verificar' if num_null > 0.05 * len(col_data) else 'Ok'
    # For each allowed variable:    
    if column in eligible_variables:
        col_data = df[column]
        motivo = check_input(col_data.name, input_rule, col_data)
        col_type = col_data.dtype
        num_null = col_data.isnull().sum()
        num_total = len(col_data)
        num_distinct = col_data.nunique()

        # Compute the percentage of fullness
        completude = f"{(1 - (num_null / num_total)):.2%}"

        # Null Check
        # Here we shall verify if the number of null is greater than 5% of the number of available observations
        null_check = 'Verificar' if num_null > 0.05 * len(col_data) else 'Ok'

        if is_qualitative(col_data):
            classe = 'Qualitativa'
        # Mode Check
        # Here we shall verify if the number of each factor is greater than 1% 
            moda_check = 'Ok'
            freq_observed = col_data.value_counts(normalize=True)
            if (freq_observed < 0.01).any():
                moda_check = 'Verificar'
            mean_quali = freq_observed.mean()
            std_quali = freq_observed.std()

        # Homogeneity Check
        # Here we shall verify if the observed frequency of each factor is adequate     
            cv_quali = (std_quali / mean_quali)*100 if col_data.dtype == 'object' and mean_quali != 0 else None
            cv_quali_check = 'Ok' if (cv_quali is None or cv_quali <= 200) else 'Verificar' 

        # Compute greatest mode for each variable and its own frequency
            moda = freq_observed.idxmax()
            moda_freq = f"{freq_observed.max():.2%}"
        else:
            moda = None
            moda_freq = None

        if is_quantitative(col_data):
            classe = 'Quantitativa'    
        # Filter of standard deviantions:
        # Here we shall compute the number of outliers by the common standard deviation filter
            filtro_sd_check = 'Ok'
            mean = col_data.mean()
            std = col_data.std()
            lower_bound = mean - 3 * std
            upper_bound = mean + 3 * std
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            justificativa = "Na coluna "+ col_data.name + " o valor observado foi identificado como outlier por estar fora do intervalo [{:.2f} , {:.2f}].".format(lower_bound,upper_bound) 
            num_outliers = len(outliers)
            out_list = df.iloc[outliers.index.tolist(), :].copy()
            out_list['Motivo'] = justificativa
            if num_outliers > 0.05 * len(col_data):
                filtro_sd_check = 'Verificar'
            list_outliers = pd.concat([list_outliers, out_list], ignore_index=True)
            maximum = col_data.max()
            minimum = col_data.min()
            median = col_data.median()
            med_inf = median - minimum
            med_sup = maximum - median

        # Coefficient of Variation
        # Here we compute the relation of mean and standard deviation and classify the variable
        cv = (std / mean) * 100 if is_quantitative(col_data) and mean != 0 else None
        cv_check = 'Ok' if (cv is None or cv <= 400) else 'Verificar'

        # Skewness 
        # Here we compute the coefficient of skewness, centered in the second moment
        Skewness_coef = np.mean((col_data - mean) ** 3) / (std ** 3) if is_quantitative(col_data) and std != 0 else None

        Skew_check = 'Ok' if (Skewness_coef is None or Skewness_coef <= 30) else 'Verificar'

        if is_timebased(col_data):
            classe = 'Temporal'
            freq_observed_time = col_data.value_counts(normalize=True)
            mean_time = freq_observed_time.mean()
            std_time = freq_observed_time.std()

        # Time Homogeneity Check
        # Here we shall verify if the observed frequency of each factor is adequate     
            cv_time = (std_time / mean_time)*100 if col_data.dtype == 'datetime64[ns]' and mean_time != 0 else None
            cv_time_check = 'Ok' if (cv_time is None or cv_time <= 20) else 'Verificar' 

    # Packing features into the output dataset
    output_df = pd.concat([output_df, pd.DataFrame([[
        column,
        col_type,
        motivo,
        classe,
        num_null,
        completude,
        null_check,
        median if is_quantitative(col_data) else None,
        minimum if is_quantitative(col_data) else None,
        med_inf if is_quantitative(col_data) else None,
        mean if is_quantitative(col_data) else None,        
        maximum if is_quantitative(col_data) else None,
        med_sup if is_quantitative(col_data) else None,
        std if is_quantitative(col_data) else None,
        num_distinct if col_data.dtype == 'object' or col_data.dtype == 'datetime64[ns]' else None,
        cv_quali if is_qualitative(col_data) else None,
        cv_quali_check if is_qualitative(col_data) else None,
        moda if is_qualitative(col_data) else None,
        moda_freq if is_qualitative(col_data) else None,
        moda_check if is_qualitative(col_data) else None,
        num_outliers if is_quantitative(col_data) else None,
        filtro_sd_check if is_quantitative(col_data) else None,
        cv if is_quantitative(col_data) else None,
        #cv_check if is_quantitative(col_data) else +None,
        Skewness_coef if is_quantitative(col_data) else None,
        Skew_check if is_quantitative(col_data) else None,
        cv_time if is_timebased(col_data) else None,
        cv_time_check if is_timebased(col_data) else None
    ]], columns=output_df.columns)], ignore_index=True)

# Based on the generated features, compute the final metric.
# Here the dataset will recieve a value, a percentage of quality.
valid_counts = output_df[output_df.columns[output_df.columns.str.contains('Avaliação')]].apply(lambda x: x.value_counts().get('Ok', 0))
total_counts = valid_counts + output_df[output_df.columns[output_df.columns.str.contains('Avaliação')]].apply(lambda x: x.value_counts().get('Verificar', 0))
num_factor = sum(~np.isnan(valid_counts/total_counts))
nota_final = np.nansum((1/num_factor)*(valid_counts/total_counts))
output_df = pd.concat([output_df, pd.DataFrame([[
    'Resultado',
    nota_final,
    None,
    None,
    None,
    None,
    f"{valid_counts['Avaliação de Nulos']} / {output_df['Avaliação de Nulos'].count()}",
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    f"{valid_counts['Avaliação do CH']} / {output_df['Avaliação do CH'].count()}",
    None,
    None,
    f"{valid_counts['Avaliação de Frequências']} / {output_df['Avaliação de Frequências'].count()}",
    None,
    f"{valid_counts['Avaliação de Filtro']} / {output_df['Avaliação de Filtro'].count()}",
    None,
    None,
    f"{valid_counts['Avaliação do CA']} / {output_df['Avaliação do CA'].count()}",
    None,
    f"{valid_counts['Avaliação de Datas']} / {output_df['Avaliação de Datas'].count()}"
]], columns=output_df.columns)], ignore_index=True)


# Using a notebook enviroment? Run those ones to visualize the final result and all dependencies
# Show the Final Dataset:
print("DataFrame de Saída:")
print(output_df)

# Show Duplicates
duplicates_df = df[df.duplicated(keep=False)]
print("\nDataFrame de Linhas Duplicadas:")
print(duplicates_df)
print(f"\nDimensão do DataFrame de Linhas Duplicadas: {duplicates_df.shape[0]} linhas x {duplicates_df.shape[1]} colunas")

# Show Outliers
list_outliers_df = list_outliers
print("\nDataFrame de Valores aberrantes")
print(list_outliers_df)

# Using a Dataiku enviroment? Create those datasets in the main python recipe (change to name_of_input_validation_df)
# Those datasets will be updated in every execution
#invest_desinvest_validation_df = output_df 

#invest_desinvest_duplicates_df = duplicates_df

#invest_desinvest_outliers_df = list_outliers_df
