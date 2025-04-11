import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

filepath1 = 'Customer Flight Activity.csv'
filepath2 = 'Customer Loyalty History.csv'

dataFlight = pd.read_csv(filepath1)
dataLoyalty = pd.read_csv(filepath2)

#Traz todas as informações contidas nas tabela
# print(dataFlight.info)
# print('\n')
# print(dataLoyalty.info)

uniqueEnrollmentTypes = dataLoyalty['Enrollment Type'].unique()
uniqueEnrollmentYears = dataLoyalty['Enrollment Year'].unique()

#Traz os anos e os tipos de planos
# print(uniqueEnrollmentTypes) ['Standard' '2018 Promotion']
# print(uniqueEnrollmentYears) [2016 2014 2013 2012 2015 2018 2017]

#inplace : bool, default False
#Whether to modify the DataFrame rather than creating a new one.
dataLoyalty.drop_duplicates(inplace=True)

#drop : bool, default False
#Do not try to insert index into dataframe columns. This resets the index to the default integer index.
#inplace : bool, default False
#Whether to modify the DataFrame rather than creating a new one.
dataLoyalty.reset_index(drop= True, inplace=True)

#Retorna True se existir algum campo nulo qualquer na tabela
nanValues = dataLoyalty.isnull().any()

#Exibe as colunas com os campos nulos
# if nanValues.any():
#     nanColumns = nanValues[nanValues].index.tolist()
#     print(f"As colunas com números vazios são: {nanColumns}")
# else:
#     print("Não há colunas com valores nulos")

#Cria um novo campo, formatando os campos de ano e mês em apenas um (data de dia 01 usada por conveniência)
dataLoyalty['Enrollment Date'] = pd.to_datetime(dataLoyalty['Enrollment Year'].astype(str) + '-' + dataLoyalty['Enrollment Month'].astype(str) + '-01')

campaignStartDate = pd.to_datetime("2018-02-01")
campaignEndDate = pd.to_datetime("2018-04-30")

# Filtra somente as resevas feitas durante campanha
enrollmentPromotion2018 = dataLoyalty[(dataLoyalty["Enrollment Type"].str.contains('Promotion',na=False)) & (dataLoyalty['Enrollment Date'] >= campaignStartDate) & (dataLoyalty['Enrollment Date'] <= campaignEndDate)]


#.shape retorna uma tupa com o número de linhas e colunas, usamos [0] para utilizar somente a primeira informação
enrollmentPromotion2018Count = enrollmentPromotion2018.shape[0]

print(enrollmentPromotion2018Count)
#Números de reservas canceladas durante o período de promoçoes
#isin() : Whether elements in Series are contained in values.
cancellPromotions2018 = dataLoyalty[(dataLoyalty['Cancellation Year'] == 2018) & (dataLoyalty['Cancellation Month'].isin([2,3,4]))]

#len() e .shape[0] funcionam da mesma meneira
cancellPromotions2018Count = len(cancellPromotions2018)

#Outputs
print(f"Inscrições na promoção: {enrollmentPromotion2018Count}")
print(f"Cancelamentos na promoção: {cancellPromotions2018Count}")
print(f"Somatório na promoção: {enrollmentPromotion2018Count-cancellPromotions2018Count}")

#Puxando o período de 2017 e 2018
enrollmentTimeSlice = dataLoyalty[(dataLoyalty['Enrollment Year'] >= 2017) & (dataLoyalty['Enrollment Year'] <= 2018)]

#agrupamento por Mês e por ano, onde criando a estrutura {Enrollmente Year : Enrollment Month}
#.size(): Number of rows in each group as a Series if as_index is True or a DataFrame if as_index is False.
#.reset_index(): This is useful when the index needs to be treated as a column, or when the index is meaningless and needs to be reset to the default before another operation.
enrollmentByMonthCount = enrollmentTimeSlice.groupby(['Enrollment Year', 'Enrollment Month']).size().reset_index(name='Count')

#Sinalizando quais meses do período escolhido são de promoção e quais não
enrollmentByMonthCount['Promotion Enrollment'] = np.where(
    (enrollmentByMonthCount['Enrollment Year'] == 2018) &
    (enrollmentByMonthCount['Enrollment Month'].between(2, 4)),
    '2018 Feb-Apr',
    'Other'
)

# Deine a palheta de cores a serem usadas
sns.set_palette("dark")

# Define o tamanho da tabela a ser exibida
plt.figure(figsize=(12, 6))
# Adiciona uma linha à tabela. hue: Divisão das linhas; marker: Marcador na linha
sns.lineplot(data=enrollmentByMonthCount, x='Enrollment Month', y='Count', hue='Enrollment Year', marker='o')

# Adicionando a linha vermelha tracejada somente no período das promoções (enrollmentByMonthCount['Promotion Enrollment'] == '2018 Feb-Apr')
promotion_period_data = enrollmentByMonthCount[enrollmentByMonthCount['Promotion Enrollment'] == '2018 Feb-Apr']
sns.lineplot(data=promotion_period_data, x='Enrollment Month', y='Count', color='red', marker='o', linestyle='--')

plt.title('Monthly Enrollment Counts in 2017 and 2018 with Promotion Period Highlighted')
plt.xlabel('Month')
plt.ylabel('Number of Enrollments')
# xticks garante que a quantidade total de mêses seja exibida
plt.xticks(range(1, 13))
plt.legend(title='Year')
plt.grid(True)
plt.show()