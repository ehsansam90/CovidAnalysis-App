import requests
import pandas as pd

key = "2a9512d3a2a949aba660af647b042d1a"
url = "https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=" + key    #getting current data
url_current = "https://api.covidactnow.org/v2/states.csv?apiKey=" + key

#r = requests.get(url).content
df = pd.read_csv(url_current)
df.to_csv("test2.csv")

print(df["actuals.cases"])

