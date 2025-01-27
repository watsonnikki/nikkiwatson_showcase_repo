# Optimal Squencing of Biologic Treatments of Crohn's Disease
'''
Note: For graphs plotted with plotly (go, px), they are interactive and you
will be able to zoom in and out of the graph as well as hover over to see
specific values. To view the graph, uncomment the line that says 'graph.show()'.
'''

# Import Statements
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import scipy as sp
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Treatments and their assosiated failure rates
healthy_rate = {'healthy': 0.009706}
treatment_failure_rates = {'mesalamine': 60,
                    'remicade': 60,
                    'humira': 32,
                    'entyvio': 60,
                    'skyrizi': 12.3,
                    'rinvoq': 86}
failure_rate = {'failure': 0}


def define_treatments():
    '''
    Defines the treatment options for Crohn's Disease.
    Treatment options are aligned with current clinical practice.
    Takes no arguments. Returns a dictionary of treatment options.
    '''
    permutations = list(it.permutations(treatment_failure_rates.keys(), 6))
    treatment_progressions = {i: treatment for i, treatment in enumerate(permutations) if i < 51}
    return treatment_progressions

def simulate_model(x, t, params, treatment_order):
    '''
    Simulates a linear compartmental model for the progression of
    patients through a treatment option.
    Takes the following arguments:
        x: a list of the initial values of the compartments
        t: a list of time points to evaluate the model at
        params: a dictionary of the parameters for the model
        treatment_order: a list of the treatments to be used in the model
    Returns a list of the values of the compartments at each time point.
    '''
    # Unpack the parameter rates
    healthy_rate = 1/0.009706
    rates = {treatment: 1/params[treatment] for treatment in treatment_order}
    failure_rate = 1

    # Unpack the initial values
    num_patients = {treatment: x[i] for i, treatment in enumerate(treatment_order)}
    num_failure = x[-1]

    dx = np.zeros(len(x))
    dx[0] = -healthy_rate * num_patients[treatment_order[0]]
    for i, treatment in enumerate(treatment_order):
        if i == 0:
            dx[i] = -rates[treatment] * num_patients[treatment]
        else:
            dx[i] = rates[treatment_order[i-1]] * num_patients[treatment_order[i-1]] - rates[treatment] * num_patients[treatment]
    dx[-2] = rates[treatment_order[-1]] * num_patients[treatment_order[-1]]
    dx[-1] = failure_rate * num_patients[treatment_order[-1]]

    return dx

def calculate_cost(treatment_years, failure_years):
    '''
    Calculates the cost of a treatment plan based on the number of years
    in treatment and the number of years in failure.
    Takes the following arguments:
        treatment_years: the number of years in treatment
        failure_years: the number of years in failure
    Returns the cost of the treatment plan.
    '''
    infusion_cost = 41549
    ostomy_cost = 47114

    cost_of_failure = ostomy_cost + (failure_years * 3000) # cost of ostomy maintenance
    cost_of_treatment = infusion_cost * treatment_years * 6 # cost of infusion treatment if given once every two months (moderate disease)

    return (cost_of_treatment, cost_of_failure)

