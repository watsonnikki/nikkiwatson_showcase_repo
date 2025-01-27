import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go

def plot_efig1(): ## Elizabeth's bar chart of physical activity limitation
    eq1 = pd.read_pickle('eq1.pkl')
    fig = px.bar(eq1,
             x='Stratification1',  # Place gender on the x-axis
             y='DataValue',  # This is the mean value you want to plot
             color='YearEnd',  # Use color to represent different years
             barmode='group',  # Ensures that the bars for each year/gender are side by side
             title='Recent Activity Limitation by Gender Over the Years',
             labels={'Stratification1': 'Gender', 'DataValue': 'Average Activity Limitation', 'YearEnd': 'Year'})

    return fig

def plot_efig2(): ## Elizabeth's histogram by year
    eq2 = pd.read_pickle('eq2.pkl')
    fig = px.box(eq2,
             x='YearEnd',
             y='DataValue',
             color='Stratification1',
             title='Recent Physical Activity Limitation by Age Group Over Time',
             labels={'Stratification1': 'Age Group', 'DataValue': 'Physical Activity Limitation', 'YearEnd': 'Year'})

    return fig

def plot_efig3(): ## Elizabeth's choropleth
    eq3 = pd.read_pickle('eq3.pkl')

    fig = px.choropleth(eq3, locations='LocationAbbr', color='DataValue',
                           locationmode='USA-states',
                           color_continuous_scale='Viridis',
                           scope="usa",
                           labels={'data_value':'Data Value'},
                           title="Crude Mean of Recent Activity Limitation of Adults in the US, Years 2019-2022"
                          )
    return fig


def plot_dfig1(): ## Plot Dan's obesity over time graph
    dq1 = pd.read_pickle('dq1.pkl')

    fig = px.line(dq1, x='YearEnd',y='DataValue',color='DataValueType',
                range_y=[30.01,35], title="Prevalence of U.S. Adult Obesity Over Time",
                labels={'DataValue':'Percent (%)', 'YearEnd':'Year', 'DataValueType': 'Crude Prevalence'})        
    fig.update_yaxes(nticks=6)
    fig.update_xaxes(nticks=4)
    fig.update_layout(title={'x':0.5,})

    return fig

def plot_dfig2(): ## Plot Dan's obesity in USA map
    dq2 = pd.read_pickle('dq2.pkl')

    fig = px.choropleth(dq2, locations='LocationAbbr', color='DataValue',
                           locationmode='USA-states',
                           color_continuous_scale='Viridis',
                           scope="usa",
                           labels={'DataValue':'Crude Prevalence Obesity','LocationAbbr':'State'},
                           title="Percentage of Obese Adults Per State"
                         )
    return fig

def plot_dfig3(): ## Plot Dan's demographics
    dq3 = pd.read_pickle('dq3.pkl')

    fig = px.histogram(dq3, x="Stratification1", y="DataValue",
             barmode='group', color="StratificationCategory1", histfunc='avg',
             labels={'avg of DataValue ':'Obesity Rate (%)','StratificationCategory1':'',
                     'Stratification1':''},
             title="Adult Obesity Rate by Demographics",
             #category_orders={'Stratification1':legend_order},
             height=600)
    return fig

def plot_mfig1(): # Michael's choropleth of non-engagement in PA
    mq1 = pd.read_pickle('mq1.pkl')
    mq1 = mq1[~mq1['LocationAbbr'].isin(['GU','VI','PR', 'US'])]
    fig = px.choropleth(mq1, locations='LocationAbbr', color='DataValue',
                    locationmode='USA-states',
                    color_continuous_scale='Viridis',
                    scope="usa",
                    labels={'DataValue':'Percentage of Adults'},
                    title="Percentage of Adults that do not Engage in Leisure-time Physical Activity in the US",
                    range_color=[mq1['DataValue'].min(),mq1['DataValue'].max()]
                    )
    return fig

