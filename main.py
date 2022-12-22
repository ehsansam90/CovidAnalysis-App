import os

import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import datetime

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

st.title('Covid 19 Analysis across US  ')
st.markdown("""
 This app performs simple ... !
 * **Python libraries:** base64, pandas, streamlit
 * **Data source:** [Basketball-reference.com](https://apidocs.covidactnow.org/migration/).
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
        "Select a specific date in range", start_date, end_date,
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
st.dataframe(df_result)

st.markdown(filedownload(df_result,start_date,end_date,selected_state), unsafe_allow_html=True)

#plotting

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
        f, ax = plt.subplots(figsize=(15, 10))
        ax = sns.heatmap(corr, mask=mask, vmin=-1, vmax=1, annot=True)
    st.pyplot(f)

st.write(df['actuals.newCases'].dropna())

#Current data
df2 = pd.read_csv(url_current)
df2['deathRatio'] = (df2['actuals.deaths']/df2.population)*100
df2.rename(columns={"metrics.vaccinationsCompletedRatio":"vaccinatedRatio"}, inplace=True)
selected_states = st.sidebar.multiselect('Select States to perform comparison', df2.state.unique(), [])
df_result = df2.loc[df2['state'].isin(selected_states)][['state','deathRatio','vaccinatedRatio']]
st.write(df_result)



#Copmarison part between selected states
if st.button('Comparison'):
    st.write('--')

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




