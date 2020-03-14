import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import re
import plotly.express as px
from dash.dependencies import Input, Output
#from app import app
# reading dataframe
competitor_data=pd.read_csv('competitors_data.csv')
competitor_data.drop(columns=['Unnamed: 0'],inplace=True)
competitor_data.reset_index(drop=True,inplace=True)
competitor_data = competitor_data[['homestay_name', 'area','region','place', 'price', 'amenities']]
competitor_data.area=competitor_data.area.apply(lambda x:x.strip())
competitor_data.region=competitor_data.region.apply(lambda x:x.strip())
competitor_data.place=competitor_data.place.apply(lambda x:x.strip())
competitor_data.price=competitor_data.price.apply(lambda x:re.sub('[^0-9]','',x))
competitor_data.price=competitor_data.price.apply(lambda x:int(x))
# data cleaning trip thrills
trip_thrills_data=pd.read_csv('homestays_trip_thrills.csv')
trip_thrills_data.drop(columns=['Unnamed: 0'],inplace=True)
trip_thrills_data.area=trip_thrills_data.area.fillna('unknown')
trip_thrills_data.area=trip_thrills_data.area.apply(lambda x:x.strip())
trip_thrills_data.region=trip_thrills_data.region.fillna('unknown')
trip_thrills_data.region=trip_thrills_data.region.apply(lambda x:x.strip())
trip_thrills_data=trip_thrills_data.reset_index().rename(columns={'index':'hotel_id'})
trip_thrills_data=trip_thrills_data[['hotel_id','area','region','homestay_name','price']]


# Analysis
competitor_data_analysis=pd.read_csv('competitors_data.csv')
competitor_data_analysis.drop(columns=['Unnamed: 0'],inplace=True)
competitor_data_analysis.reset_index(drop=True,inplace=True)
competitor_data_analysis = competitor_data_analysis[['homestay_name', 'area','region','place', 'price', 'amenities']]
competitor_data_analysis.area=competitor_data_analysis.area.apply(lambda x:x.strip())
competitor_data_analysis.region=competitor_data_analysis.region.apply(lambda x:x.strip())
competitor_data_analysis.place=competitor_data_analysis.place.apply(lambda x:x.strip())
competitor_data_analysis.price=competitor_data_analysis.price.apply(lambda x:re.sub('[^0-9]','',x))
competitor_data_analysis.price=competitor_data_analysis.price.apply(lambda x:int(x))
competitor_data_analysis.amenities=competitor_data_analysis.amenities.apply(lambda x:eval(x))
# getting rid of the extra space
competitors_amenities=[]
for i in competitor_data_analysis.amenities:
    individual_element=[]
    for j in i:
        individual_element.append(j.strip())
    competitors_amenities.append(individual_element)
competitor_data_analysis.amenities=competitors_amenities

trip_thrills_data_analysis=pd.read_csv('homestays_trip_thrills.csv')
trip_thrills_data_analysis.drop(columns=['Unnamed: 0'],inplace=True)
trip_thrills_data_analysis.area=trip_thrills_data_analysis.area.fillna('unknown')
trip_thrills_data_analysis.area=trip_thrills_data_analysis.area.apply(lambda x:x.strip())
trip_thrills_data_analysis.region=trip_thrills_data_analysis.region.fillna('unknown')
trip_thrills_data_analysis.region=trip_thrills_data_analysis.region.apply(lambda x:x.strip())
trip_thrills_data_analysis.amenities=trip_thrills_data_analysis.amenities.apply(lambda x:eval(x))
# getting rid of the extra space
trip_thrills_amenities=[]
for i in trip_thrills_data_analysis.amenities:
    individual_element=[]
    for j in i:
        individual_element.append(j.strip())
    trip_thrills_amenities.append(individual_element)
trip_thrills_data_analysis.amenities=trip_thrills_amenities
        

all_amenities_trip_thrills=[]
for i in trip_thrills_data_analysis.amenities:
    for j in (i):
        all_amenities_trip_thrills.append(j)

all_amenities_competitors=[]
for i in competitor_data_analysis.amenities:
    for j in (i):
        all_amenities_competitors.append(j)


