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
df = pd.read_csv(url)

columns = ['state','actuals.newCases','actuals.cases','metrics.caseDensity','metrics.weeklyNewCasesPer100k','metrics.infectionRate',
 'actuals.positiveTests','actuals.negativeTests','metrics.testPositivityRatio','actuals.icuBeds.currentUsageCovid',
'actuals.hospitalBeds.currentUsageCovid','actuals.vaccinesDistributed','actuals.vaccinationsAdditionalDose',
 'metrics.vaccinationsInitiatedRatio','metrics.vaccinationsCompletedRatio','actuals.deaths']

df.index = pd.to_datetime(df.date)
df = df[columns]
# slider for picking a date
# from datetime import datetime
# start_time = st.slider(
#     "When do you start?",datetime(2019, 1, 1),datetime(2021, 1, 1),
#     value=datetime(2020, 1, 1),
#     format="MM/DD/YY")
# st.write("Start time:", start_time)

st.title('NBA Player Stats Explorer')

st.markdown("""
 This app performs simple webscraping of NBA player stats data!
 * **Python libraries:** base64, pandas, streamlit
 * **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
 """)
today = datetime.date.today()

#st.sidebar.header('User Input Features')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))
start_date = st.sidebar.date_input('Start date', today)
end_date = st.sidebar.date_input('End date', today)
if start_date < end_date:
    st.success('Data from " `%s`" to " `%s` "' % (start_date, end_date))
else:
    st.error('Error: End date must fall after start date.')

selected_state = st.sidebar.selectbox('State', df.state.unique())

df = df[df.state == selected_state]
df_result = df[start_date:end_date]
st.dataframe(df_result)

st.markdown(filedownload(df_result,start_date,end_date,selected_state), unsafe_allow_html=True)

#ploting
# if st.button('New Cases trend'):
#     st.subheader(f'New Cases trend from _{start_date}_ to _{end_date}_')
#
#     with sns.axes_style("dark"):
#         df_graph = df_result[df_result['actuals.newCases'] != 0]
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.newCases")
#     st.pyplot(f)

# if st.button('All the cases'):
#     st.subheader(f'New Cases trend from _{start_date}_ to _{end_date}_')
#
#     with sns.axes_style("dark"):
#         df_graph = df_result[df_result['actuals.cases'] != 0]
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.cases")
#     st.pyplot(f)

col1, col2= st.columns([10,10])
with col1:
    if st.button('All the cases'):
        st.write(f'New Cases trend from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['actuals.cases'] != 0]
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.cases")
        st.pyplot(f)


with col2:
    if st.button('New Cases trend'):
        st.write(f'allthe cases from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['actuals.newCases'] != 0]
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.newCases")
        st.pyplot(f)
col3,col4 = st.columns([10,10])
with col3:
    if st.button('Positive tests Ratio'):
        st.write(f'Positive test ratio from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['metrics.testPositivityRatio'] != 0]
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="metrics.testPositivityRatio")
        st.pyplot(f)

with col4:
    if st.button('Vaccinated initiated ratio'):
        st.write(f'Vaccinated initiated from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("dark"):
            df_graph = df_result[df_result['metrics.vaccinationsInitiatedRatio'] != 0]
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

# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)  # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats


playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
#selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
#selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write(
    'Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)


# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href


st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
# if st.button('Intercorrelation Heatmap'):
#     st.header('Intercorrelation Matrix Heatmap')
#     df_selected_team.to_csv('output.csv', index=False)
#     df = pd.read_csv('output.csv')
#
#     corr = df.corr()
#     mask = np.zeros_like(corr)
#     mask[np.triu_indices_from(mask)] = True
#     with sns.axes_style("white"):
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
#     st.pyplot()

st.line_chart(tickerDF.Close)

st.write("""
**Volume**""")
st.line_chart(tickerDF.Volume)


