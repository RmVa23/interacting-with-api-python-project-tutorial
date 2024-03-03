import pandas as pd
import spotipy
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()

client_id = os.environ.get("Client_ID")
client_secret = os.environ.get("Client_secret")

sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Código de spotify del artista (en este caso los Strokes)
the_strokes = '0epOFNiUfyON9EYx7Tpr6V'

# Solicitud a la API con nuestras claves de acceso (sp) de los datos del artista - (sobra)
artist = sp.artist('0epOFNiUfyON9EYx7Tpr6V')

# Solicitud a la API del top de canciones del artista de interés
top_tracks_response = sp.artist_top_tracks(the_strokes)

# Extraemos la información de las canciones principales
top_tracks = top_tracks_response['tracks']

# Lista para almacenar los resultados (necesaria para posteriormente convertir a DataFrame)
best_songs_strokes = []

# Sacar nombre de la canción, duración y popularidad
# Iteramos sobre las canciones principales y mostramos sus nombres

print("Top 10 de canciones del artista:")
for i, track in enumerate(top_tracks[:10], 1):  # 1. enumerate() es una función de Python que toma una secuencia (en este caso, la lista top_tracks[:10] que contiene las primeras 10 canciones principales del artista)
    nombre = track['name']                      #   y devuelve un iterador que genera pares (índice, elemento) para cada elemento en la secuencia. El segundo argumento opcional 1 especifica el valor inicial del índice, que en este caso comienza en 1 en lugar del valor predeterminado 0.
    popularidad = track['popularity']           # 2. for i, track in ...: Esto es una declaración de bucle for que itera sobre los elementos generados por enumerate().
    duracion = track['duration_ms']             #   En cada iteración, i será el índice de la canción en la lista (1, 2, 3, ..., 10) y track será la información de la canción.
    print(f"{i}. {nombre} - {popularidad} - {duracion}")

    # Añadimos la información extraída de interés a la lista (dentro del bucle!!)
    best_songs_strokes.append({'Nombre': nombre, 'Popularidad': popularidad, 'Duración (ms)': duracion})

# Convertimos la lista en un DataFrame
data = pd.DataFrame(best_songs_strokes)

# Ordenamos el dataframe por popularidad creciente y mostramos el top 3
data_ordenado = data.sort_values(by='Popularidad')
top_3 = data_ordenado.tail(3)

# Análisis popularidad - duracion
plt.figure(figsize=(10, 5))
plt.scatter(data['Duración (ms)'], data['Popularidad'], color='blue')
plt.title('Relación entre Popularidad y Duración de las Canciones')
plt.xlabel('Duración (ms)')
plt.ylabel('Popularidad')
plt.grid(True)
plt.show()

# Correlación entre la popularidad y la duración de las canciones
correlacion = data['Popularidad'].corr(data['Duración (ms)'])
print("Correlación entre popularidad y duración:", correlacion)
# La correlación varía entre -1 y 1. Un valor cercano a 1 indica una correlación positiva (las variables aumentan juntas),
# un valor cercano a -1 indica una correlación negativa (una variable aumenta mientras que la otra disminuye)
# y un valor cercano a 0 indica una correlación débil o nula.
print(f"Como podemos observar tanto en el gráfico como en la metida cuantitativa ({correlacion}), apenas hay correlacion entre la popularidad de las canciones y su duración.")

# Estadísticas descriptivas de la popularidad
popularity_stats = data['Popularidad'].describe()
print("Estadísticas descriptivas de la popularidad:")
print(popularity_stats)

# La desviación estándar de la popularidad es relativamente baja,
# lo que indica que las puntuaciones de popularidad están relativamente cerca de la media,
# con una dispersión moderada alrededor de la media

# Con estas estadísticas, podemos concluir que la mayoría de las canciones tienen una popularidad cercana a la media,
# con una dispersión moderada alrededor de ella. La popularidad de las canciones varía desde 70 hasta 83,
# con la mayoría de las canciones teniendo una popularidad en el rango de 70 a 75.

# Matriz de correlación

matrix = data[['Popularidad', 'Duración (ms)']]
correlation_matrix = matrix.corr()
print(correlation_matrix)
