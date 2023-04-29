# !pip install dash
# !pip install jupyter_dash
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

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


table_data_2 = gss_clean[['income', 'job_prestige', 'socioeconomic_index', 'education', 'sex']].groupby('sex')
table_data_2 = table_data_2.mean().round(2).reset_index()

table_data_2 = table_data_2.rename({'income': 'AnnualIncome',  'job_prestige': 'OccupationalPrestigeScore',  
                                'socioeconomic_index': 'SocioeconomicIndex', 'education': 'YearsofFormalEducation',
                                'sex': 'Sex'}, axis = 1)
table_data_2 = ff.create_table(table_data_2)
table_data_2.show()

data_table_3 = gss_clean[['id', 'sex', 'male_breadwinner']].groupby(['sex', 'male_breadwinner']).count().reset_index()
data_table_3 = data_table_3.rename({'id':'count'}, axis = 1)

figure_3 = px.bar(data_table_3, x='male_breadwinner', y='count', color='sex',
              labels={'male_breadwinner':'Agreement Level with Male Breadwinner', 
                      'count':'Number of People'},
              text='count',
              hover_data = ['male_breadwinner'],
              barmode = 'group')

figure_3.update_layout(showlegend=True)
figure_3.update(layout=dict(title=dict(x=0.5)))
figure_3.show()


data_table_4 = gss_clean[['sex', 'job_prestige', 'income', 'education', 'socioeconomic_index']]

figure_4 = px.scatter(data_table_4, x='job_prestige', y='income', 
                  color = 'sex', 
                  trendline='ols',
                  height=800, width=800,
                  labels={'job_prestige':'Occupational Prestige Score', 
                          'income':'Annual Income'},
                  hover_data=[ 'socioeconomic_index', 'education'])

figure_4.update(layout=dict(title=dict(x=0.5)))
figure_4.show()


data_table_5_income = gss_clean[['sex', 'income']]

figure_5_income = px.box(data_table_5_income, x='income', y = 'sex', color = 'sex', 
                     labels={'income':'Annual Income'})

figure_5_income.update(layout=dict(title=dict(x=0.5)))
figure_5_income.update_layout(showlegend=False)
figure_5_income.show()

data_table_5_job_prestige = gss_clean[['sex', 'job_prestige']]

figure_5_job_prestige = px.box(data_table_5_job_prestige, x='job_prestige', y = 'sex', color = 'sex', 
                     labels={'job_prestige':'Occupational Prestige Score'})

figure_5_job_prestige.update(layout=dict(title=dict(x=0.5)))
figure_5_job_prestige.update_layout(showlegend=False)
figure_5_job_prestige.show()

data_table_6 = gss_clean[['income', 'sex', 'job_prestige']]

data_table_6['prestige_group'] = pd.cut(data_table_6.job_prestige, 
                                      bins = 6, 
                                      labels=("1 VeryLow", "2 Low", "3 Medium", 
                                              "4 High", "5 VeryHigh", "6 SuperHigh"))
data_table_6 = data_table_6.dropna()

data_table_6 = data_table_6.sort_values('prestige_group')


figure_6 = px.box(data_table_6, x = 'income', y = 'sex', color = 'sex', 
              facet_col='prestige_group', facet_col_wrap=2,
              color_discrete_map = {'male':'blue', 'female':'red'},
              labels={'income':'Annual Income', 'sex':''})

figure_6.update(layout=dict(title=dict(x=0.5)))
figure_6.update_layout(showlegend=False)
figure_6.show()

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

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
        
        dcc.Graph(figure=figure_3),
        
        html.H2("Scatterplot of Job Prestige versus Annual Income by Gender"),
        
        dcc.Graph(figure=figure_4),
        
        html.H2("Distribution of Annual Income by Gender"),
        
        dcc.Graph(figure=figure_5_income),
        
        html.H2("Distribution of Job Prestige by Gender"),
        
        dcc.Graph(figure=figure_5_job_prestige),
        
        html.H2("Distribution of Annual Income by Job Prestige group by Gender"),
        
        dcc.Graph(figure=figure_6)
    
    ]
)

if __name__ == '__main__':
#   app.run()
  app.run_server(debug=True)