def plot_mfig2(): # Michael's line chart of percent of adults non PA over time
    mq2_2 = pd.read_pickle('mq2_2.pkl')
    fig = px.line(mq2_2, x='YearEnd',y='DataValue',color='Stratification1', 
                 title="Adults not Engaging in Physical Activity During Leisure Time",
                 labels={'DataValue':'Percent (%)', 'YearEnd':'Year', 'Stratification1': 'Demographic'})
    fig.update_yaxes(nticks=6)
    fig.update_xaxes(nticks=4)
    fig.update_layout(title={'x':0.5,})
    return fig


def plot_mfig3(selected_state):
    # Load your data
    mq3 = pd.read_pickle('mq3.pkl')
    
    # Filter the dataframe for the selected state
    fig3_data_state = mq3[mq3['LocationDesc'] == selected_state]
    
    # Create subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]])
    male_percent = fig3_data_state.loc[fig3_data_state['Stratification1'] == 'Male', 'DataValue'].values[0]
    female_percent = fig3_data_state.loc[fig3_data_state['Stratification1'] == 'Female', 'DataValue'].values[0]

    male_data = {'Category': ['Males that do not perform leisure time physical activity',
        'Males that do perform leisure time physical activity'], 'Percent': [male_percent, 100 - male_percent]}
    fig.add_trace(
        go.Pie(labels=male_data['Category'], values=male_data['Percent'], name='Males'),
        row=1, col=1
    )

    female_data = {'Category': ['Females that do not perform leisure time physical activity',
        'Females that do perform leisure time physical activity'], 'Percent': [female_percent, 100 - female_percent]}
    fig.add_trace(
        go.Pie(labels=female_data['Category'], values=female_data['Percent'], name='Females'),
        row=1, col=2
    )

    fig.update_layout(
        title_text=f"Gender Distribution of Adults that do not Engage in Physical Activity in {selected_state} ",
        annotations=[dict(text='', x=0.20, y=0.5, font_size=12, showarrow=False),
                    dict(text='', x=0.80, y=0.5, font_size=12, showarrow=False)]
    )

    return fig

def plot_nfig1(): ## Plot Nikki 2 chronic conditions USA map
    nq1 = pd.read_pickle('nq1.pkl')

    fig = px.choropleth(nq1, locations='LocationAbbr', color='DataValue',
                           locationmode='USA-states',
                           color_continuous_scale='Viridis',
                           scope="usa",
                           labels={'data_value':'Data Value'},
                           title="Percentage of Adults with 2 or more Chronic Conditions in the US"
                          )
    return fig

def plot_nfig2(): ## Plot Nikki violin plot
    nq2 = pd.read_pickle('nq2.pkl')
    fig = px.violin(nq2, y="DataValue", x="Stratification1", color='Stratification1',
                box=True, points=False, hover_data=nq2.columns,
                title="Distribution of Adults with 2 or more Chronic Conditions by Demographic Group",
                labels={'DataValue':'Percent (%)', 'Stratification1':'Demographic Group'})
    fig.update_layout(title={'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'}, showlegend=False)
    return fig

