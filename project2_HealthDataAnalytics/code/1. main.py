import dash
from dash import dcc, Dash, Input, Output, callback
from dash import html
import plotly.express as px
import pandas as pd
import EDA
import vis
import pickle
from dash.dependencies import Input, Output, State
from sklearn.pipeline import Pipeline


app = dash.Dash(__name__)
server = app.server

## Initialize all the databases to be used in visualizations
# EDA.create_databases()

mq3 = pd.read_pickle('mq3.pkl')
ml_model = pickle.load(open('ml_model.pkl', 'rb'))
ml_df = pd.read_pickle('ml_df.pkl')

app.layout = html.Div([
    html.H1('STATS 507 Group 14 Obesity and Activity Dashboard',
             style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}),
    html.H2('Elizabeth Healy, Michael Hernández Lamberty, Daniel Rubio-Ejchel, Nikki Watson, Bingqing Xiang',
            style={'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}),

    dcc.Tabs([
        dcc.Tab(label='Chronologically', children=[
            html.Div([
                html.H4(""" The question that we looked at in the following plots is there a difference between
                        the age-adjusted and crude prevalence of overall obesity in the US over the span of 4 years.
                       """),
                dcc.Graph(
                    id='dan-line',
                    figure=vis.plot_dfig1()
                ),
                html.P("""In this graph we can observe that the age adjusted prevalence of 
                       obesity in adults has the same trend as the crude, but slightly higher.
                       This makes sense and shows us that the survey age adjustment increases
                       the prevalence of obesity. Since they track each other closely though, we can 
                       use this to justify only using one of them going forward and not having to 
                       make two of each plot.
                       """
                       ),
                html.Br(),
                html.H4(""" The question that we looked at in the following plot is what is the prevalence of 2 or 
                       more chronic conditions among adults in the US. The data spans from 2019 to 2022.
                       """),
                dcc.Graph(
                    id='nikki-scatter',
                    figure=vis.plot_nfig3()
                ),
                html.P("""Across all years, there is a significantly higher prevalence of two or more chronic 
                       conditions in adults above the age of 65. 
                       """
                       ),
                html.Br(),
                html.H4(""" The question that we looked at in the following plot is the crude prevelance of no leisure-time 
                       physical activity among adults in the US. The data spans from 2019 to 2022.
                       """),
                dcc.Graph(
                    id='michael-line',
                    figure=vis.plot_mfig2()
                ),
                html.P(""" This graph illustrates that there is no specific behavior for each demographic in regards 
                       to this leisure time physical activity across time. The different demographics can be toggled 
                       on and off by clicking on the legend.
                       """
                       ),
                html.Br(),
                html.H4(""" The question that we looked at in the following plot is the crude mean of recent activity limitation
                       among adults by age group. The data spans from 2019 to 2022.
                       """),
                dcc.Graph(
                    id='elizabeth-boxplot',
                    figure=vis.plot_efig2()
                ),
                html.P("""The age group of 18 to 44 years report the lowest average recent physical limitation for all 
                       years, then the age group of 65 years and older, and thirdly the age group of 45 to 64 years.
                       """
                       ),
                html.Br(),
                html.H4(""" The question that we looked at in the following three plot is the crude prevalence of frequent 
                        physical distress among adults.
                       """),
                dcc.Graph(
                    id='bing-bar',
                    figure=vis.plot_bfig1()
                ),
                html.P("""This graph is a bar chart that indicates the crude prevalence of frequent physical distress 
                       in Michigan compared to the national average from 2019 to 2022. Michigan's average fluctuates 
                       every year, and remains higher than the national average, but the difference is diminishing year 
                       by year.
                       """
                       ),
                dcc.Graph(
                    id='bing-bubble',
                    figure=vis.plot_bfig2()
                ),
                html.P("""This graph is a bubble chart that depicts the average crude prevalence of frequent physical 
                       distress divided by year and age group. The size of the bubble means the confidence interval. 
                       The higher the age, the higher the risk of frequent physical distress. And the risk significantly 
                       increases after age 45.
                       """
                       ),
                dcc.Graph(
                    id='bing-bar2',
                    figure=vis.plot_bfig3()
                ),
                html.P("""The third graph is a stacked bar chart showing the frequent physical distress among adults 
                       prevalence over years, divided by race.The portion of each race does not change significantly over 
                       years, and American Indian has highest prevalence, while Asian has lowest prevalence. 
                       """
                       ),
            ])
        ]),
        dcc.Tab(label='Geographically', children=[
            html.Div([
                html.H4(""" The question that we looked at in the following four choropleth plots is if there are regional variations or 
                        similarities in the prevalence of various health indicators between states in the US. The data used is the mean over a 
                        span of 4 years.
                        """),
                dcc.Graph(
                    id='nikki-USA',
                    figure=vis.plot_nfig1()
                    ),
                html.P("""This graph is a choropleth that illustrates the percentage of adults in each state with 2 
                        or more chronic conditions. West Virginia is a clear outlier, with almost 30 percent of the population 
                        having 2 or more chronic conditions.
                       """
                       ),
                dcc.Graph(
                    id='daniel-USA',
                    figure=vis.plot_dfig2()
                    ),
                html.P("""From this graph, we can observe which are the more and less obese states. Colorado, New Jersey, Massachusetts, California,
                         New York, Vermont, and Florida are the least obese states. Most of these states seem to be on or near a coast, with the 
                         exceptions of Colorado and Vermont. The states that seem to struggle most with obesity are concentrated in the 
                         cultural South of the US. One difference between the least and most obese states is that the more obese states
                         tend to be ones that do not emphasize public programs and vice versa. This may be something to do with it.
                       """
                       ),
                dcc.Graph(
                    id='michael-USA',
                    figure=vis.plot_mfig1()
                    ),
                html.P("""This choropleth graph shows the state-wise overall prevalence in the United States of adults who do not engage in physcial 
                       activity during their leisure time. The data presented is the crude prevalence between 2019 and 2022.
                       """
                       ),
                dcc.Graph(
                    id='elizabeth-USA',
                    figure=vis.plot_efig3()
                    ),
                html.P("""This graph demonstrates the geographic variation of recent physical activity in the United States averaged for the years 2019-2022. 
                       It shows that there is regional variation, as nearby states generally have similar values. A clear outlier to this trend is West Virginia, 
                       which has the highest value of 4.1.  
                       """
                       ),
            ])
        ]),
        dcc.Tab(label='Demographically', children=[
            html.Div([
                html.H4(""" The following two graphs tackle the difference between genders for two different questions. The pie chart demonstrates
                        the difference between both Females and Males in each state and how their lack of leisure time physcial activity varies.
                        The bar chart demonstrates the difference in recent activity limitation over time for both Females and Males. 
                        """),
                "Choose a State: ",
                dcc.Dropdown(
                    mq3['LocationDesc'].unique(),
                    value='Alabama',
                    id='mfig3-state'
                    ),
                dcc.Graph(id='michael-pie'
                         ),
                html.P("""The differnce between both Females and Males is different for each state and no overall trend is obsereved. Using the 
                       dropdown menu, the state that is being presented can be changed to present the differences between male and females in 
                       the state.
                       """),
                dcc.Graph(
                    id='elizabeth-bar',
                    figure=vis.plot_efig1()
                    ),
                html.P("""This graph shows that gender impacts the reported average recent activity limitation across the United States. In every year from 2019 
                       to 2022, females have a higher average recent activity limitation than males. For both males and females, there is a decrease in reported 
                       activity limitation in 2020, which might be due to the Covid-19 lockdown. From 2020, the recent activity limitation increases each year 
                       for both males and females.
                       """
                       ),
                html.Br(),
                html.H4(""" The following two graphs show the difference between demographic groups for two different questions. The violin plot chart highlights 
                        the distrubiton of two or more chronic conditions across demographic groups. The bar chart demonstrates the difference in crude prevalence of 
                        adult obesity rate between 2019 and 2022 for different demographic, gender and age groups. 
                        """),
                dcc.Graph(
                    id='nikki-violin',
                    figure=vis.plot_nfig2()
                    ),
                html.P("""This graph is a violin graph that shows the distribution of people with two or more chronic conditions by demographic group. 
                        The largest range of people with chronic conditions occurred in American Indian or Alaskan Native populations while the closest 
                        range occurred in Asian populations. 
                       """
                       ),
                dcc.Graph(
                    id='daniel-bar',
                    figure=vis.plot_dfig3()
                    ),
                html.P("""This bar chart shows that sex is a minor factor when it comes to obesity rate. Both age and race groups both have much larger 
                       spreads in obesity rates. A clear outlier is Asian, non-Hispanic group having a much lower obesity rate.
                       """
                       )                
                ]),
            
            ]),
        dcc.Tab(label='Machine Learning', children=[
            html.Div([
                # html.P("learn machine learn!!!"),
                html.H2("Use a machine learning model to predict the obesity prevalence for different year, state and demographic.", 
                        style={'width': '100%', 'display': 'flex', 'align-items':'left', 'justify-content':'left'}),
                "Input a Year: ",
                dcc.Input(
                    id = 'input-1-year', value = '2025', type = 'text'
                        ),
                html.Br(),
                html.Br(),
                "Choose a State: ",
                dcc.Dropdown(
                    ml_df['LocationDesc'].unique(),
                    'Alabama',
                    id = 'input-2-state'                    
                        ),
                html.Br(), 
                "Choose a Demographic: ",
                dcc.Dropdown(
                    ml_df['Demographics'].unique(),
                    'Overall',
                    id = 'input-3-demographic'
                        ),
                html.Br(),
                html.Button('Submit', id='submit-button', n_clicks=0),
                html.Br(),
                html.H3(id='output-prediction')
             ])
        ]),
        dcc.Tab(label='Conclusion', children=[
            html.Div([
                html.H2("""
                        The comprehensive analysis across various demographics, locations, and age groups reveals insights 
                        into the health indicators of the adult population in the United States. The data underscore a higher 
                        prevalence, particularly among older adults, certain racial groups, and regions like the Appalachian 
                        mountain range and the South. The trends and patterns highlighted by the visualizations emphasize the 
                        necessity for targeted public health interventions and resources, especially in demographics and locations 
                        identified as high-risk, to address and potentially mitigate the identified health disparities. By 
                        combining local insights with broad-scale public health strategies, the goal of creating healthier 
                        communities across the United States becomes more attainable.

                    """),
                html.Br(),
                html.Img(src='assets/Group14.jpg'),
                html.Img(src='assets/Obama.gif')
             ])
        ]),
    ])
])

@callback(
    Output('michael-pie', 'figure'),  # This tells Dash to update the 'figure' of the component with ID 'michael-pie'
    [Input('mfig3-state', 'value')] # This takes the 'value' of the component with ID 'mfig3 - state' as input
)

def update_pie_chart(selected_state):
    return vis.plot_mfig3(selected_state)

@app.callback(
    Output('output-prediction', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-1-year', 'value'),
     State('input-2-state', 'value'),
     State('input-3-demographic', 'value')]
)
def update_output(n_clicks, input_year, input_state, input_demographic):
    if n_clicks is None:
        return ""
    else:
        input_year = float(input_year)
        input_state = str(input_state)
        input_demographic = str(input_demographic)
        features = pd.DataFrame({
                    'YearEnd': [input_year],
                    'LocationDesc': [input_state],
                    'Demographics': [input_demographic]
                })
        
        prediction = ml_model.predict(features)
        
        return f"The predicted percentage of obesity prevalence for {features['Demographics'][0]} adults in {features['LocationDesc'][0]} in {round(features['YearEnd'][0])} is {round(prediction[0], 2)}%"
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
