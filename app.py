import numpy as np
import statsmodels
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
# from jupyter_dash import JupyterDash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                  encoding='cp1252', 
                  na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                             'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"],
                  low_memory=False)

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

para_1 = '''According to the report available at the website given by the link 'https://www.gao.gov/products/gao-23-106041', Women earned an estimated 82 cents for every dollar that men earned which is a an overall gap of 18 cents on a dollar. The gender pay gap varies a lot based on the many factors including job designation, sectors (private, government, etc.), level of education, racial and ethnic job places. This variation is as per the Published Census Bureau data for 2021. '''


para_2 = '''The GSS conducts surveys of adults in the United States related to opinions, attitudes, behavior of contemporary American society. It collects data using these surveys and is the best source for demographic, civil affairs, sociological and attitudinal data covering the United States. The GSS has been conduting these surveys since 1972 and it also uses  questions from earlier surveys, which allows comparisons up to last 80 years. The GSS scientifically selects its survey participants to make sure that 
the every section of the country is represented. '''

table_data_2 = gss_clean[['income', 'job_prestige', 'socioeconomic_index', 'education', 'sex']].\
    groupby('sex').mean().round(2).reset_index()

table_data_2 = ff.create_table(table_data_2)


table_data_3 = gss_clean[['id', 'sex', 'male_breadwinner']].groupby(['sex', 'male_breadwinner']).count().reset_index()
table_data_3 = table_data_3.rename({'id':'count'}, axis = 1)

figure_3 = px.bar(table_data_3, x='male_breadwinner', y='count', color='sex',
              labels={'male_breadwinner':'Level of Agreement with Male Breadwinner Question', 'count':'Number of People'},
              hover_data = ['male_breadwinner'],
              text='male_breadwinner',
              barmode = 'group')

figure_3.update_layout(showlegend=True)
figure_3.update(layout=dict(title=dict(x=0.5)))


table_data_4 = gss_clean[['sex', 'job_prestige', 'income', 'education', 'socioeconomic_index']]

figure_4 = px.scatter(table_data_4, x='job_prestige', y='income', 
                  color = 'sex', 
                  trendline='ols',
                  height=600, width=600,
                  labels={'job_prestige':'Occupational Prestige Score', 
                          'income':'Annual Income'},
                  hover_data=['job_prestige', 'income', 'socioeconomic_index', 'education'])

figure_4.update(layout=dict(title=dict(x=0.5)))


table_data_5_income = gss_clean[['sex', 'income']]

figure_5_income = px.box(table_data_5_income, x='income', y = 'sex', color = 'sex', 
                     labels={'income':'Annual Income', 'sex':''})

figure_5_income.update(layout=dict(title=dict(x=0.5)))
figure_5_income.update_layout(showlegend=False)


table_data_5_prestige = gss_clean[['sex', 'job_prestige']]

figure_5_prestige = px.box(table_data_5_prestige, x='job_prestige', y = 'sex', color = 'sex',
                       labels={'job_prestige':'Occupational Prestige Score', 'sex':''})

figure_5_prestige.update(layout=dict(title=dict(x=0.5)))
figure_5_prestige.update_layout(showlegend=False)


table_data_6 = gss_clean[['income', 'sex', 'job_prestige']]

table_data_6['job_prestige_group'] = pd.cut(table_data_6.job_prestige, 
                                      bins = 6, 
                                      labels=("1 Very Low", "2 Low", "3 Medium", 
                                              "4 High", "5 Very High", "6 Super High"))
table_data_6 = table_data_6.dropna()

table_data_6 = table_data_6.sort_values('job_prestige_group')


figure_6 = px.box(table_data_6, x = 'income', y = 'sex', color = 'sex', 
              facet_col='job_prestige_group', facet_col_wrap=2,
              color_discrete_map = {'male':'blue', 'female':'red'},
              labels={'income':'Annual', 'sex':''})

figure_6.update(layout=dict(title=dict(x=0.5)))
figure_6.update_layout(showlegend=False)

bar_columns = ['satjob', 'relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer', 'men_overwork'] 
group_columns = ['sex', 'region', 'education'] 

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server
# app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Gender Difference within United States"),
        
        dcc.Markdown(children = para_1),
        dcc.Markdown(children = para_2),
        
        html.H2("Gender Difference in Annual Income, Job Prestige, Socioeconomic Status and Years of Formal Education"),
        
        dcc.Graph(figure = table_data_2),
        
        html.H2("Gender Difference in Level of Agreement for the Male Breadwinner Question"),
        dcc.Markdown(children = 'Agree or Disagree with: "It is much better for everyone involved if the man \
        is the achiever outside the home and the woman takes care of the home and family."'),
        
        # dcc.Graph(figure=fig3),
        
        html.Div([
            
            html.H3("Select the variable you want to see. "),
            
            dcc.Dropdown(id='bar',
                         options=[{'label': i, 'value': i} for i in bar_columns],
                         value='male_breadwinner'),
            
            html.H3("Select the grouping variable you want to use"),
            
            dcc.Dropdown(id='group',
                         options=[{'label': i, 'value': i} for i in group_columns],
                         value='sex')
        
        ], style={'width': '25%', 'float': 'left', 'margin-bottom': 100}),
        
        html.Div([
            
            dcc.Graph(id="graph")
        
        ], style={'width': '70%', 'float': 'right'}),        
        
        html.Div([
            
            html.H2("Scatterplot of Job Prestige versus Annual Income by Gender"),
        
            dcc.Graph(figure=figure_4),

            html.H2("Distribution of Annual Income by Gender"),

            dcc.Graph(figure=figure_5_income),

            html.H2("Distribution of Job Prestige by Gender"),

            dcc.Graph(figure=figure_5_prestige),

            html.H2("Distribution of Annual Income by Job Prestige group by Gender"),

            dcc.Graph(figure=figure_6)], style={'width': '100%', 'float': 'left','padding': 10})    
    ]
)

@app.callback(Output(component_id="graph",component_property="figure"), 
                  [Input(component_id='bar',component_property="value"),
                   Input(component_id='group',component_property="value")])

def make_figure(bar, group):
    
    table_data_3 = gss_clean[['id', group, bar]].groupby([group, bar]).count().reset_index()
    table_data_3 = table_data_3.rename({'id':'count'}, axis = 1)

    return px.bar(table_data_3, x=bar, y='count', color = group, barmode = 'group')

if __name__ == '__main__':
#     app.run_server(debug=True, port=8051, host='0.0.0.0')
#     app.run_server(mode='inline', debug=True, port=1234)
    app.run_server(debug=True)
