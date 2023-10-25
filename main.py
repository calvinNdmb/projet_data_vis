import streamlit as st
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import pandas as pd
import plotly as pl
import plotly.graph_objects as go
from bokeh.models import GeoJSONDataSource, HoverTool
from bokeh.plotting import figure

#extrem_left = ["ARTHAUD","POUTOU"]
#extrem_right = ["LE PEN","ZEMMOUR","DUPONT-AIGNAN",'CHEMINADE']
#left=["JADOT","HIDALGO","ROUSSEL",'HOLLANDE','JOLY']
#right=["PÉCRESSE","SARKOZY"]
#centre =["MACRON","BAYROU"]

def calcule_vote_camp(row, candidates):
    return row[candidates].sum()

def calcule_color(row):
    if row.right_candidates > row.center_candidates  and row.right_candidates > row.left_candidates :
        return 'blue'
    if row.center_candidates > row.left_candidates :
        return 'white'
    else :
        return 'red'
     
def slider_annee(dfannee_2012,dfannee_2017,dfannee_2022):
    slid = st.select_slider(
        'Select a year',
        options=[2012,2017,2022])

    if slid == 2012:
        df=dfannee_2012
        st.write("## Graphique des votes par candidat pour l'année 2012")
        st.bar_chart([df['ARTHAUD'].sum(),df['BAYROU'].sum(),df['CHEMINADE'].sum(),
                    df['DUPONT-AIGNAN'].sum(),df['HOLLANDE'].sum(),df['JOLY'].sum(),
                    df['LE PEN'].sum(),df['MELENCHON'].sum(),df['POUTOU'].sum(),
                    df['SARKOZY'].sum()])
        st.write("""
                    ### Légende
                    - **0: ARTHAUD**: Votes pour Arthaud
                    - **1: BAYROU**: Votes pour Bayrou
                    - **2: CHEMINADE**: Votes pour Cheminade
                    - **3: DUPONT-AIGNAN**: Votes pour Dupont-Aignan
                    - **4: HOLLANDE**: Votes pour Hollande
                    - **5: JOLY**: Votes pour Joly
                    - **6: LE PEN**: Votes pour Le Pen
                    - **7: MELENCHON**: Votes pour Melenchon
                    - **8: POUTOU**: Votes pour Poutou
                    - **9: SARKOZY**: Votes pour Sarkozy
                    """)
        
    if slid == 2017:
        df=dfannee_2017
        st.bar_chart([df['DUPONT-AIGNAN'].sum(),df['LE PEN'].sum(),
                    df['MACRON'].sum(),df['HAMON'].sum(),df['ARTHAUD'].sum(),
                    df['POUTOU'].sum(),df['CHEMINADE'].sum(),df['LASSALLE'].sum(),
                    df['MÉLENCHON'].sum(),df['ASSELINEAU'].sum(),df['FILLON'].sum()])
        st.write("""
                    ### Légende
                    - **0: DUPONT-AIGNAN**: Votes pour Dupont-Aignan
                    - **1: LE PEN**: Votes pour Le Pen
                    - **2: MACRON**: Votes pour Macron
                    - **3: HAMON**: Votes pour Hamon
                    - **4: ARTHAUD**: Votes pour Arthaud
                    - **5: POUTOU**: Votes pour Poutou
                    - **6: CHEMINADE**: Votes pour Cheminade
                    - **7: LASSALLE**: Votes pour Lassalle
                    - **8: MÉLENCHON**: Votes pour Melenchon
                    - **9: ASSELINEAU**: Votes pour Asselineau
                    - **10: FILLON**: Votes pour Fillon
                    """)
        
    if slid == 2022:
        df=dfannee_2022
        st.bar_chart([df['ARTHAUD'].sum(),df['ROUSSEL'].sum(),
                    df['MACRON'].sum(),df['LE PEN'].sum(),df['ZEMMOUR'].sum(),
                    df['HIDALGO'].sum(),df['JADOT'].sum(),df['PÉCRESSE'].sum(),
                    df['POUTOU'].sum(),df['DUPONT-AIGNAN'].sum(),df['LASSALLE'].sum(),df['MÉLENCHON'].sum()])
        st.write("""
                    ### Légende
                    - **0: ARTHAUD**: Votes pour Arthaud
                    - **1: ROUSSEL**: Votes pour Roussel
                    - **2: MACRON**: Votes pour Macron
                    - **3: LE PEN**: Votes pour Le Pen
                    - **4: ZEMMOUR**: Votes pour Zemmour
                    - **5: HIDALGO**: Votes pour Hidalgo
                    - **6: JADOT**: Votes pour Jadot
                    - **7: PÉCRESSE**: Votes pour Pécresse
                    - **8: POUTOU**: Votes pour Poutou
                    - **9: DUPONT-AIGNAN**: Votes pour Dupont-Aignan
                    - **10: LASSALLE**: Votes pour Lassalle
                    - **11: MÉLENCHON**: Votes pour Melenchon
                    """)
    return slid

