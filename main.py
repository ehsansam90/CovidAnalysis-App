import os
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import numpy as np
import plotly.graph_objects as go
from matplotlib.patches import Circle



from dotenv import load_dotenv
load_dotenv()



st.set_page_config(
    page_title="Covid 19 Analysis across US",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        body {
            background-color: #FFFFFF;  /* Set your preferred background color here */
            color: #262730;  /* Set your preferred text color here */
        }
    </style>
    """,
    unsafe_allow_html=True,
)


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
 'metrics.vaccinationsInitiatedRatio','metrics.vaccinationsCompletedRatio','actuals.deaths','actuals.vaccinationsCompleted','date']
states = {'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AS': 'American Samoa', 'AZ': 'Arizona', 'CA': 'California',  'CO': 'Colorado', 'CT': 'Connecticut', 'DC': 'District of Columbia',  'DE': 'Delaware', 'FL': 'Florida',  'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii','IA': 'Iowa','ID': 'Idaho','IL': 'Illinois','IN': 'Indiana','KS': 'Kansas','KY': 'Kentucky','LA': 'Louisiana','MA': 'Massachusetts','MD': 'Maryland','ME': 'Maine','MI': 'Michigan','MN': 'Minnesota','MO': 'Missouri','MP': 'Northern Mariana Islands','MS': 'Mississippi','MT': 'Montana','NA': 'National','NC': 'North Carolina','ND': 'North Dakota','NE': 'Nebraska','NH': 'New Hampshire','NJ': 'New Jersey','NM': 'New Mexico','NV': 'Nevada','NY': 'New York','OH': 'Ohio','OK': 'Oklahoma','OR': 'Oregon','PA': 'Pennsylvania','PR': 'Puerto Rico','RI': 'Rhode Island','SC': 'South Carolina','SD': 'South Dakota','TN': 'Tennessee','TX': 'Texas','UT': 'Utah','VA': 'Virginia','VI': 'Virgin Islands','VT': 'Vermont','WA': 'Washington','WI': 'Wisconsin','WV': 'West Virginia','WY': 'Wyoming'}

st.title('🦠Covid 19 Analysis across US 🦠 ')
st.markdown("""
 **This web application would provide analysis on real time data related to Covid across all states located in United states**.\n
 First part, A graphical representation of the distribution of infection and vaccination rates in various states at different times can be generated by selecting a specific date and feature.
 \nBefore beginning the second part of analysis, it is important to specify the time range and location for the data collection. 
 This can be done by defining the desired time frame and selecting the specific state of interest in the sidebar. 
 Additionally, the CSV file containing the specified data can also be downloaded for further analysis. 
 * Data source: [covidactnow.org/](https://covidactnow.org/) \n\n---""")

st.write("**Geographic Heat Map related to Vaccination and infection ratio**")
today = datetime.date.today()
date_map = st.slider(
    "**Specific time in range from 03/01/2020 to Today**", datetime.datetime.strptime('01032020', "%d%m%Y").date(), today,
    value=datetime.datetime.strptime('01032020', "%d%m%Y").date(),
    format="MM/DD/YY")

selected_feature = st.selectbox('Geomap Graphical about:', ["infection Rate","Vaccination Rate"])
dict={"Vaccination Rate":"metrics.vaccinationsInitiatedRatio","infection Rate":"metrics.infectionRate"}

df_map = df.reset_index()
df_map_result = df_map[df_map['date'] == str(date_map)]
df_map_result.loc[df_map_result.index, 'text'] = "States: " + df_map_result['state']
fig = go.Figure(data = go.Choropleth(locations=df_map_result['state'], z= df_map_result[dict[selected_feature]].astype(float),
                                   locationmode="USA-states",colorscale='Reds',colorbar_title= selected_feature,text=df_map_result['text']))
fig.update_layout(title_text = f'Distribution of {selected_feature} at {date_map}', geo_scope='usa', height=600, width=1000 )

st.plotly_chart(fig)




#st.sidebar.header('User Input Features')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2020))))
start_date = st.sidebar.date_input('Start date', (today - datetime.timedelta(days = 30)))
end_date = st.sidebar.date_input('End date', today)

if start_date < end_date:
    st.success('Data from " `%s`" to " `%s` "' % (start_date, end_date))
elif end_date > datetime.date.today():
    st.error('End date must fall in today or before')
else:
    st.error('Error: End date must fall after start date.')

selected_state = st.sidebar.selectbox('State', df.state.unique())

#slider for picking a date
# try:
#     start_time = st.slider(
#         "**Select a specific date in range**", start_date, end_date,
#         value=start_date,
#         format="MM/DD/YY")
#     st.write(f"Number of new cases in {selected_state} at {str(start_time)} are:  ",
#              df.groupby("date").sum()['actuals.newCases'][str(start_time)])
#     st.write("\n")
# except:
#     st.error('Values are not correct')


top_10 = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI"]
df_top_10 = df[df['state'].isin(top_10)]

grouped_data_death = df_top_10.groupby("state")['actuals.deaths'].sum()
grouped_data_vac = df_top_10.groupby("state")['actuals.vaccinationsCompleted'].sum()


st.title('Donut Chart of Total vaccinated and Deaths in top 10 populated States')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Creating the donut chart with a thicker circle using Matplotlib
ax1.pie(grouped_data_death, labels=grouped_data_death.index, autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth': 5, 'edgecolor': 'white'})
center_circle = Circle((0, 0), 0.4, color='white')  # Increase the radius to make it thicker
ax1.add_artist(center_circle)  # Adding a thicker white circle to create a donut chart
ax1.set_title('Total Deaths by State')

ax2.pie(grouped_data_vac, labels=grouped_data_vac.index, autopct='%1.1f%%', startangle=90, wedgeprops={'linewidth': 5, 'edgecolor': 'white'})
center_circle = Circle((0, 0), 0.4, color='white')  # Increase the radius to make it thicker
ax2.add_artist(center_circle)  # Adding a thicker white circle to create a donut chart
ax2.set_title('Total Vaccinated by State')

plt.tight_layout()

st.pyplot(fig)




result = df.groupby('state').agg({'actuals.cases': 'sum', 'actuals.deaths': 'sum'}).reset_index()
result['cases'] = result['actuals.cases'] / result['actuals.cases'].sum() * 100
result['deaths'] = result['actuals.deaths'] / result['actuals.deaths'].sum() * 100

# Streamlit app
st.title('Side-by-Side Percentage Bar Plot for all states')

fig, ax = plt.subplots(figsize=(20, 10))  # Increased figure width

bars_cases = ax.bar(result['state'], result['cases'], label='Total Cases Percentage', width=0.6, align='edge')  # Increased width

bars_deaths = ax.bar(result['state'], result['deaths'], label='Deaths Percentage', width=-0.6, align='edge', alpha=0.7)  # Increased width

ax.set_facecolor('white')
ax.set_xlabel('State')
ax.set_ylabel('Percentage')
ax.set_title('Percentage bar for distribution of Total new cases and new death per State')
ax.legend()

for bar in bars_cases:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', color='black')

for bar in bars_deaths:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom', color='black')

st.pyplot(fig)
df = df[columns]
df.index = pd.to_datetime(df.date)
df = df[df.state == selected_state]
df_result = df[start_date:end_date]
columns_to_fill = ['actuals.deaths', 'actuals.vaccinationsCompleted']
df_result[columns_to_fill] = df_result[columns_to_fill].fillna(0)



#plotting
st.write(f"2. Real time analysis from {str(start_date)} to {str(end_date)} in {selected_state} is provided in following:")

col1, col2, col3= st.columns([10,10,10])
with col1:
    if st.button('All the cases'):
        st.write(f'New Cases trend from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("white"):
            df_graph = df_result[df_result['actuals.cases'] != 0]
            df_graph['actuals.cases'] = df_graph['actuals.cases'].dropna()
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="actuals.cases")
        st.pyplot(f)

with col2:
    if st.button('Positive tests Ratio'):
        st.write(f'Positive test ratio from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("white"):
            df_graph = df_result[df_result['metrics.testPositivityRatio'] != 0]
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="metrics.testPositivityRatio")
        st.pyplot(f)
#col3 = st.columns([10,10])
# with col3:
#     if st.button('Positive tests Ratioo'):
#         st.write(f'Positive test ratio from _{start_date}_ to _{end_date}_:')

#         with sns.axes_style("dark"):
#             df_graph = df_result[df_result['metrics.testPositivityRatio'] != 0]
#             f, ax = plt.subplots(figsize=(7, 5))
#             ax = sns.lineplot(data=df_graph, x=df_graph.index, y="metrics.testPositivityRatio")
#         st.pyplot(f)

with col3:
    if st.button('Vaccinated initiated ratio'):
        st.write(f'Vaccinated initiated from _{start_date}_ to _{end_date}_:')

        with sns.axes_style("white"):
            df_graph = df_result[df_result['metrics.vaccinationsInitiatedRatio'] != 0]
            f, ax = plt.subplots(figsize=(7, 5))
            df_graph['metrics.vaccinationsInitiatedRatio'] = df_graph['metrics.vaccinationsInitiatedRatio'].dropna()
            ax = sns.lineplot(data=df_graph, x=df_graph.index, y="metrics.vaccinationsInitiatedRatio")
        st.pyplot(f)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    
    df_result = df_result.dropna()
    corr = df_result.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
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
    if selected_states:
        st.header(f'Comparison between: {" & ".join([states[state] for state in selected_states])}')

        st.bar_chart(df_result.set_index('state'))
        with sns.axes_style("white"):
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.style.use("classic")
            f, ax = plt.subplots(figsize=(7, 5))
            df_result.plot(x='state', y=["deathRatio", "vaccinatedRatio"], kind="bar", rot=0)
        st.pyplot()

    else:
         st.error("You need to provide some states first on the side bar for performing Comparison ")


        
st.write("Data table Requested as follows:")
st.dataframe(df_result)

st.markdown(filedownload(df_result,start_date,end_date,selected_state), unsafe_allow_html=True)


st.markdown("\n\nCreated by Ehsan S")




