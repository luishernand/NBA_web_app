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
|Luis Hernández|2 de octubre 2020|[luishernand11@gmail.com](luishernand11@gmail.com)|
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

######################################
# Exploratory data Analysis
######################################
#convertir los datos a numericos
entire= df_selected_team.astype({'Age': 'int','G':'int', 'GS': 'float', 'MP': 'float', 'FG':'float', 'FGA':'float',
 'FG%':'float', '3P':'float','3PA':'float', '3P%':'float', '2P':'float', '2PA':'float', '2P%':'float',
  'eFG%':'float', 'FT':'float', 'FTA':'float', 'FT%':'float', 'ORB':'float',
       'DRB':'float', 'TRB':'float', 'AST':'float', 'STL':'float', 'BLK':'float', 'TOV':'float', 'PF':'float',
       'PTS':'float'})

# Top 5
st.write('''
    ### Lideres de la Temporada
    ''')
#1 Jugador lider en puntos
most_points = entire.nlargest(5, 'PTS').set_index('Player')
st.subheader('puntos')
st.write(most_points[['Tm', 'PTS']])

# Score 20 or more points per game

more_20 = entire[entire.PTS >20]
more_20_filtered = more_20.nlargest(5, 'PTS')[['Player', 'Tm', 'PTS']].set_index('Player')
st.subheader('Jugadores con 20pts o más')
st.write(more_20_filtered)


#2 Which player  the most AST (AST) Per Game?
playersmostpoints = entire.nlargest(5, 'AST').set_index('Player')
st.subheader('asistencias')
st.write(playersmostpoints[['Tm', 'AST']])

# 3 Rebotes
rebotes = entire.nlargest(5, 'TRB').set_index('Player')
st.subheader('Rebotes')
st.write(rebotes[['Tm', 'TRB']])

#4  Tapones
tapones = entire.nlargest(5, 'BLK').set_index('Player')
st.subheader('tapones')
st.write(tapones[['Tm', 'BLK']])

#5 Bolas robadas
steals = entire.nlargest(5, 'STL').set_index('Player')
st.subheader('Bolas Robadas')
st.write(steals[['Tm', 'STL']])

#6 Eficiencia en field goal
#field_goal = entire.nlargest(5, 'eFG%').set_index('Player')
#st.subheader('% Field Goal')
#st.write(field_goal[['Tm', 'eFG%']])

#7  Tiros de campo
#tiros_campo = entire.nlargest(5, 'FG%').set_index('Player')
#st.subheader('% de Tiros de campo')
#st.write(tiros_campo[['Tm', 'FG%']])

#8 Players wich most 3P% per game?
three_point = entire.nlargest(5, '3P%').set_index('Player')
st.subheader('Lider en % de 3pts')
st.write(three_point[['Tm', '3P%']])

#9 free trows %?
three_trows = entire.nlargest(5, 'FT%').set_index('Player')
st.subheader(' % de Tiros libre')
st.write(three_trows[['Tm', 'FT%']])

#10 Cantidad minutos jugados
games = entire.nlargest(5, 'MP').set_index('Player')
st.subheader('Minuts por juegos')
st.write(games[['Tm', 'MP']])

#11 free trows ?
free_trows = entire.nlargest(5, 'FT').set_index('Player')
st.subheader(' Tiros libre')
st.write(free_trows[['Tm', 'FT']])

#12 free trows per game?
free_trows_pergame = entire.nlargest(5, 'FTA').set_index('Player')
st.subheader(' Tiros libres por juego')
st.write(free_trows_pergame[['Tm', 'FTA']])

#13  Triples antados?
triples_anotados = entire.nlargest(5, '3P').set_index('Player')
st.subheader(' Triples anotados')
st.write(triples_anotados[['Tm', '3P']])


#14 Triples por juego
triples_por_juego = entire.nlargest(5, '3PA').set_index('Player')
st.subheader(' triples por juego')
st.write(triples_por_juego[['Tm', '3PA']])


#15 Balones perdidos
balones_perdidos = entire.nlargest(5, 'TOV').set_index('Player')
st.subheader(' Balones perdidos')
st.write(three_point[['Tm', 'TOV']])

# 16 Faltas cometidas?
personal_foul = entire.nlargest(5, 'PF').set_index('Player')
st.subheader(' Faltas personales')
st.write(three_point[['Tm', 'PF']])