def geo_map_vote(df):
    m = folium.Map(location=[46.603354, 1.888334], min_zoom=6, max_zoom=6)
    gdf_departments = gpd.read_file("departements.geojson")
    gdf_departments = gdf_departments.merge(df, left_on='nom', right_on='Département')
    folium.GeoJson(gdf_departments,
                name="geojson_departments",
                style_function=lambda feature: {
                    'fillColor': feature['properties']['color'],
                    'color': 'black',
                    'weight': 1.5,
                    'fillOpacity': 0.7,
                },
                highlight_function=lambda x: {
                    'fillColor': 'white',
                    'color': 'black',
                    'weight': 3,
                    'fillOpacity': 0.7,
                },
                tooltip=folium.GeoJsonTooltip(fields=['nom'], labels=True, sticky=False)
                ).add_to(m)
    for index, row in gdf_departments.iterrows():
        department_name = row['nom']
        geojson_department = row['geometry']
        
        folium.GeoJson(geojson_department,
                    name=department_name,
                    style_function=lambda x: {'fillOpacity': 0},
                    highlight_function=lambda x: {'fillOpacity': 0.5},
                    tooltip=department_name,
                    ).add_to(m)
    folium_static(m)

def geo_map_vote2(df):
    gdf_departments = gpd.read_file("departements.geojson")
    gdf_departments = gdf_departments.merge(df, left_on='nom', right_on='Département')

    # Convert the GeoDataFrame to a GeoJSON data source for Bokeh
    geosource = GeoJSONDataSource(geojson=gdf_departments.to_json())

    # Create a new figure
    p = figure(title='Percentage of Votes by Department')

    # Add department geometries to the figure
    p.patches('xs', 'ys', source=geosource,
              fill_color='color',
              line_color='black',
              line_width=1.5,
              fill_alpha=0.7)

    # Add the Hover tool
    hover = HoverTool()
    hover.tooltips = [("Department", "@nom"),
                      ("Percentage of Votes", "@right_candidates"),
                      ("Percentage of Votes", "@left_candidates"),
                      ("Percentage of Votes", "@center_candidates")]
    p.add_tools(hover)

    return p

def barchart_plotly(df):
    fig = go.Figure(data=[
        go.Bar(name='Left', x=df['Département'], y=df['left_candidates'], marker=dict(color='red')),
        go.Bar(name='Right', x=df['Département'], y=df['right_candidates'], marker=dict(color='blue')),
        go.Bar(name='Center', x=df['Département'], y=df['center_candidates'], marker=dict(color='white'))
    ])
    fig.update_layout(barmode='group')
    st.plotly_chart(fig)