# Filtering competitor data based on filteration on excel 
amenities_to_consider_competitor=pd.read_csv('amenities_competitor filter.csv',encoding='utf-8',header=None).rename(columns={0:'amenities'})

competitors_amenities=[]
for i in competitor_data_analysis.amenities:
    individual_element=[]
    for j in i:
        individual_element=[j for j in i if j in list(amenities_to_consider_competitor.amenities)]
    competitors_amenities.append(individual_element)

competitor_data_analysis.amenities=competitors_amenities

amenities_to_consider_trip_thrills=pd.read_csv('amenities_trip_thrills filter.csv',encoding='utf-8',header=None).rename(columns={0:'amenities'})

all_amenities_trip_thrills=[]
for i in trip_thrills_data_analysis.amenities:
    individual_element=[]
    for j in i:
        individual_element=[j for j in i if j in list(amenities_to_consider_trip_thrills.amenities)]
    all_amenities_trip_thrills.append(individual_element)

trip_thrills_data_analysis.amenities=all_amenities_trip_thrills


mapping_file=pd.read_csv('mapping.csv')

mapping_file=dict(zip(mapping_file['original '], mapping_file.mapped))

all_amenities_competitors_replaced=[]
for i in competitor_data_analysis.amenities:
    individual_element=[]
    for j in (i):
        if j in list(mapping_file.keys()):
            individual_element.append(mapping_file[j])
    all_amenities_competitors_replaced.append(list(set(individual_element)))

competitor_data_analysis.amenities=all_amenities_competitors_replaced

all_amenities_tripthrills_replaced=[]
for i in trip_thrills_data_analysis.amenities:
    individual_element=[]
    for j in (i):
        if j in list(mapping_file.keys()):
            individual_element.append(mapping_file[j])
    all_amenities_tripthrills_replaced.append(list(set(individual_element)))

trip_thrills_data_analysis.amenities=all_amenities_tripthrills_replaced

def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

competitor_data_analysis=competitor_data_analysis.reset_index().rename(columns={'index':'hotel_id'})
trip_thrills_data_analysis=trip_thrills_data_analysis.reset_index().rename(columns={'index':'hotel_id'})

competitor_data_analysis['price_type']=competitor_data_analysis['price'].apply(lambda x:'luxury' if x>15000 else 'comfort' if x>5000 else 'budget')
trip_thrills_data_analysis['price_type']=trip_thrills_data_analysis['price'].apply(lambda x:'luxury' if x>15000 else 'comfort' if x>5000 else 'budget')

competitor_id=[]
trip_thrills_id=[]
for i in competitor_data_analysis['hotel_id']:
    for j in trip_thrills_data_analysis['hotel_id']:
        competitor_id.append(i)
        trip_thrills_id.append(j)
        

same_area=[]
same_region=[]
same_pricing=[]
for i in competitor_data_analysis['hotel_id']:
    for j in trip_thrills_data_analysis['hotel_id']:
        same_area.append(competitor_data_analysis.loc[(competitor_data_analysis.hotel_id==i),'area'].values[0]==trip_thrills_data_analysis.loc[(trip_thrills_data_analysis.hotel_id==j),'area'].values[0])
        same_region.append(competitor_data_analysis.loc[(competitor_data_analysis.hotel_id==i),'region'].values[0]==trip_thrills_data_analysis.loc[(trip_thrills_data_analysis.hotel_id==j),'region'].values[0])
        same_pricing.append(competitor_data_analysis.loc[(competitor_data_analysis.hotel_id==i),'price_type'].values[0]==trip_thrills_data_analysis.loc[(trip_thrills_data_analysis.hotel_id==j),'price_type'].values[0])


## Getting hotel similarity
similarity_score=[]
for i in competitor_data_analysis['hotel_id']:
    for j in trip_thrills_data_analysis['hotel_id']:
        similarity_score.append(jaccard_similarity(competitor_data_analysis.loc[(competitor_data_analysis.hotel_id==i),'amenities'].values[0],trip_thrills_data_analysis.loc[(trip_thrills_data_analysis.hotel_id==j),'amenities'].values[0]))

similarity_score_table=pd.DataFrame(list(zip(competitor_id,trip_thrills_id,similarity_score,same_area,same_region,same_pricing))).rename(columns={0:'competitor hotel id',1:'trip thrills hotel id',2:'similarity score',3:'same_area',4:'same_region',5:'same_pricing'})

