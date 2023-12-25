import pandas as pd
import plotly.express as px
import plotly as plotly
import os

cw_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(cw_dir)
# data_dir = os.path.join(parent_dir, 'Data')
# current_data_dir = os.path.join(data_dir, 'Current Data')
# past_data_dir = os.path.join(data_dir, 'Past Data')

main_view_dir = os.path.join(parent_dir, 'main_view')
templates_dir = os.path.join(main_view_dir, 'templates')
test_view_dir = os.path.join(templates_dir, 'test_view')

country_iso_data = pd.read_csv(os.path.join(cw_dir, 'country_code_data.csv'))

# (os.path.join(current_data_dir,fr'{type_of_graph.lower()}.csv'))
# (os.path.join(past_data_dir,fr'{type_of_graph.lower()}-past.csv'))

def graph_maker_function(type_of_graph):
    type_of_graph = type_of_graph.upper()
    data_set_for_graph = pd.DataFrame(columns=['ISO', 'Year', 'Country', f'{type_of_graph}'])
    current_data_set = pd.read_csv(fr"https://f005.backblazeb2.com/file/World-Factbook-Analyzer/Current+Data/{type_of_graph.lower()}.csv",usecols=[0,2])
    past_data_set = pd.read_csv(fr"https://f005.backblazeb2.com/file/World-Factbook-Analyzer/Past+Data/{type_of_graph.lower()}-past.csv", usecols=['Country','Value','Year'])

    for row in current_data_set.itertuples():
        current_country = row[1]

        if current_country in country_iso_data.Country.values:
            current_row = country_iso_data.loc[country_iso_data['Country']==current_country].index[0].astype(int)
            past_data_rows = list(past_data_set.loc[past_data_set['Country']==current_country].index)

            try:
                current_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                          'Year': 2023,
                                          'Country': current_country,
                                          f'{type_of_graph}':int(row[2].replace(',','').replace('$',''))})

            except AttributeError:
                current_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                          'Year': 2023,
                                        'Country': current_country,
                                        f'{type_of_graph}':(row[2])})
            except ValueError:
                current_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                          'Year': 2023,
                                        'Country': current_country,
                                        f'{type_of_graph}':float(row[2])})



            data_set_for_graph = pd.concat([data_set_for_graph, current_data.to_frame().T])

            for row_val in past_data_rows:
                try:
                    current_extra_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                              'Year': past_data_set.loc[row_val, 'Year'],
                                              'Country': current_country,
                                              f'{type_of_graph}':int((past_data_set.loc[row_val,'Value']).replace(',','').replace('$',''))})
                except AttributeError:
                    current_extra_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                              'Year': past_data_set.loc[row_val, 'Year'],
                                              'Country': current_country,
                                              f'{type_of_graph}':(past_data_set.loc[row_val,'Value'])})
                except ValueError:
                    current_extra_data = pd.Series({'ISO':country_iso_data.loc[current_row, 'ISO'],
                                              'Year': past_data_set.loc[row_val, 'Year'],
                                              'Country': current_country,
                                              f'{type_of_graph}':float(past_data_set.loc[row_val,'Value'])})


                data_set_for_graph = pd.concat([data_set_for_graph, current_extra_data.to_frame().T])

            data_set_for_graph['ISO'] = data_set_for_graph['ISO'].astype(str)
            data_set_for_graph[f'{type_of_graph}'] = data_set_for_graph[f'{type_of_graph}'].astype(float)

            try:
                data_set_for_graph['Year'] = data_set_for_graph['Year'].astype(int)
            except:
                pass

            data_set_for_graph = data_set_for_graph.sort_values('Year')


    title = f'{type_of_graph} by Country, {get_units()[allowed_data().index(type_of_graph.lower())]}'.upper()


    fig = px.choropleth(data_set_for_graph, locations='ISO', color=f'{type_of_graph}',
                        hover_name='Country', hover_data=[f'{type_of_graph}'],
                        projection='natural earth', title=title,
                        animation_frame='Year',
                        color_continuous_scale='jet', color_continuous_midpoint=(data_set_for_graph[f'{type_of_graph}'].max()/2),
                        range_color=[(data_set_for_graph[f'{type_of_graph}'].min()),(data_set_for_graph[f'{type_of_graph}'].max())],
                        animation_group='ISO'
                        )

    file_path = os.path.join(test_view_dir,fr'{type_of_graph.lower()}.html')

    plotly.offline.plot(fig, filename=file_path, auto_open=False)

    with open(file_path, 'r', encoding='macroman') as file:
        lines = file.readlines()


    lines[:3] = ['{% extends "test_view/base.html" %}\n{% block content %}\n']
    lines[-2:] = ['{% endblock %}\n']


    with open(file_path, 'w', encoding='MacRoman') as file:
        file.writelines(lines)


def allowed_data():
    with open((os.path.join(cw_dir, r'data.txt')), 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    return lines

def allowed_data_stripped():
    return [value.replace(',', '').upper() for value in allowed_data()]

def get_units():
    with open((os.path.join(cw_dir,r'data_rep.txt')), 'r') as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    return lines


# graph_maker_function("area")






















