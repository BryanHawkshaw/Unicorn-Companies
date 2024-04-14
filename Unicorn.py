# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import datetime as datetime

# %%
df_companies = pd.read_csv("Unicorn_Companies.csv")

# %%
df_companies.head(10)

# %%
df_companies.shape

# %%
df_companies.info()

# %%
df_companies.describe()

# %%
df_companies['Year Joined'] = pd.to_datetime(df_companies['Date Joined']).dt.year

# %%
def str_to_num(x):
    x = x.strip('$B')
    x = int(x)
    
    return x

# %%
df_companies['Valuation_Num'] = df_companies['Valuation'].apply(str_to_num)
df_companies[['Valuation', 'Valuation_Num']].head()

# %%
df_companies.isna().sum()

# %%
mask = df_companies.isna()
mask.tail()

# %%
mask = mask.any(axis=1)
mask.head()

# %%
df_missing_rows = df_companies[mask]
df_missing_rows


# %%
count_total = df_companies.size
count_total

# %%
count_dropna_rows = df_companies.dropna().size
count_dropna_rows

# %%
count_dropna_columns = df_companies.dropna(axis=1).size
count_dropna_columns

# %%
percentage_rows = ((count_total - count_dropna_rows) / count_total) * 100
print(f'Percentage removed, rows: {percentage_rows:.3f}')


percentage_columns = ((count_total - count_dropna_columns) / count_total) * 100
print(f'Percentage removed, columns: {percentage_columns:.3f}')

# %%
df_companies_backfill = df_companies.bfill()

df_companies_backfill.iloc[df_missing_rows.index, :]

# %%
cities = ['Beijing', 'San Francisco', 'London']
mask = (
    (df_companies['Industry']=='Hardware') & (df_companies['City'].isin(cities))
) | (
    (df_companies['Industry']=='Artificial intelligence') & (df_companies['City']=='London')
)

df_invest = df_companies[mask]
df_invest


# %%
national_valuations = df_companies.groupby(['Country/Region'])['Valuation_Num'].sum().sort_values(ascending=False).reset_index()

national_valuations.head(15)


# %%
mask = ~national_valuations['Country/Region'].isin(['United States', 'United Kingdom', 'China', 'India'])
national_valuations_no_big4 = national_valuations[mask]
national_valuations_no_big4

# %%
sns.barplot(data=national_valuations_no_big4.head(20),
            y='Country/Region',
            x='Valuation_Num')
plt.title('Top 20 non-big-4 countries by total company valuation')



plt.show()

# %%
data = national_valuations_no_big4

px.scatter_geo(data,
               locations='Country/Region',
               size='Valuation_Num',
               locationmode='country names',
               color='Country/Region',
               title='Total company valuations by country (non-big-four)')




