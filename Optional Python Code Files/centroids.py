import pandas as pd
from shapely.geometry import MultiPoint

# read the csv file containing borderline longitudes and latitudes for all Indian districts
df = pd.read_csv(r"C:\Users\sam\IndiaMap\Ind_adm2_Points.csv")

district = ""
geoList = []
result_df = pd.DataFrame(data=None,columns=['State','District','Latitude','Longitude'])

for index, row in df.iterrows():
    # check if this is anew district value
    if district and (district!=df.iloc[index]['District']):
        # calculate centroid for previous district
        points = MultiPoint(geoList)
        # save the state, district, long-lat and centroid to new dataframe
        result_df = result_df.append({'State':df['State'].iloc[index-1],'District':df['District'].iloc[index-1],'Latitude':points.centroid.x,'Longitude':points.centroid.y}, ignore_index=True)
        # clear old geoList (APPEND NEW LONG-LAT ALSO)
        del geoList[:]
    # save this new district's name
    district = df.iloc[index]['District']
    # add this long lat info to later calculate centroid
    geoList.append((df.iloc[index]['Latitude'],df.iloc[index]['Longitude']))

# add last district's centroid
if geoList:
    points = MultiPoint(geoList)
    result_df = result_df.append({'State':df['State'].iloc[-1],'District':df['District'].iloc[-1],'Latitude':points.centroid.x,'Longitude':points.centroid.y}, ignore_index=True)
    del geoList[:]

result_df.to_csv("centroids.csv",index=False)