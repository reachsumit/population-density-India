from bs4 import BeautifulSoup as bs
import requests

# Base url for scraping
res=requests.get('http://www.citypopulation.de/India.html')
# delicious soup
soup= bs(res.text,'lxml')
# path to the required links
allLinks = soup.select('ul li a')
# keep only the links with full district data
allLinks = allLinks[int(len(allLinks)/2):]

# form direct links to each state
state = []
links = []
for item in allLinks:
    state.append(item.text)
    links.append("http://www.citypopulation.de/"+item.attrs['href'])

# use Pandas to directly fetch table from the webpage
population_df = pd.DataFrame(data=None,columns=['State','District','Population in 2001','Population in 2011'])
for idx, link in enumerate(links):
    temp_df = pd.read_html(link)[0]
    for index, row in temp_df.iterrows():
        if temp_df['Status'].iloc[index] == 'District':
            population_df = population_df.append({'State':state[idx],'District':temp_df['Name'].iloc[index],'Population in 2001':temp_df['PopulationCensus2001-03-01'].iloc[index],'Population in 2011':temp_df['PopulationCensus2011-03-01'].iloc[index]}, ignore_index=True)

# save population data to csv
population_df.to_csv("population.csv",index=False)