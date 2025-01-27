import pandas as pd
import numpy as np

def create_databases():

    df = pd.read_csv('U.S._Chronic_Disease_Indicators.csv')

    nutr_topic = df[df['Topic'] == 'Nutrition, Physical Activity, and Weight Status']
    hs_topic = df[df['Topic'] == 'Health Status']

    # Elizabeth default df
    eq = hs_topic[hs_topic['Question'] == 'Recent activity limitation among adults']
    eq = eq[eq['DataValueType']=='Crude Mean']
    
    ## Elizabeth recent activity over the years
    eq1 = eq[eq['StratificationCategory1']=='Sex']
    eq1_gen = eq1[eq1['StratificationCategory1']=='Sex']
    eq1_gen_year= eq1_gen.groupby(['Stratification1','YearEnd']).mean(numeric_only=True).reset_index()
    eq1_gen_year['YearEnd'] = eq1_gen_year['YearEnd'].astype(str)
    eq1_gen_year.to_pickle('eq1.pkl')
    
    ## Elizabeth box plot
    eq2 = eq[eq['StratificationCategory1']=='Age']
    eq2.to_pickle('eq2.pkl')
    
    ## Elizabeth USA plot (same as default)
    eq3 = eq.groupby(['LocationAbbr']).mean(numeric_only=True).reset_index()
    eq3.to_pickle('eq3.pkl')


    # Michael default data frame
    mq = nutr_topic[nutr_topic['Question'] == 'No leisure-time physical activity among adults']

    ## Michael USA Leisure time
    mq1 = mq[mq['DataValueType'] == 'Crude Prevalence']
    mq1 = mq1.groupby(['LocationAbbr']).mean(numeric_only=True).reset_index()
    mq1.to_pickle('mq1.pkl')

    ## Michael Demographic Line over years
    mq_fig2 = mq[['YearEnd', 'Stratification1', 'DataValueType','DataValue']]
    mq_fig2 = mq_fig2[mq_fig2['DataValueType'] == 'Crude Prevalence']
    ethnicities_to_include = ['Hispanic', 'White, non-Hispanic', 'Black, non-Hispanic', 'American Indian or Alaska Native, non-Hispanic', 'Asian, non-Hispanic', 'Multiracial, non-Hispanic', 'Hawaiian or Pacific Islander, non-Hispanic']
    mq_ethnicity = mq_fig2[mq_fig2['Stratification1'].isin(ethnicities_to_include)]
    fig_m2_data = mq_ethnicity[['Stratification1', 'YearEnd','DataValue']]
    fig_m2_data = fig_m2_data.groupby(['Stratification1', 'YearEnd']).mean().reset_index()
    mq2_2 = fig_m2_data
    mq2_2.to_pickle('mq2_2.pkl')
    
    ## Michael Pie Charts
    fig3_data = mq
    fig3_data_c = fig3_data.dropna(subset=['DataValue']).dropna(axis=1, how='all')
    stratifications_to_include = ['Male', 'Female']
    fig3_data_c = fig3_data_c[fig3_data_c['Stratification1'].isin(stratifications_to_include)]
    fig3_data2 = fig3_data_c[['LocationDesc', 'DataValue', 'Stratification1']]
    fig3_data2 = fig3_data2.groupby(['LocationDesc', 'Stratification1']).mean().reset_index()
    mq3 = fig3_data2
    mq3.to_pickle('mq3.pkl')


    # Dan default data frame
    dq = nutr_topic[nutr_topic['Question'] == 'Obesity among adults']
    
    ## Dan obesity over time graph
    dq1 = dq[['DataValueType','YearEnd','DataValue']]
    dq1 = dq1.groupby(['DataValueType','YearEnd']).mean(numeric_only=True).reset_index()
    dq1.to_pickle('dq1.pkl')

    ## Dan USA Obesity Crude Prevalance
    dq2 = dq[dq['DataValueType'] == 'Crude Prevalence']
    dq2 = dq2[['LocationAbbr', 'DataValue']]
    dq2 = dq.groupby(['LocationAbbr']).mean(numeric_only=True).reset_index()
    dq2.to_pickle('dq2.pkl')

    ## Dan histogram
    dq3 = dq[dq['DataValueType'] == 'Crude Prevalence']
    dq3.to_pickle('dq3.pkl')

    # Nikki default data frame
    nq = hs_topic[hs_topic['Question'] == '2 or more chronic conditions among adults']
    
    ## Nikki USA graph uses her default df
    nq1 = nq[nq['DataValueType'] == 'Crude Prevalence']
    nq1 = nq1.groupby(['LocationAbbr']).mean(numeric_only=True).reset_index()
    nq1.to_pickle('nq1.pkl')
    
    ## Nikki violin plot
    nq2_tormv = ['Age 18-44', 'Age 45-64', 'Age >=65', 'Female', 'Male']
    nq2 = nq[~nq['Stratification1'].isin(nq2_tormv)]
    nq2.to_pickle('nq2.pkl')
    
    ## Nikki scatter plot
    nw_ages = nq[nq['Stratification1'].str.contains('Age')]
    stratification1_to_size = {'Age 18-44': 1, 'Age 45-64': 2, 'Age >=65': 3}
    nq3 = nw_ages.groupby(['YearEnd', 'Stratification1'])['DataValue'].mean(numeric_only=True).reset_index()
    nq3['SizeCategory'] = nq3['Stratification1'].map(stratification1_to_size)
    nq3.to_pickle('nq3.pkl')

    # Bing default data frame, used for all questions
    bing_question = hs_topic[hs_topic['Question'] == 'Frequent physical distress among adults']
    bing_question = bing_question.dropna(how='all', axis=1)
    crude_df = bing_question[bing_question['DataValueType'] == 'Crude Prevalence'][['DataValue']]
    age_adjusted_df = bing_question[bing_question['DataValueType'] == 'Age-adjusted Prevalence'][['DataValue']]
    crude_df.rename(columns={'DataValue': 'Crude_Prevalence'}, inplace=True)
    age_adjusted_df.rename(columns={'DataValue': 'Age_adjusted_Prevalence'}, inplace=True)
    bing_question = pd.merge(bing_question, crude_df, how='left', left_index=True, right_index=True)
    bing_question = pd.merge(bing_question, age_adjusted_df, how='left', left_index=True, right_index=True)
    bing_question.drop(columns=['DataValueType','DataValue'], inplace=True)
    bing_question['YearEnd'] = bing_question['YearEnd'].astype(str)
    bq = bing_question
    bq.to_pickle('bq.pkl')