def plot_nfig3(): ## Plot Nikki scatter
    nq3 = pd.read_pickle('nq3.pkl')
    fig = px.scatter(nq3, x='YearEnd', y='DataValue', title='Percentage of Adults with 2 or more Chronic Conditions by Age',
                 size='SizeCategory', color='Stratification1', range_x=[2018, 2023],
                 labels={'DataValue':'Percent (%)', 'YearEnd':'Year', 'Stratification1': 'Age Category'},)
    fig.update_yaxes(nticks=6)
    fig.update_xaxes(nticks=8)
    fig.update_layout(title={
                        'text': "Average Percentage of Adults with 2 or more Chronic Conditions by Age per Year",
                        'y':0.9,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'})
    return fig

def plot_bfig1(): # Plot Bing's trace bar graph
    bq1 = pd.read_pickle('bq.pkl')

    # Michigan trace
    michigan_data = bq1[(bq1['LocationDesc'] == 'Michigan')]
    michigan_yearly = michigan_data.groupby('YearEnd').mean(numeric_only=True).reset_index()
    michigan_bar_trace = go.Bar(x=michigan_yearly['YearEnd'], y=michigan_yearly['Crude_Prevalence'], name='Michigan', marker_color=px.colors.sequential.Viridis[3])

    # National trace
    national_yearly = bq1.groupby('YearEnd').mean(numeric_only=True).reset_index()
    national_bar_trace = go.Bar(x=national_yearly['YearEnd'], y=national_yearly['Crude_Prevalence'], name='National', 
                                    marker_color='green')

    # Combine both traces
    fig = go.Figure(data=[national_bar_trace,michigan_bar_trace])
    fig.update_layout(
        title='Crude Prevalence in Michigan and National Average Over Years',
        xaxis_title='Year',
        yaxis_title='Crude Prevalence (%)',
        xaxis=dict(tickmode='linear'),
        barmode='group'
    )

    return fig

def plot_bfig2(): ## Bing's bubble chart
    bq2 = pd.read_pickle('bq.pkl')

    # Bubble Chart for different age group over year
    bubble_chart_data = bq2[bq2['StratificationCategory1'] == 'Age']
    bubble_chart_data = bubble_chart_data.groupby(['YearEnd', 'Stratification1']).agg({
        'Crude_Prevalence': 'mean',
        'LowConfidenceLimit': 'mean',
        'HighConfidenceLimit': 'mean'
    }).reset_index()

    # Calculating the size of the confidence interval to use as bubble size
    bubble_chart_data['ConfidenceIntervalSize'] = bubble_chart_data['HighConfidenceLimit'] - bubble_chart_data['LowConfidenceLimit']

    # Create the bubble chart
    bubble_trace = go.Scatter(
        x=bubble_chart_data['YearEnd'],
        y=bubble_chart_data['Crude_Prevalence'],
        text=bubble_chart_data['Stratification1'],
        mode='markers',
        marker=dict(
            size=bubble_chart_data['ConfidenceIntervalSize'],
            sizemode='area',
            sizeref=2.*max(bubble_chart_data['ConfidenceIntervalSize'])/(40.**2),
            sizemin=4,
            color=bubble_chart_data['Crude_Prevalence'],
            colorscale='Viridis',
            showscale=True
        )
    )

    fig = go.Figure(data=[bubble_trace])
    fig.update_layout(
        title='Average Crude Prevalence by Age Over Years',
        xaxis_title='Year',
        yaxis_title='Average Crude Prevalence (%)',
        xaxis=dict(tickmode='linear')
    )

    return fig

def plot_bfig3(): ## Bing's bar chart
    bq3 = pd.read_pickle('bq.pkl')

    bar_chart_data = bq3[bq3['StratificationCategory1'] == 'Race/Ethnicity']
    bar_chart_data = bar_chart_data.groupby(['YearEnd', 'Stratification1']).agg({
        'Crude_Prevalence': 'mean',
    }).reset_index()
    race_colors = {
        'American Indian or Alaska Native, non-Hispanic':  px.colors.sequential.Viridis[0], 
        'Multiracial, non-Hispanic':  px.colors.sequential.Viridis[2],                
        'Asian, non-Hispanic':  px.colors.sequential.Viridis[7],                           
        'Black, non-Hispanic':  px.colors.sequential.Viridis[3],                           
        'Hawaiian or Pacific Islander, non-Hispanic': px.colors.sequential.Viridis[4],    
        'Hispanic':  px.colors.sequential.Viridis[5],                                          
        'White, non-Hispanic':  px.colors.sequential.Viridis[6],   
        'Asian or Pacific Islander, non-Hispanic':  px.colors.sequential.Viridis[7],        
    }

    race_bar_traces = []
    for race in bar_chart_data['Stratification1'].unique():
        df = bar_chart_data[bar_chart_data['Stratification1'] == race]
        trace = go.Bar(
            x=df['YearEnd'],
            y=df['Crude_Prevalence'],
            name=race,
            marker_color=race_colors.get(race, '#000')
        )
        race_bar_traces.append(trace)
    fig = go.Figure(data=race_bar_traces)
    fig.update_layout(
        title='Average Crude Prevalence by Race/Ethnicity Over Years',
        xaxis_title='Year',
        yaxis_title='Average Crude Prevalence (%)',
        barmode='stack',
        legend=dict(
            title='Race/Ethnicity:',
            bgcolor='rgba(255,255,255,0.5)'
        )
    )
    fig.update_xaxes(nticks=8)
    return fig