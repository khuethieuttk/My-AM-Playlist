#!/usr/bin/env python
# coding: utf-8

# In[209]:


import pandas as pd
import xml.etree.ElementTree as ET

# Handle the data from xml file to DataFrame that can be worked on
def parse_itunes_xml(xml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Locate the "Tracks" dictionary
    tracks_dict = root.find(".//dict/dict")
    
    # Extract track data
    tracks = []
    for track in tracks_dict.findall("dict"):
        track_data = {}
        key = None
        for element in track:
            # Detect <key> and save it for the next element
            if element.tag == "key":
                key = element.text
            elif key:
                # Handle different data types
                if element.tag == "integer":
                    track_data[key] = int(element.text)
                elif element.tag == "string":
                    track_data[key] = element.text
                elif element.tag == "date":
                    track_data[key] = element.text
                key = None  # Reset key after saving
        tracks.append(track_data)

    # Convert to DataFrame
    df = pd.DataFrame(tracks)
    return df

xml_path = r"C:\Users\OneDrive\Music.xml"
df = parse_itunes_xml(xml_path)

# Display the DataFrame
print(df.head())


# In[73]:


# Total play counts
tot_play = df["Play Count"].sum()

# Total songs
tot_song = df["Name"].count()

# Total artists
tot_artist = df["Artist"].nunique()

# Total albums
tot_album = df["Album"].nunique()

# Make a summary table of total numbers
import hvplot.pandas
summary_df = pd.DataFrame({'Title':['Total Songs', 'Total Plays','Total Artists','Total Albums'],
                           'Value':[f'{tot_song} songs', f'{tot_play} plays', f'{tot_artist} artists', 
                                    f'{tot_album} albums']})

summary_table = summary_df.hvplot.table()
summary_table


# In[238]:


# See the most played song in my playlist
most_played_song = df[df['Play Count'] == df['Play Count'].max()]

for _, row in most_played.iterrows():
    print(f'Song with the Most Play Count: {row["Name"]} by {row["Artist"]} with {row["Play Count"]} plays')

# Most played artist
artist_played = df.groupby('Artist')['Play Count'].sum()
most_played_artist = artist_played.idxmax()
max_artist_pcount = artist_played.max()

print(f"Artist with most plays: {most_played_artist} with {max_artist_pcount} plays")

# Most played album
album_played = df.groupby('Album')['Play Count'].sum()
most_played_album = album_played.idxmax()
max_album_pcount = album_played.max()

print(f'Album with most plays: {most_played_album} with {max_album_pcount} plays')



# In[244]:


# See the play counts of each songs in my playlist
play_per_song = df.groupby('Name', as_index=False)['Play Count'].sum()

# Convert it into a table
sort_play_per_song = play_per_song.sort_values(by='Play Count',ascending=[False])
play_per_song_table = sort_play_per_song.hvplot.table()
play_per_song_table


# In[241]:


# See the play counts of each artist in my playlist
play_per_artist = df.groupby('Artist', as_index=False)['Play Count'].sum()

# Convert it into a table
sort_play_per_artist = play_per_artist.sort_values(by='Play Count',ascending=[False])
play_per_artist_table = sort_play_per_artist.hvplot.table()
play_per_artist_table


# In[242]:


# See the play counts of each album in my playlist
play_per_album = df.groupby('Album', as_index=False)['Play Count'].sum()

# Convert it into a table
sort_play_per_album = play_per_album.sort_values(by='Play Count',ascending=[False])
play_per_album_table = sort_play_per_album.hvplot.table()
play_per_album_table


# In[62]:


# See the number of songs in each genre in my playlist
genre_counts = df["Genre"].value_counts()

print("Most Common Genres:")
print(genre_counts)


# In[151]:


# Count the number of songs in each genre
genre_counts = df['Genre'].value_counts().head(20)

# Count the total songs:
tot_counts = len(df)
print("Genre:")
# Count the percentage of songs in each genre
for genre, count in genre_counts.items():
    genre_percentage = round(count / tot_counts *100,2)
    print(f'{genre} - {genre_percentage}%')


# In[45]:


# See the number of songs by each artist in my playlist
artist_counts = df["Artist"].value_counts()

print("Most Common Artists:")
print(artist_counts)


# In[6]:


# Count the songs by each artist
artist_counts = df["Artist"].value_counts().head(10)

# Count the total songs
tot_counts = len(df)
print("Artist:")

# Count the percentage of songs by each artist
for artist, count in artist_counts.items():
    artist_percentage = round(count / tot_counts *100,2)
    print(f'{artist} - {artist_percentage}%')


# In[95]:


# See the number of tracks in each album in my playlist
album_counts = df["Album"].value_counts()

print("Albums with the most tracks:")
print(album_counts)


# In[66]:


import hvplot.pandas
# Make a table showing the genre coverage in my playlist
genre_counts = df['Genre'].value_counts().head(20)
tot_counts = len(df)

summary_df2 = pd.DataFrame(columns=['Genre','%'])
for genre, count in genre_counts.items():
    genre_percentage = round(count / tot_counts *100,2)
    summary_df2 = pd.concat([summary_df2,pd.DataFrame({'Genre':[genre],
                           '%':f'{genre_percentage}%'})])
    
genre_summary = summary_df2.hvplot.table()
genre_summary


# In[270]:


import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')

# Turn the genre coverage into an interactive bar chart
genre_counts = df["Genre"].value_counts().head(20)
tot_counts = len(df)
genres =[]
percentages=[]
for genre, count in genre_counts.items():
    genre_percentage = round(count / tot_counts *100,2)
    genres.append(genre)
    percentages.append(genre_percentage)

genre_df = pd.DataFrame({'Genre':genres, 'Percentage':percentages})
genre_chart = genre_df.hvplot.bar(x='Genre',y='Percentage',color='lightblue',title='Most common genres').opts(ylim=(0,30),shared_axes=False)
genre_chart


# In[104]:


# Make a table showing the artist coverage in my playlist
artist_counts = df['Artist'].value_counts().head(20)
tot_counts = len(df)
summary_df3=pd.DataFrame(columns=['Artist','%'])

for artist, count in artist_counts.items():
    artist_percentage = round(count / tot_counts *100,2)
    summary_df3 = pd.concat([summary_df3,pd.DataFrame({'Artist':[artist],
                           '%':f'{artist_percentage}%'})])
    
artist_summary = summary_df3.hvplot.table(min_width={'Artist', '%'})
artist_summary


# In[271]:


import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')

# Turn the artist coverage into an interactive bar chart
artist_counts = df["Artist"].value_counts().head(20)
tot_counts = len(df)
artists =[]
percentages=[]
for artist, count in artist_counts.items():
    artist_percentage = round(count / tot_counts *100,2)
    artists.append(artist)
    percentages.append(artist_percentage)

artist_df = pd.DataFrame({'Artist':artists, 'Percentage':percentages})
artist_chart = artist_df.hvplot.bar(x='Artist',y='Percentage',color='green',title='Most common artists').opts(ylim=(0,5),shared_axes=False)
artist_chart


# In[272]:


# Final dashboard
import panel as pn
pn.extension('tabulator')

# Showing all the tables and charts on a "My Playlist Summary" dashboard
template = pn.template.FastListTemplate(
    title = "My Playlist Summary",
    logo = r"C:\Users\35c1c4bd969123cf7a80.jpg",
    header_background = "lightblue",
    main =[
        pn.Row(summary_table,play_per_song_table,play_per_artist_table,play_per_album_table,width=300,height=200),
        pn.GridBox(artist_summary,artist_chart,ncols=2,align='start',sizing_mode='stretch_width'),
        pn.GridBox(genre_summary,genre_chart,ncols=2,align='start',sizing_mode='stretch_width')
    ]
)
template.show()
        





