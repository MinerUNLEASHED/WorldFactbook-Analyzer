import numpy as np
import pandas as pd
import plotly.express as px
import plotly as plotly
from fractions import Fraction

country_iso_data = pd.read_csv('data_processing\country_code_data.csv')
# print(country_iso_data.columns)
# print()
# print(country_iso_data['Afghanistan'])
# print(type(country_iso_data['Country'][1]))



def graph_maker_function(type_of_graph):
    type_of_graph = type_of_graph.upper()
    data_set_for_graph = pd.DataFrame(columns=['ISO', 'Year', 'Country', f'{type_of_graph}'])
    current_data_set = pd.read_csv(f'data_processing/{type_of_graph.lower()}.csv', sep=';')[['name', 'value']]
    past_data_set = pd.read_csv(f'Data/Current Data/{type_of_graph.lower()}.csv',sep=',')[['Country','Value','Year']]
    print(current_data_set.head)
    
    for row in current_data_set.itertuples():
        # row_count = 0
        current_country = row[1]
        if current_country in country_iso_data.Country.values:
            current_row = country_iso_data.loc[country_iso_data['Country']==current_country].index[0]
            # print(type(int(row[2].replace(',',''))))
            try:
                current_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                          'Year': 2023,
                                        'Country': current_country, 
                                        f'{type_of_graph}':int(row[2].replace(',',''))})
                extra_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                          'Year': 2022,
                                        'Country': current_country,
                                        f'{type_of_graph}':int(row[2].replace(',',''))})
            except AttributeError:
                current_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                          'Year': 2023,
                                        'Country': current_country, 
                                        f'{type_of_graph}':row[2]})
                extra_data = pd.Series({'ISO': country_iso_data.loc[current_row, 'ISO'],
                                        'Year': 2022,
                                        'Country': current_country,
                                        f'{type_of_graph}':row[2]})
             # type: ignore
            # data_set_for_graph.index = data_set_for_graph.index + 1
            # data_set_for_graph = data_set_for_graph.sort_index()
            data_set_for_graph = pd.concat([data_set_for_graph, extra_data.to_frame().T])
            data_set_for_graph = pd.concat([data_set_for_graph, current_data.to_frame().T])
            data_set_for_graph[f'{type_of_graph}'] = data_set_for_graph[f'{type_of_graph}'].astype(float)
            data_set_for_graph['Year'] = data_set_for_graph['Year'].astype(int)
            # row_count += 1
    # print(data_set_for_graph)

    fig = px.choropleth(data_set_for_graph, locations='ISO', color=f'{type_of_graph}',
                        hover_name='Country', hover_data=[f'{type_of_graph}'],
                        projection='natural earth', title=f'{type_of_graph} by Country'.upper(),
                        animation_frame='Year',
                        # color_continuous_scale=px.colors.diverging.BrBG, color_continuous_midpoint=4000000000000
                        )

    plotly.offline.plot(fig, filename=f'main_view/templates/test_view/{type_of_graph.lower()}.html', auto_open=True)

graph_maker_function('area')

