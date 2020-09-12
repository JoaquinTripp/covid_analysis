"""Amphora Health:
Challenge code. 
Author: Joaquin Tripp Gudiño
Date: September 11, 2020. 

This is a correlation analysis, searching for the factors associated with
 ICU (Intensive Care Unity) usage by state,
in the people infected with Covid-19 in Mexico.

The Covid-19 is the infectious disease caused by the most recently discovered 
coronavirus. On March 11 of 2020,the World Health Organization declared the 
virus COVID-19 a Pandemic. Currently, on September 2020, there are more than 
27,000,000 of people infected around the world. In Mexico, there are almost 
650,000 and it ranks number 4 in deaths. 

The informtaion used in this analysis, was taken from Mexico's ministry of 
health website:
https://www.gob.mx/salud/documentos/datos-abiertos-152127, 
"""

#Librarys used
import pandas as pd
import csv
import matplotlib.pyplot as plt

#Import the data
data = pd.read_csv('200909COVID19MEXICO.csv',encoding='windows-1252')


"""This is a correlation analysis about the people with COVID in ICU,therefore, 
we need to filtered the information to exclude the negative cases and only use
the positives
"""

#Filtering the information about infected people
data_uci = data[data['RESULTADO'] == 1]
print(f'\n--------The Data has been filtered up-----------')


"""It is neccessary to clean up the data, because in some cases, there is no register 
about if patient had or had not the disease, then are resgistered with 97, 98 
and 99. It may causes lags. 
The correlation analysis will be gruped by state (I have took the state
of residence from the COVID database), and others groups wil be considered too, like 
the age and gender. 
"""

#List of the factors in the database that will be used
factors = ['NEUMONIA','DIABETES','EPOC','ASMA','INMUSUPR','HIPERTENSION',
'CARDIOVASCULAR','OBESIDAD',
'RENAL_CRONICA','TABAQUISMO']

list_genders = [0,1]
list_states = []
for s in range(33):
    list_states.append(s)
key_disease = 'UCI'
age = []
uci_cases = []
uci_cases_per = []
total_uci_cases = data_uci['UCI'][data_uci['UCI'] == 1].count()

#The number of UCI cases by age. The 90% of the cases are betweem the 25 and 80 years old. 
for n in range(0,110):
    new_cases = data_uci['EDAD'][data_uci['EDAD'] == n][data_uci['UCI'] == 1].count()
    new_cases_per = new_cases/total_uci_cases
    age.append(n)
    uci_cases.append(new_cases)
    print(f'Age {n}:{new_cases} : {new_cases_per*100}%')

input(f'¿Continue?')

#The list of the states
states = ['AGUASCALIENTES','BAJA CALIFORNIA','BAJA CALIFORNIA SUR','CAMPECHE',
'COAHUILA DE ZARAGOZA','COLIMA','CHIAPAS','CHIHUAHUA','CIUDAD DE MÉXICO','DURANGO',
'GUANAJUATO','GUERRERO','HIDALGO','JALISCO','MÉXICO','MICHOACÁN DE OCAMPO','MORELOS',
'NAYARIT','NUEVO LEÓN','OAXACA','PUEBLA','QUERÉTARO','QUINTANA ROO','SAN LUIS POTOSÍ',
'SINALOA','SONORA','TABASCO','TAMAULIPAS','TLAXCALA','VERACRUZ','YUCATÁN','ZACATECAS']

genders = ['Female','Male']
#This function runs the correlation between the infected people with UIC vs the infected people
# with each disease given in the parameter name_2, grouped by date. 
def corr_data(name_1,name_2):
#Count the number of positive cases
    group_x = data_uci.groupby(['FECHA_INGRESO'])[[name_1]].apply(lambda x: x[ x == 1].count())
    group_y = data_uci.groupby(['FECHA_INGRESO'])[[name_2]].apply(lambda x: x[ x == 1].count())
#Define the two list to compare
    x = group_x[name_1]
    y = group_y[name_2]
#Correlation method application
    coef = x.corr(y,method='pearson')
    #if x.count() == y.count():
        #print(f'There are {x.count()} people with UCI')
    #else:
        #print('UPS! something went wrong')
    return coef 

#Variables to get the disease and the UCI cases by day
value_x = []
value_y = []
#A dictionary to save the correaltion for each disease
disease_corr = {}

#Create a new file to save the correlations for each disease by state
outfile = open('results_by_state_gender.csv', 'w')
print(f'STATE,GENDER,NEUMONIA,DIABETES,EPOC,ASMA,INMUSUPR,HIPERTENSION,CARDIOVASCULAR,OBESIDAD,RENAL_CRONICA,TABAQUISMO', file = outfile)

#Run the code for the 32 states
for state in range(1,33):
    print(f'\n---------------------------{states[state-1]}------------------------')
    print(f'\nIn {states[state-1]}')
    #By gender
    for gender in range(1,3):
        data_uci = data[data['ENTIDAD_RES'] == state][data['RESULTADO'] == 1 ][data['SEXO'] == gender]
        counter = 0
        #by disease
        for item in factors:
            counter += 1
            #Define the UCI cases and the disease cases to correlate
            value_x = 'UCI'
            value_y = item
            #Correlation method
            run = corr_data(name_1 = value_x, name_2 = value_y)
            #dic = {f'UCI vs {item}' : run}
            #print(f'{counter} corrida: {value_x} vs {value_y}\nScore = {run}')
            
            #Dictionary of disease correlations
            disease_corr[item] = run

        #for item, key in disease_corr.items():
            #print(f'UCI vs {item} : {key}')

        #Max correlation founded
        max_corr = max(disease_corr.values())
        #define the disease variable to print it on the outfile
        disease = []

        for item, score in disease_corr.items():
            if score == max_corr:
                disease = item
        #Print the max correaltion by gender for each state
        print(f'\t>>> The max correlation is {max_corr} by {disease} disease in {genders[gender-1]}.')
        
        #Print the information about all correlations by state, gender and disease, on the outfile
        print(f'{states[state-1]},{genders[gender-1]},{disease_corr["NEUMONIA"]},{disease_corr["DIABETES"]},{disease_corr["EPOC"]},{disease_corr["ASMA"]},{disease_corr["INMUSUPR"]},{disease_corr["HIPERTENSION"]},{disease_corr["CARDIOVASCULAR"]},{disease_corr["OBESIDAD"]},{disease_corr["RENAL_CRONICA"]},{disease_corr["TABAQUISMO"]}', file = outfile)
        
        #Refresh the outfile
        outfile.flush()

print(f'---------The process has finished-----------')
final_file = pd.read_csv('results_by_state_gender.csv',encoding = 'windows-1252')
print(f'Information description{final_file.describe()}')


