import dash
import dash_table
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
#from app import app
# reading dataframe
similarity_score_table=pd.read_csv('similarity_score_table.csv')
trip_thrills_data=pd.read_csv('trip_thrills_data.csv')
trip_thrills_data.drop(columns=['Unnamed: 0'],inplace=True)
competitor_data_analysis=pd.read_csv('competitor_data_analysis.csv')
trip_thrills_data_analysis=pd.read_csv('trip_thrills_data_analysis.csv')
trip_thrills_data_analysis.amenities=trip_thrills_data_analysis.amenities.apply(lambda x:eval(x))
competitor_data_analysis.amenities=competitor_data_analysis.amenities.apply(lambda x:eval(x))
def similar_hotel_details(hotel_id):
    if(len(similarity_score_table[(similarity_score_table['trip thrills hotel id']==hotel_id) & (similarity_score_table['same_region']==True) & (similarity_score_table['same_pricing']==True)].sort_values(by='similarity score',ascending=False)['competitor hotel id'])<5):
        return 'Not Enough Data To Compare'
    else:
        return similarity_score_table[(similarity_score_table['trip thrills hotel id']==hotel_id) & (similarity_score_table['same_region']==True) & (similarity_score_table['same_pricing']==True)].sort_values(by='similarity score',ascending=False)['competitor hotel id'][0:5]

# Frontend
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app=dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server
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
    app.run_server(debug=False)