if __name__ == '__main__':

    # # Print the treatment options
    # for i in range(51):
    #     print(define_treatments()[i])

    # Define the initial values
    num_healthy = 340000000 # 340 million people in the US
    num_mesalamine = 1011000 # 1.011 million people in the US with Crohn's Disease

    # Initial state values
    x0 = [num_healthy, num_mesalamine, 0, 0, 0, 0, 0, 0]

    # Time = 25 years
    t0 = 1
    tf = 26
    dt = 1

    # Time points
    t = np.arange(t0, tf, dt)

    # Treatments used in model
    treatments = define_treatments()


    # Modeling for 50 permutations of the treatment plans
    results = {}
    total_people = sum(x0)
    for i in range(51):
        for treatment_key, treatment_value in treatments.items():
            x = sp.integrate.odeint(simulate_model, x0, t, args=(treatment_failure_rates, treatment_value),)
            df = pd.DataFrame(x, columns=['healthy', 'mesalamine', 'remicade', 'humira', 'entyvio', 'skyrizi', 'rinvoq', 'failure'])
            df['failure_rate'] = df['failure'] / total_people
            df['Year'] = t
            df = df[['Year', 'healthy', 'mesalamine', 'remicade', 'humira', 'entyvio', 'skyrizi', 'rinvoq', 'failure', 'failure_rate']]
            df.set_index('Year', inplace=True)
            results[treatment_key] = df


    # Printing results for each permutation
    # for i in range(51):
    #     print(f'Dataframe {i}: {results[i]}')


    # Dataframe with only the failure results
    # Each column is a treatment plan and each row is the number of failures in each year
    failure_df = pd.DataFrame()
    for key, df in results.items():
        failure_df[key] = df['failure']


    # Failure of each treatment after 25 years
    failures_at_25_years = failure_df.loc[25]
    fail_plot = px.bar(failures_at_25_years, x=failures_at_25_years.index, y=failures_at_25_years.values,
                    color=failures_at_25_years.values, color_continuous_scale='viridis', title='Cumulative Failures at 25 Years Per Trial',
                    labels={'index':'Treatment Plan', 'y':'Number of People who Failed Treatment', 'color': 'Failures'})
    # fail_plot.show()


    # Plotting the best performing treatment plans
    best_performers = failures_at_25_years[failures_at_25_years < 100000]
    best_performing_treatments = {key: value for key, value in treatments.items() if key in best_performers.index}
    print('\nBest Performers')
    for treatment, failure_rate in best_performing_treatments.items():
        print(f'Treatment Plan: {treatment}, Failure Rate: {failure_rate}')
    fail_plot = px.bar(best_performers, x=best_performers.index, y=best_performers.values,
                    color=best_performers.index, color_continuous_scale= 'viridis', title='Cumulative Failures of Best Performers',
                    labels={'index':'Treatment', 'y':'Number of People who Failed Treatment'},
                    text=best_performers.index)
    fail_plot.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fail_plot.update_layout(height=600)
    # fail_plot.show()

    # Plotting the worst performing treatment plans
    worst_performers = failures_at_25_years[failures_at_25_years > 500000]
    worst_performing_treatments = {key: value for key, value in treatments.items() if key in worst_performers.index}
    print('\nWorst Performers')
    for treatment, failure_rate in worst_performing_treatments.items():
        print(f'Treatment Plan: {treatment}, Failure Rate: {failure_rate}')
    fail_plot = px.bar(worst_performers, x=worst_performers.index, y=worst_performers.values,
                    color=worst_performers.index, color_continuous_scale= 'viridis', title='Cumulative Failures of Worst Performers',
                    labels={'index':'Treatment', 'y':'Number of People who Failed Treatment'},
                    text=worst_performers.index)
    fail_plot.update_traces(textposition='outside')
    fail_plot.update_layout(height=600)
    # fail_plot.show()

    # Plotting the failure rates of middle performing treatment plans
    failures_in_between = failures_at_25_years[(failures_at_25_years < 500000) & (failures_at_25_years > 100000)]
    treatments_in_between = {key: value for key, value in treatments.items() if key in failures_in_between.index}
    print('\nMiddle Performers')
    for treatment, failure_rate in treatments_in_between.items():
        print(f'Treatment Plan: {treatment}, Failure Rate: {failure_rate}')
    fail_plot = px.bar(failures_in_between, x=failures_in_between.index, y=failures_in_between.values,
                    color=failures_in_between.index, color_continuous_scale= 'viridis', title='Cumulative Failures of Middle Performers',
                    labels={'index':'Treatment', 'y':'Number of People who Failed Treatment'},
                    text=failures_in_between.index)
    fail_plot.update_traces(textposition='outside')
    fail_plot.update_layout(height=600)
    # fail_plot.show()

    # Plotting the failure rates of all treatment plans
    all_data = pd.concat(results, names=['Treatment', 'Year'])
    all_data.reset_index(inplace=True)
    category_mapping = {0: 'Worst Performers', 1: 'Best Performers', 3: 'Middle Performers 1', 9: 'Middle Performers 2'}
    all_data = all_data[all_data['Treatment'].isin([0, 1, 3, 9])] # Idices in each category
    all_data['Treatment'] = all_data['Treatment'].map(category_mapping)
    facet_graph = px.line(all_data, x='Year', y='failure_rate', color='Treatment', title='Failure Rate for All Treatment Plans',
                            labels={'failure_rate':'Failure Rate', 'Year':'Year', 'Treatment':'Treatment Category'})
    facet_graph.update_xaxes(matches=None)
    # facet_graph.show()

    print(f'\nPeople - Years in study')
    # People-years in study
    average_years = 0
    for df in results.values():
        average_years += df.iloc[-1].sum()
    average_years /= 50
    print(f'Total Years: {average_years}')

    average_failure_years = 0
    for df in results.values():
        average_failure_years += df['failure'].sum()
    average_failure_years /= 50
    print(f'Total Failure Years: {average_failure_years}')

    average_treatment_years = 0
    for df in results.values():
        average_treatment_years += df['mesalamine'].iloc[-1]
        average_treatment_years += df['remicade'].iloc[-1]
        average_treatment_years += df['humira'].iloc[-1]
        average_treatment_years += df['entyvio'].iloc[-1]
        average_treatment_years += df['skyrizi'].iloc[-1]
        average_treatment_years += df['rinvoq'].iloc[-1]
    average_treatment_years /= 50
    print(f'Total Treatment Years: {average_treatment_years}')

    healthy_years = average_years - average_failure_years - average_treatment_years
    print(f'Healthy Years: {healthy_years}')

    # plot years in pie chart
    fig = go.Figure(data=[go.Pie(labels=['Total Failure Years', 'Total Treatment Years', 'Total Healthy Years'],
                                values=[average_failure_years, average_treatment_years, healthy_years])],
                                layout=go.Layout(title='People-Years in Study'))
    # fig.show()

    # extrapolate failure years
    average_extrapolated_failure_years = average_failure_years*25
    healthy_years = average_years - average_extrapolated_failure_years - average_treatment_years
    fig = go.Figure(data=[go.Pie(labels=['Total Failure Years', 'Total Treatment Years', 'Total Healthy Years'],
                                values=[average_extrapolated_failure_years, average_treatment_years, healthy_years])],
                                layout=go.Layout(title='People-Years in Study when Failure is Extrapolated'))
    # fig.show()

    # Calculate Cost
    print('\nCost')
    cost = calculate_cost(average_treatment_years, average_extrapolated_failure_years)
    print(f'Cost of Treatment: {cost[0]}')
    print(f'Cost of Failure: {cost[1]}')


    print('\nDALYs')
    # Dalys
    # failure burden = 0.095
    # treatment burden = 0.231
    failure_daly = average_failure_years*0.095
    extrapolated_failure_dalys = average_failure_years*25*0.095 # 25 more years per person in failure
    treatment_daly = average_treatment_years*0.231

    print(f'Failure DALY: {failure_daly}')
    print(f'Extrapolated Failure DALY: {extrapolated_failure_dalys}')
    print(f'Treatment DALY: {treatment_daly}')

    # Plot failure dalys and extrapolated failure dalys
    bars = plt.bar(['Failure DALYs', 'Extrapolated Failure DALYs'],
        [failure_daly, extrapolated_failure_dalys])
    plt.ylabel('DALYs')
    plt.title('DALYs for Failure & Extrapolated Failure')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 2), va='bottom')
    # plt.show()

    # Plot average treatment dalys vs. extrapolated failure dalys
    bars = plt.bar(['Treatment DALYs', 'Extrapolated Failure DALYs'],
        [treatment_daly, extrapolated_failure_dalys])
    plt.ylabel('DALYs')
    plt.title('DALYs for Treatment vs. Extrapolated Failure')

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, round(yval, 2), va='bottom')
    # plt.show()