def piechart_plotly(df):
    colors = ['red', 'white', 'blue']
    sum_left, sum_right, sum_center = df['left_candidates'].sum(), df['right_candidates'].sum(), df['center_candidates'].sum()

    fig = go.Figure(data=[go.Pie(labels=['left', 'center', 'right'],
                                 values=[sum_left, sum_center, sum_right])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                      marker=dict(colors=colors))

    st.plotly_chart(fig) 

def show_data(df,slider_2):
    if slider_2 == 2012:
        df = df.drop(['color','Code du département'], axis=1)
        cols = ['Département'] + [col for col in df.columns if col != 'Département']
        df = df[cols]
        df

    if slider_2 == 2017:
        df = df.drop(['color','Code du département'], axis=1)
        df
    if slider_2 == 2022:
        df = df.drop(['color','Code du département','Inscrits','Abstentions','Votants','Blancs','Nuls','Exprimés','ARTHAUD_% Voix/Exp',
                      'ROUSSEL_% Voix/Exp','MACRON_% Voix/Exp','LASSALLE_% Voix/Exp','LE PEN_% Voix/Exp','ZEMMOUR_% Voix/Exp','MÉLENCHON_% Voix/Exp',
                      'HIDALGO_% Voix/Exp','JADOT_% Voix/Exp','PÉCRESSE_% Voix/Exp','POUTOU_% Voix/Exp','DUPONT-AIGNAN_% Voix/Exp'], axis=1)
        df

def chooser(option,dfannee_2012,dfannee_2017,dfannee_2022):
    colors = ['Maroon', 'red', 'white', '#0087FF', 'blue']
    col1,col2,col3 = st.columns(3)
    st.header("2012")
    dfannee_2012[dfannee_2012["Département"] == option][['Département','ARTHAUD', 'BAYROU', 'CHEMINADE',
       'DUPONT-AIGNAN', 'HOLLANDE', 'JOLY', 'LE PEN', 'MELENCHON', 'POUTOU',
       'SARKOZY',  'left_candidates', 'right_candidates',
       'center_candidates']]
    sum_extrem_left,sum_left,sum_center,sum_right,sum_extrem_right= dfannee_2012[dfannee_2022["Département"] == option][['ARTHAUD','POUTOU','MELENCHON']].sum().sum(),dfannee_2012[dfannee_2022["Département"] == option][['JOLY','HOLLANDE']].sum().sum(),dfannee_2012[dfannee_2022["Département"] == option]['BAYROU'].sum(),dfannee_2012[dfannee_2022["Département"] == option]['SARKOZY'].sum(),dfannee_2012[dfannee_2022["Département"] == option][['LE PEN', 'CHEMINADE']].sum().sum()
    fig = go.Figure(data=[go.Pie(labels=['extrem_left', 'left', 'center', 'right', 'extrem_right'],
                                     values=[sum_extrem_left, sum_left, sum_center, sum_right, sum_extrem_right])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=colors))
    st.plotly_chart(fig)

    st.header("2017")
    dfannee_2017[dfannee_2017["Département"] == option][['Département', 'DUPONT-AIGNAN',
       'LE PEN', 'MACRON', 'HAMON', 'ARTHAUD', 'POUTOU', 'CHEMINADE',
       'LASSALLE', 'MÉLENCHON', 'ASSELINEAU', 'FILLON', 'left_candidates',
       'right_candidates', 'center_candidates']]
    sum_extrem_left,sum_left,sum_center,sum_right,sum_extrem_right= dfannee_2017[dfannee_2022["Département"] == option][['ARTHAUD','POUTOU','MÉLENCHON']].sum().sum(),dfannee_2017[dfannee_2022["Département"] == option]['HAMON'].sum(),dfannee_2017[dfannee_2022["Département"] == option][['MACRON','ASSELINEAU']].sum().sum(),dfannee_2017[dfannee_2022["Département"] == option][['LASSALLE','FILLON']].sum().sum(),dfannee_2017[dfannee_2022["Département"] == option][['LE PEN', 'CHEMINADE','LASSALLE']].sum().sum()
    fig = go.Figure(data=[go.Pie(labels=['extrem_left', 'left', 'center', 'right', 'extrem_right'],
                                     values=[sum_extrem_left, sum_left, sum_center, sum_right, sum_extrem_right])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=colors))
    st.plotly_chart(fig)

    st.header("2022")
    dfannee_2022[dfannee_2022["Département"] == option][['Département','ARTHAUD',
        'ROUSSEL', 'MACRON',
       'LASSALLE',  'LE PEN',
        'ZEMMOUR',  'MÉLENCHON',
        'HIDALGO',  'JADOT',
        'PÉCRESSE',  'POUTOU',
        'DUPONT-AIGNAN', 
       'left_candidates', 'right_candidates', 'center_candidates']]
    colors = ['Maroon', 'red', 'white', '#0087FF', 'blue']
    sum_extrem_left,sum_left,sum_center,sum_right,sum_extrem_right= dfannee_2022[dfannee_2022["Département"] == option][['ARTHAUD','POUTOU','MÉLENCHON','ROUSSEL']].sum().sum(),dfannee_2022[dfannee_2022["Département"] == option][['HIDALGO','JADOT']].sum().sum(),dfannee_2022[dfannee_2022["Département"] == option]['MACRON'].sum(),dfannee_2022[dfannee_2022["Département"] == option][['LASSALLE','PÉCRESSE']].sum().sum(),dfannee_2022[dfannee_2022["Département"] == option][['LE PEN', 'DUPONT-AIGNAN']].sum().sum()
    fig = go.Figure(data=[go.Pie(labels=['extrem_left', 'left', 'center', 'right', 'extrem_right'],
                                     values=[sum_extrem_left, sum_left, sum_center, sum_right, sum_extrem_right])])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=colors))
    st.plotly_chart(fig)