def similar_hotel_details(hotel_id):
    if(len(similarity_score_table[(similarity_score_table['trip thrills hotel id']==hotel_id) & (similarity_score_table['same_region']==True) & (similarity_score_table['same_pricing']==True)].sort_values(by='similarity score',ascending=False)['competitor hotel id'])<5):
        return 'Not Enough Data To Compare'
    else:
        return similarity_score_table[(similarity_score_table['trip thrills hotel id']==hotel_id) & (similarity_score_table['same_region']==True) & (similarity_score_table['same_pricing']==True)].sort_values(by='similarity score',ascending=False)['competitor hotel id'][0:5]

# Frontend
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([
                       html.H1('Analysis',style={'textAlign': 'center','overflow':'hidden',
  'background-color':'#1F77b4',
  'color':'#FFFFFF',
  'padding': '20px 20px'
}),
 html.Hr(),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i.capitalize(), "id": i} for i in trip_thrills_data.columns],
    data=trip_thrills_data.to_dict('records'),
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
    },
    style_cell_conditional=[
            {'if': {'column_id': 'hotel_id'},
         'width': '10%'},
         {'if': {'column_id': 'homestay_name'},
         'width': '60%','textAlign': 'center'},
        {'if': {'column_id': 'area'},
         'width': '10%','textAlign': 'center'},
        {'if': {'column_id': 'region'},
         'width': '10%','textAlign': 'center'},
          {'if': {'column_id': 'price'},
         'width': '10%','textAlign': 'center'}
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': '#1F77b4',
        'fontWeight': 'bold',
         'fontSize': 16,
         'color':'white',
         'textAlign': 'center'
         
    },
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    column_selectable="single",
    row_selectable="single",
    row_deletable=False,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current= 0,
    page_size= 10,
),
    html.Br(),
    html.Br(),
    html.Hr(),
html.Div(id='output_table')
    
    
      ])


@app.callback(
    Output(component_id='output_table', component_property='children'),
    [Input(component_id='table',component_property='selected_rows')]
)
def update_output_div(selected_rows):
    if len(selected_rows)==0:
        return 'No hotel selected'
    else:
        table_to_return=competitor_data_analysis[competitor_data_analysis['hotel_id'].isin(list(similar_hotel_details((selected_rows[0])).values))]
        extra_amenities_competitor=[]
        for i in table_to_return.amenities:
            extra_amenities_competitor.append(list(set(set(i)-set(trip_thrills_data_analysis.loc[trip_thrills_data_analysis.hotel_id==selected_rows[0],'amenities'][selected_rows[0]]))))
        table_to_return['required_amenities']=extra_amenities_competitor 
        table_to_return['required_amenities']=table_to_return['required_amenities'].apply(lambda x:str(x))
        table_to_return=table_to_return.loc[:,table_to_return.columns.isin(['homestay_name','area','region','price','price_type','required_amenities'])]
        
        return dash_table.DataTable(
    columns=[{"name": i.capitalize(), "id": i} for i in table_to_return.columns],
    data=table_to_return.to_dict('records'),
    style_cell={
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'maxWidth': 0,
    },
    style_cell_conditional=[
            {'if': {'column_id': 'price_type'},
         'width': '10%'},
         {'if': {'column_id': 'homestay_name'},
         'width': '30%','textAlign': 'center'},
        {'if': {'column_id': 'area'},
         'width': '10%','textAlign': 'center'},
        {'if': {'column_id': 'region'},
         'width': '10%','textAlign': 'center'},
          {'if': {'column_id': 'price'},
         'width': '10%','textAlign': 'center'},
          {'if': {'column_id': 'required_amenities'},
         'width': '30%','textAlign': 'center'} 
           
          
    ],
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': '#1F77b4',
        'fontWeight': 'bold',
         'fontSize': 16,
         'color':'white',
         'textAlign': 'center'
         
    },
    editable=True,
    filter_action="native",
    sort_action="native",
    sort_mode="multi",
    row_deletable=False,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current= 0,
    page_size= 10,
)
#
if __name__ == '__main__':
    app.run_server(debug=True)
