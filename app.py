from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.boxofficemojo.com/year/world/')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div', attrs = {'class': 'a-section imdb-scroll-table-inner'})
rows = table.find_all('tr')

row_length = len(rows)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
	# get rank
    rank = rows[i].findAll('td')[0].text

    # get release group
    release_group = rows[i].findAll('td')[1].text

    # get worldwide
    worldwide = rows[i].findAll('td')[2].text

    # get domestic
    domestic = rows[i].findAll('td')[3].text
    
    # get foreign
    foreign = rows[i].findAll('td')[5].text
    
    temp.append((rank, release_group, worldwide, domestic, foreign)) 

# temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('rank', 'release_group', 'worldwide', 'domestic', 'foreign'))

#ini merupakan proses cleansing data yaitu mengubah tipe data penjualan tiket yang sebelumnya object menjadi integer
df['worldwide'] = df['worldwide'].str.replace("$","")
df['worldwide'] = df['worldwide'].str.replace(",","")
df['worldwide'] = df['worldwide'].astype('int64')
df['domestic'] = df['domestic'].str.replace("$","")
df['domestic'] = df['domestic'].str.replace(",","")
df['domestic'] = df['domestic'].str.replace("-","0")
df['domestic'] = df['domestic'].astype('int64')
df['foreign'] = df['foreign'].str.replace("$","")
df['foreign'] = df['foreign'].str.replace(",","")
df['foreign'] = df['foreign'].str.replace("-","0")
df['foreign'] = df['foreign'].astype('int64')

df = df.set_index('release_group')


#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["worldwide"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.head(10).plot(kind='barh', figsize = (10,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)