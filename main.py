import os
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np

from dotenv import load_dotenv
load_dotenv()

def filedownload(df,startDate,endDate,state):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="CovidResultsFrom{startDate}To{endDate}for{state}.csv">Download CSV File</a>'
    return href

key = os.getenv("KEY")
url = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=" + key
url_current = "https://api.covidactnow.org/v2/states.csv?apiKey=" + key
df = pd.read_csv(url)

columns = ['state','actuals.newCases','actuals.cases','metrics.caseDensity','metrics.weeklyNewCasesPer100k','metrics.infectionRate',
 'actuals.positiveTests','actuals.negativeTests','metrics.testPositivityRatio','actuals.icuBeds.currentUsageCovid',
'actuals.hospitalBeds.currentUsageCovid','actuals.vaccinesDistributed','actuals.vaccinationsAdditionalDose',
 'metrics.vaccinationsInitiatedRatio','metrics.vaccinationsCompletedRatio','actuals.deaths']
states = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California',  'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',  'DE': 'Delaware', 'FL': 'Florida',  'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}

st.title('Covid 19 Analysis across US  ')
st.markdown("""
 **This web application would provide analysis on real time data related to Covid across all states located in United states**.\n
 1. Before beginning the analysis, it is important to specify the time range and location for the data collection. 
 This can be done by defining the desired time frame and selecting the specific state of interest in the sidebar. 
 Additionally, the CSV file containing the specified data can also be downloaded for further analysis. 
 * **Data source:** [covidactnow.org/](https://covidactnow.org/).
 """)



today = datetime.date.today()
#st.sidebar.header('User Input Features')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))
start_date = st.sidebar.date_input('Start date', today)
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.success('Data from " `%s`" to " `%s` "' % (start_date, end_date))
if end_date > datetime.date.today():
    st.error('End date must fall in today or before')
else:
    st.error('Error: End date must fall after start date.')

selected_state = st.sidebar.selectbox('State', df.state.unique())

#slider for picking a date
try:
    start_time = st.slider(
        "**Select a specific date in range**", start_date, end_date,
        value=end_date,
        format="MM/DD/YY")
    st.write(f"Number of new cases in {selected_state} at {str(start_time)} are:  ",
             df.groupby("date").sum()['actuals.newCases'][str(start_time)])
    st.write("\n")
except:
    st.error('Values are not correct')



df.index = pd.to_datetime(df.date)
df = df[columns]
df = df[df.state == selected_state]
df_result = df[start_date:end_date]
st.write("Data table Requested as follows:")
st.dataframe(df_result)

st.markdown(filedownload(df_result,start_date,end_date,selected_state), unsafe_allow_html=True)

#plotting
st.write(f"2. Real time analysis from {str(start_date)} to {str(end_date)} in {selected_state} is provided in following:")

col1, col2= st.columns([10,10])
with col1:
    if st.button('All the cases'):
        st.write(f'New Cases trend from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['actuals.cases'] != 0]
            plt.style.use("dark_background")
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.cases")
        st.pyplot(f)


with col2:
    if st.button('New Cases trend'):
        st.write(f'allthe cases from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['actuals.newCases'] != 0]
            plt.style.use("dark_background")
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.newCases")
        st.pyplot(f)
col3,col4 = st.columns([10,10])
with col3:
    if st.button('Positive tests Ratio'):
        st.write(f'Positive test ratio from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['metrics.testPositivityRatio'] != 0]
            plt.style.use("dark_background")
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="metrics.testPositivityRatio")
        st.pyplot(f)

with col4:
    if st.button('Vaccinated initiated ratio'):
        st.write(f'Vaccinated initiated from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['metrics.vaccinationsInitiatedRatio'] != 0]
            plt.style.use("dark_background")
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="metrics.vaccinationsInitiatedRatio")
        st.pyplot(f)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')

    corr = df_result.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        plt.style.use("dark_background")
        f, ax = plt.subplots(figsize=(15, 10))
        ax = sns.heatmap(corr, mask=mask, vmin=-1, vmax=1, annot=True)
    st.pyplot(f)


#Current data
df2 = pd.read_csv(url_current)
df2['deathRatio'] = (df2['actuals.deaths']/df2.population)*100
df2.rename(columns={"metrics.vaccinationsCompletedRatio":"vaccinatedRatio"}, inplace=True)
selected_states = st.sidebar.multiselect('Select States to perform comparison', df2.state.unique(), [])
df_result = df2.loc[df2['state'].isin(selected_states)][['state','deathRatio','vaccinatedRatio']]



#Copmarison part between selected states

st.write("\n\n3. To perform a comparison on the ratio of vaccinated individuals and the ratio of deaths, you can select any number of states from the sidebar.")

if st.button('Comparison'):
    st.header(f'Comparison between: {" & ".join([states[state] for state in selected_states])}')

    st.bar_chart(df_result.set_index('state'))
    with sns.axes_style("dark"):
        st.set_option('deprecation.showPyplotGlobalUse', False)
        plt.style.use("dark_background")
        f, ax = plt.subplots(figsize=(7, 5))
        df_result.plot(x='state', y=["deathRatio", "vaccinatedRatio"], kind="bar", rot=0)
    st.pyplot()


#ChatGPT

# from pyChatGPT import ChatGPT
# chat_key = os.getenv("CHAT_GPTKEY")
#
# api = ChatGPT(chat_key)
# response = api.send_message("hi")
# st.write(response)




