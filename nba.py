import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st
import base64

st.markdown('''
![logo](https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQyjeCbSW_eG8PgCSXtcRQualH_nGnx6LUjow&usqp=CAU)	
# NBA players Stats
	''')

st.markdown('''
Esta aplicación realiza un rastreo web  simple de datos (***webscraping***),  de las  estadísticas de jugadores de la NBA!  
* **Librerias de python:** base64, pandas, streamlit  
* **Fuentes de datos:** [Basketball-reference.com](https://www.basketball-reference.com/)

|Realizado por|fecha|email|
|-------------|-----|-----|
|Luis Hernández|17 de septiembre 2020|[luishernand11@gmail.com](luishernand11@gmail.com)|
	''')

st.sidebar.header('Entrada del Usuario')
selected_year = st.sidebar.selectbox('Año', list(reversed(range(1950, 2021))))

#web scraping nba players
@st.cache
def load_data(year):
	url = 'https://www.basketball-reference.com/leagues/NBA_' + str(year) + '_per_game.html'
	html = pd.read_html(url, header=0)
	df = html[0]
	raw= df.drop(df[df.Age =='Age'].index)#elimina los header que se repiten
	raw = raw.fillna(0)
	playerstats = raw.drop(['Rk'], axis = 1)
	return playerstats
playerstats = load_data(selected_year)

#slider de la seleccion de los equipos
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Equipo', sorted_unique_team, sorted_unique_team)

#slider de la posisciion de los jugadores
unique_pos = ["C", 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Posicion', unique_pos, unique_pos)

#filtrar los datos
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Mostrar estadísticas de jugador de los equipos seleccionados')
st.write('Dimensión de los datos :' + ' ' +
	str(df_selected_team.shape[0]) + ' ' + 'Filas y' + ' ' +
	str(df_selected_team.shape[1]) +' ' + 'Columnas'
	)
st.dataframe(df_selected_team)

# Bajar o descargar  los datos en formato cvs
#codigos del foro de https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href



st.markdown(filedownload(df_selected_team), unsafe_allow_html = True)

#heatmap

if st.button('Intercorrelacion'):
	st.header('Heatmap Mátriz de Intercorrelación')
	df_selected_team.to_csv('output.csv', index=False)
	df = pd.read_csv('output.csv')
	
	corr = df.corr()
	mask = np.zeros_like(corr)
	mask[np.triu_indices_from(mask)] = True
	with sns.axes_style("white"):
		f, ax = plt.subplots(figsize=(7, 5))
		ax = sns.heatmap(corr, mask=mask, vmax=1, square=True, cmap = 'plasma')
	st.pyplot()
