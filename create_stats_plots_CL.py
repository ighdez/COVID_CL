# Data Corona from 2020
# Jose Ignacio Hernandez
# October 2020

# Load packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print('COVID-19 plots v1.0')
print('Written by Jose Ignacio Hernandez')
print(' ')

# Load data
inputfile = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19_std.csv'
print('Loading URI: ' + inputfile)
dat_positives = pd.read_csv(inputfile,delimiter=',')

inputfile = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto38/CasosFallecidosPorComuna_std.csv'
print('Loading URI: ' + inputfile)
dat_deceased = pd.read_csv(inputfile,delimiter=',')

# Correct NAs and drop unused rows
dat_positives = dat_positives.fillna(0)
dat_positives.index = pd.to_datetime(dat_positives.Fecha).dt.date.astype('str')

dat_deceased = dat_deceased.fillna(0)
dat_deceased.index = pd.to_datetime(dat_deceased.Fecha).dt.date.astype('str')

# Create matrix of region selector numbers
unique_region = dat_positives['Codigo region'].unique()
unique_regname = dat_positives['Region'].unique()

strg = str(unique_region[0]) + ':\t' + unique_regname[0]
  
for i in range(1,len(unique_region)):
    strg = strg + '\n' + str(unique_region[i]) + ':\t' + unique_regname[i]

# Ask to choose region
ans = 0

while (ans < min(unique_region) or ans > max(unique_region)) or isinstance(ans,int)==0:
    print("Select the region to plot:")
    print(strg)
    ans = eval(input('Enter a valid number and press ENTER: '))

dat_positives = dat_positives[dat_positives['Codigo region']== ans]
dat_deceased = dat_deceased[dat_deceased['Codigo region']== ans]
chosen_region = unique_regname[unique_region == ans][0]

# Create matrix of commune selector numbers
unique_region = dat_positives['Codigo comuna'].unique().astype(int)
unique_regname = dat_positives['Comuna'].unique()

strg = str(unique_region[0]) + ':\t' + unique_regname[0]
  
for i in range(1,len(unique_region)):
    strg = strg + '\n' + str(unique_region[i]) + ':\t' + unique_regname[i]

# Ask to choose region
ans = -1

while (ans < min(unique_region) or ans > max(unique_region)) or isinstance(ans,int)==0:
    print("Select the commune to plot:")
    print(strg)
    ans = eval(input('Enter a valid number and press ENTER: '))

dat_positives = dat_positives[dat_positives['Codigo comuna']== ans]
dat_deceased = dat_deceased[dat_deceased['Codigo comuna']== ans]
chosen_commune = unique_regname[unique_region == ans][0]

dat_positives = dat_positives.drop(['Fecha','Region','Codigo region','Comuna','Codigo comuna','Poblacion'],axis=1)
dat_deceased = dat_deceased.drop(['Fecha','Region','Codigo region','Comuna','Codigo comuna','Poblacion'],axis=1)

tag_plots = chosen_region + ' / ' + chosen_commune
tag_files = str(ans)
commune_code = str(ans)

print('Selected region / commune: ' + tag_plots)
print(' ')

# Check if there is an update
last_date = dat_positives.index[-1]
print('The last update is from ' + last_date)

# Show in window
print('Number of positive cases:   ' + str(int(dat_positives['Casos confirmados'][-1])))
print('Number of deceased:         ' + str(int(dat_deceased['Casos fallecidos'][-1])))

# Ask whether plots are generated
ans = ' '

while ans != 'y' and ans != 'n':
    ans = input('Do you want to create plots? (y/n): ').lower().strip()

if ans == 'n':
    print('Aborted by user.')
    exit()

# Create plots
print('Creating plots...')

# Positive cases
plt.figure(figsize=(7,5))
plt.bar(dat_positives.index, dat_positives['Casos confirmados'])
plt.margins(0,0)
plt.ylabel('Number of cases')
plt.title('Accumulative positive cases. ' + tag_plots + ' (today: ' + str(int(dat_positives['Casos confirmados'][-1])) + ')')
plt.xticks(np.arange(0,len(dat_positives.index),(len(dat_positives.index)-1)/15).round(),rotation=30,fontsize=8,ha='right')

# Export 
output_positives = 'positives_CL_' + last_date + '_' + commune_code + '.png'
plt.savefig(output_positives)
print('Filename ' + output_positives + ' exported.')

# Deceased plot
plt.figure(figsize=(7,5))
# plt.subplot(1, 3, 3)
plt.bar(dat_deceased.index, dat_deceased['Casos fallecidos'],color='red')
plt.margins(0,0)
plt.title('Accumulative deceased ' + tag_plots + ' (today: ' + str(int(dat_deceased['Casos fallecidos'][-1])) + ')')
plt.xticks(np.arange(0,len(dat_deceased.index),(len(dat_deceased.index)-1)/20).round(),rotation=30,fontsize=8,ha='right')
plt.savefig('deceased_CL_' + last_date + '_' + ans + '.png')

# Export
output_positives = 'deceased_CL_' + last_date + '_' + commune_code + '.png'
plt.savefig(output_positives)
print('Filename ' + output_positives + ' exported.')


