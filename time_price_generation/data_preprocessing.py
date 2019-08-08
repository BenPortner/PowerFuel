import pandas as pd

sFile = "OPSD_time_series_60min_singleindex.csv"
df = pd.read_csv(sFile, parse_dates=['utc_timestamp'])

df_filtered = df[[
    "utc_timestamp",
    'DE_price_day_ahead',
    'DE_solar_generation_actual',
    'DE_wind_generation_actual'
]].copy()

# add column wind + solar
df_filtered["DE_wind_plus_solar_generation_actual"] = df_filtered['DE_solar_generation_actual'] + df_filtered['DE_wind_generation_actual']

# filter for year 2017
start_date = "2017-01-01"
end_date = "2018-01-01"
df_2017 = df_filtered[(df_filtered["utc_timestamp"] >= start_date) & (df_filtered["utc_timestamp"] < end_date)]

# write csv
df_2017.to_csv("date_price_generated_DE_2017.csv", index=False)
pass