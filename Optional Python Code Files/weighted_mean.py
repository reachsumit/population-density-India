import pandas as pd

input_df = pd.read_csv(r"merged.csv")
state = ""
weights = []
x_numerator = []
y_numerator = []
results = pd.DataFrame(data=None,columns=['State','Longitude','Latitude'])

for index,x in input_df.iterrows():
    if state and (state!=input_df.iloc[index]['State']):
        #calculate weighted mean for the last state
        longitude = sum(x_numerator)/sum(weights)
        latitude = sum(y_numerator)/sum(weights)
        #empty lists
        del x_numerator[:]
        del y_numerator[:]
        del weights[:]
        #store to results dataframe
        results = results.append({'State':state,'Longitude':longitude,'Latitude':latitude}, ignore_index=True)
    state = input_df.iloc[index]['State']
    weights.append(float(input_df.iloc[index]['Population in 2001']))
    x_numerator.append(float(input_df.iloc[index]['Longitude'])*float(input_df.iloc[index]['Population in 2001']))
    y_numerator.append(float(input_df.iloc[index]['Latitude'])*float(input_df.iloc[index]['Population in 2001']))
    
# add last weight
if weights:
    longitude = sum(x_numerator)/sum(weights)
    latitude = sum(y_numerator)/sum(weights)
    del x_numerator[:]
    del y_numerator[:]
    del weights[:]
    results = results.append({'State':state,'Longitude':longitude,'Latitude':latitude}, ignore_index=True)
    
results.to_csv(r'results_2001.csv',index=False)