def sidebar_menu():
    with st.sidebar:
        st.title('Annalyse of 2012, 2017, and 2022 presidential election')
        st.write('app by Calvin Ndoumbe')
        add_radio = st.write('LinkedIn: https://www.linkedin.com/in/c-ndm/')

def app():
    sidebar_menu()
    st.subheader('Discover the data',divider='gray')
    dfannee_2012 = pd.read_csv("2012_cleared.csv", delimiter=',')
    dfannee_2017 = pd.read_csv("2017_cleared.csv", delimiter=',')
    dfannee_2022 = pd.read_csv("2022_cleared.csv", delimiter=',')
    on3 = st.toggle('watch dataset 2022')
    if on3:
        st.write('Dataframe 2022')
        show_data(dfannee_2022,2022)
    on4 = st.toggle('watch dataset 2017')
    if on4:
        st.write('Dataframe 2017')
        show_data(dfannee_2022,2017)
    on5 = st.toggle('watch dataset 2012')
    if on5:
        st.write('Dataframe 2012')
        show_data(dfannee_2022,2012)
    slider_annee(dfannee_2012,dfannee_2017,dfannee_2022)
    df = pd.DataFrame({
        'année': [2012, 2017, 2022],
        'votes': [sum([dfannee_2012['ARTHAUD'].sum(),dfannee_2012['HOLLANDE'].sum(),
                        dfannee_2012['JOLY'].sum(),dfannee_2012['MELENCHON'].sum(),dfannee_2012['POUTOU'].sum(),
                        dfannee_2012['CHEMINADE'].sum(),dfannee_2012['DUPONT-AIGNAN'].sum(),dfannee_2012['LE PEN'].sum(),
                        dfannee_2012['BAYROU'].sum()])
                ,sum([dfannee_2017['HAMON'].sum(),dfannee_2017['ARTHAUD'].sum(),
                        dfannee_2017['POUTOU'].sum(),dfannee_2017['MÉLENCHON'].sum(),dfannee_2017['LE PEN'].sum(),
                        dfannee_2017['DUPONT-AIGNAN'].sum(),dfannee_2017['CHEMINADE'].sum(),dfannee_2017['LASSALLE'].sum(),
                        dfannee_2017['MACRON'].sum()])
                ,sum([dfannee_2022['ARTHAUD'].sum(),dfannee_2022['ROUSSEL'].sum(),
                        dfannee_2022['MACRON'].sum(),dfannee_2022['LE PEN'].sum(),dfannee_2022['ZEMMOUR'].sum(),
                        dfannee_2022['HIDALGO'].sum(),dfannee_2022['JADOT'].sum(),dfannee_2022['PÉCRESSE'].sum(),
                        dfannee_2022['POUTOU'].sum(),dfannee_2022['DUPONT-AIGNAN'].sum()])]})
    st.header('Number of voters in Line',divider='gray')
    st.write('We can see that the number of voters is decreasing in 2022')
    on2 = st.toggle('Watch number of voters in Scatter')
    st.write('We can observe that less and less people are voting')
    st.line_chart(df.set_index('année')['votes']) 
    if on2:
        st.write("We can't really a great representation of the number of people who voted in these year")
        st.scatter_chart(df.set_index('année')['votes'])  
    slider_2 = st.select_slider(
        'Select a year to plot',
        options=[2012,2017,2022])
    st.title("Votes by different parties during the year{}".format(slider_2)) 
    
    if slider_2 == 2012:
            piechart_plotly(dfannee_2012)
    elif slider_2 == 2017:
            piechart_plotly(dfannee_2017)
    elif slider_2 == 2022:
            piechart_plotly(dfannee_2022)
    else:
            piechart_plotly(dfannee_2012)

    if slider_2 == 2012:
            barchart_plotly(dfannee_2012)
    elif slider_2 == 2017:
            barchart_plotly(dfannee_2017)
    elif slider_2 == 2022:
            barchart_plotly(dfannee_2022)
    else:
            barchart_plotly(dfannee_2012)
    st.subheader(" Map of the votes by department in {}".format(slider_2),divider='gray')
    on6 = st.toggle('Visualize the map wit results')
    if slider_2 == 2012:
        if on6: 
            st.bokeh_chart(geo_map_vote2(dfannee_2012), use_container_width=True)
        else:
            geo_map_vote(dfannee_2012)
    elif slider_2 == 2017:
        if on6:
            st.bokeh_chart(geo_map_vote2(dfannee_2017), use_container_width=True)
        else:
            geo_map_vote(dfannee_2017)
    elif slider_2 == 2022:
        if on6:
            st.bokeh_chart(geo_map_vote2(dfannee_2022), use_container_width=True)
        else:
            geo_map_vote(dfannee_2022)
    st.subheader("Detailed analyse on extrems {}".format(slider_2),divider='gray')
    colors = ['Maroon', 'red', 'white', '#0087FF', 'blue']
    if slider_2 == 2012:
        sum_extrem_left,sum_left,sum_center,sum_right,sum_extrem_right= dfannee_2012[['ARTHAUD','POUTOU','MELENCHON']].sum().sum(),dfannee_2012[['JOLY','HOLLANDE']].sum().sum(),dfannee_2012['BAYROU'].sum(),dfannee_2012['SARKOZY'].sum(),dfannee_2012[['LE PEN', 'CHEMINADE']].sum().sum()
        fig = go.Figure(data=[go.Pie(labels=['extrem_left', 'left', 'center', 'right', 'extrem_right'],
                                     values=[sum_extrem_left, sum_left, sum_center, sum_right, sum_extrem_right])])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=colors))
        st.plotly_chart(fig)   
    elif slider_2 == 2017:
        sum_extrem_left,sum_left,sum_center,sum_right,sum_extrem_right= dfannee_2017[['ARTHAUD','POUTOU','MÉLENCHON']].sum().sum(),dfannee_2017['HAMON'].sum(),dfannee_2017[['MACRON','ASSELINEAU']].sum().sum(),dfannee_2017[['LASSALLE','FILLON']].sum().sum(),dfannee_2017[['LE PEN', 'CHEMINADE','LASSALLE']].sum().sum()
        fig = go.Figure(data=[go.Pie(labels=['extrem_left', 'left', 'center', 'right', 'extrem_right'],
                                     values=[sum_extrem_left, sum_left, sum_center, sum_right, sum_extrem_right])])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=colors))
        st.plotly_chart(fig)  
    elif slider_2 == 2022:
        sum_extrem_left,sum_left,sum_center,sum_right,sum_extrem_right= dfannee_2022[['ARTHAUD','POUTOU','MÉLENCHON','ROUSSEL']].sum().sum(),dfannee_2022[['HIDALGO','JADOT']].sum().sum(),dfannee_2022['MACRON'].sum(),dfannee_2022[['LASSALLE','PÉCRESSE']].sum().sum(),dfannee_2022[['LE PEN', 'DUPONT-AIGNAN']].sum().sum()
        fig = go.Figure(data=[go.Pie(labels=['extrem_left', 'left', 'center', 'right', 'extrem_right'],
                                     values=[sum_extrem_left, sum_left, sum_center, sum_right, sum_extrem_right])])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                           marker=dict(colors=colors))
        st.plotly_chart(fig)
    st.subheader("Detailed analyse on departement {}".format(slider_2),divider='gray')
    option = st.selectbox('what departement do you want to watch',(dfannee_2022["Département"].unique()))
    chooser(option,dfannee_2012,dfannee_2017,dfannee_2022)


    st.subheader('Documentation :',divider='gray')
    st.write("dataset 2012: https://www.data.gouv.fr/fr/datasets/election-presidentielle-2012-resultats-par-bureaux-de-vote-1/#/community-resources")
    st.write("dataset 2017: https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-23-avril-et-7-mai-2017-resultats-definitifs-du-1er-tour-par-bureaux-de-vote/#/community-resources")
    st.write("dataset 2022: https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/#/community-resources")

app()




