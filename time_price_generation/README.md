For a version including figures, click here: https://nbviewer.jupyter.org/github/BenPortner/PowerFuel/blob/master/time_price_generation/index.html


# <span style="line-height:1.5"> An exploration of solar- and wind electricity generation in Germany in 2017 - How much? When? Market prices. Surplus.</span>

Author: Benjamin W. Portner, Bauhaus Luftfahrt e.V., Willy-Messerschmitt-Straße 1, 82024 Taufkirchen

<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Abstract" data-toc-modified-id="Abstract-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Abstract</a></span></li><li><span><a href="#Introduction" data-toc-modified-id="Introduction-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Introduction</a></span></li><li><span><a href="#Methodology" data-toc-modified-id="Methodology-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Methodology</a></span></li><li><span><a href="#Power-generation-time-series" data-toc-modified-id="Power-generation-time-series-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Power generation time series</a></span><ul class="toc-item"><li><span><a href="#Solar" data-toc-modified-id="Solar-4.1"><span class="toc-item-num">4.1&nbsp;&nbsp;</span>Solar</a></span></li><li><span><a href="#Wind" data-toc-modified-id="Wind-4.2"><span class="toc-item-num">4.2&nbsp;&nbsp;</span>Wind</a></span></li><li><span><a href="#Solar-plus-wind" data-toc-modified-id="Solar-plus-wind-4.3"><span class="toc-item-num">4.3&nbsp;&nbsp;</span>Solar plus wind</a></span></li></ul></li><li><span><a href="#Market-price-time-series" data-toc-modified-id="Market-price-time-series-5"><span class="toc-item-num">5&nbsp;&nbsp;</span>Market price time series</a></span></li><li><span><a href="#Market-price-histogram" data-toc-modified-id="Market-price-histogram-6"><span class="toc-item-num">6&nbsp;&nbsp;</span>Market price histogram</a></span></li><li><span><a href="#Cumulated-data" data-toc-modified-id="Cumulated-data-7"><span class="toc-item-num">7&nbsp;&nbsp;</span>Cumulated data</a></span></li></ul></div>

## Abstract
This document explores solar- and wind electricity generation in Germany in the year 2017. All analyses are based on open-source data obtained from the Open Power System Data project. In total, 36 TWh of solar electricity were produced. The mean hourly solar power generation was 4,1 GW. Electricity generation from wind power yielded 103 TWh in total, with a mean hourly generation of 11,7 GW. As expected, solar generation data exhibits a strong seasonality and day-night cycles. Seasonality in the wind data is less pronounced, although peaks are more frequent in autumn and winter. Similarly, all market price maxima are located in autumn and winter. A strong negative correlation between power generation and market prices is observed. Market prices are less volatile in summer, compared to the rest of the year. In fact, generation peaks do not seem to affect prices between June and August, but strongly affect them in other months. Market prices were negative for 150 hours during the year. Electricity generated during those hours is defined as surplus. The total surplus was 4.9 TWh (3.5% of combined generation). 

The presented document contains interactive plots which contain additional data. Feel free to zoom, pan and hover over data points to explore. Furthermore, by extending the python code contained in this document, readers should be able to easily manipulate the datasets and use them for their own analyses.

Note: Code cells are hidden by default. In order to make them visible, press the "Show Code" button at the top of the document. Furthermore, I exported all plot functions to <a href="https://github.com/Pommespapst/OPSD_analysis/blob/master/notebook_helpers.py">a separate script</a> to make the document more readable.

## Introduction

Of all the challenges faced during Germany's Energiewende, the intermittent nature of solar- and wind power might be the biggest one. Consequently, it is a much-debated topic in politics and science alike. Discussions can only yield meaningful results if they are based on solid data. This document aims to contribute by answering the following questions:

- How much solar- and wind electricity (MWh) was generated in which hour of the year 2017?
- What was the price (€/MWh) of that electricity on the day-ahead spot market?
- How much surplus electricity was available?


## Methodology

All data was sourced from the Open Power System Data project (OPSD, https://open-power-system-data.org/). OPSD provides data concerning the generation, consumption, and pricing of solar- and wind electricity for most members of the European Network of Transmission System Operators for Electricity (ENTSOE) for the years 2006 - 2018. For this document, I use their hourly-resolved data (<a href="https://data.open-power-system-data.org/time_series/2019-06-05/time_series_60min_singleindex.csv">Link</a>). This dataset provides more data than needed, so preprocessing was applied. All steps from the downloaded file to the final CSV used in this document are documented in <a href="https://github.com/Pommespapst/OPSD_analysis/blob/master/data_preprocessing.py">data_preprocessing.py</a>.

The final CSV is loaded into Pandas dataframe. The first lines look as follows:


```python
# loading the csv and showing the first few lines
import pandas as pd 
df = pd.read_csv("date_price_generated_DE_2017.csv", parse_dates=['utc_timestamp'])
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>utc_timestamp</th>
      <th>DE_price_day_ahead</th>
      <th>DE_solar_generation_actual</th>
      <th>DE_wind_generation_actual</th>
      <th>DE_wind_plus_solar_generation_actual</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2017-01-01 00:00:00</td>
      <td>20.90</td>
      <td>0.0</td>
      <td>15363.0</td>
      <td>15363.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2017-01-01 01:00:00</td>
      <td>18.13</td>
      <td>0.0</td>
      <td>15080.0</td>
      <td>15080.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2017-01-01 02:00:00</td>
      <td>16.03</td>
      <td>0.0</td>
      <td>14731.0</td>
      <td>14731.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2017-01-01 03:00:00</td>
      <td>16.43</td>
      <td>0.0</td>
      <td>14865.0</td>
      <td>14865.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2017-01-01 04:00:00</td>
      <td>13.75</td>
      <td>0.0</td>
      <td>15254.0</td>
      <td>15254.0</td>
    </tr>
  </tbody>
</table>
</div>



The csv file has five columns: 
- time stamp (hourly resolution)
- day-ahead spot price (€/MWh)
- solar power generation (MW)
- wind power generation (MW)
- total wind + power (MW)

In the following sections, data analysis is performed using Dataframe describe()-functions and bokeh plots. Throghout the document, surplus electricity is defined as the portion of electricity produced during hours when the market price was negative.

## Power generation time series

Note: Click on a legend entry to hide the corresponding line.


```python
# plot 1: electricity generation solar, wind, total over time
from notebook_helpers import *
plotGenerationData(df)
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1118">Loading BokehJS ...</span>
    </div>











  <div class="bk-root" id="8406893a-cc92-47d2-8186-252d3d3c31b1" data-root-id="1002"></div>





### Solar
There are 8760 datapoints, corresponding to the 8,760 hours of one year. The seasonality is clearly visible: more power is generated in summer than in the winter. Upon zooming, the day-night cycles also become visible. Peak power generation occurred on 27 May 2017 at 11:00 when 27,634 MW were generated. Minimum generation was 0 MW during several hours. In fact, 43% of the time, no solar power was generated. Mean solar power generation over the year was 4,096 MW. In total, 36 TWh were produced.

### Wind
There are 8760 datapoints, corresponding to the 8,760 hours of one year. No clear seasonality is visible, although generation peaks occur mainly during the winter months. Peak power generation occurred on 28 October 2017 at 17:00 when 29,231 MW were generated. Minimum generation was 165 MW on 6 July 2017 7:00. Mean wind power generation over the year was 11,720 MW. Mean and peak wind power generation surpass solar generation, due to larger installed capacities. In total, 103 TWh were produced.

### Solar plus wind
Peak power generation occurred on 7 June 2017 at 11:00 and amounted to 51,942 MW. Minimum generation was 312 MW on 8 January 2017 15:00. Mean over the year was 15,816 MW. In total, 139 TWh were produced.

## Market price time series


```python
# plot 2: market price over time
plotPriceData(df)
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1385">Loading BokehJS ...</span>
    </div>











  <div class="bk-root" id="494841e5-fc0c-4656-8ac2-0fcefed7008a" data-root-id="1288"></div>






```python
# additional statistics
df["DE_price_day_ahead"].describe()
```




    count    8760.000000
    mean       34.185533
    std        17.663967
    min       -83.040000
    25%        27.780000
    50%        33.825000
    75%        40.570000
    max       163.520000
    Name: DE_price_day_ahead, dtype: float64



There are 8760 datapoints, one for each hour of the year. Prices fluctuated significantly throughout the year. A few datapoints are in the negative range indicating a surplus of electricity on the market. These will be more-closely quantified in the next sections. The minimum market price was -83.04 €/MWh occurring on 29 October 2017 3:00. The maximum price was 163.52 €/MWh on 24 January 2017 6:00. Interestingly, both the maximum and the minimum occurred in rather "cold" months. The lowest price (i.e. maximum surplus) did not coincide with the maximum of the power generation dataset (7 June, click on "combined generation" in the legend to show data). However, there is a strong negative correlation between both datasets. Market prices were less volatile in summer, compared to the rest of the year. In fact, generation peaks do not seem to affect prices between June and August, but strongly affect them in other months. The mean - i.e. most common - market price was 34.19 €/MWh. The median was 33.82 €/MWh. This is very close to the mean, implying a centered distribution. The standard deviation is 17.66 €/MWh.


```python
# turn-over calculation
df_turnover = df["DE_price_day_ahead"]*df["DE_wind_plus_solar_generation_actual"]
turnover_pos = df_turnover[df_turnover>0].sum()
turnover_neg = df_turnover[df_turnover<0].sum()
print(
    " turnover (positive): " + "%.2e" % turnover_pos + " €\n", 
    "turnover (negative): " + "%.2e" % turnover_neg + " €"
)
```

     turnover (positive): 4.13e+09 €
     turnover (negative): -1.30e+08 €
    

The total turnover (integral of price * combined generation) was 4.26 Bln €. 4.13 Bln were traded at a positive price, 130 Mio at a negative price.

## Market price histogram


```python
# plot 3: market price histogram
makePriceHistogram(df)
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1652">Loading BokehJS ...</span>
    </div>











  <div class="bk-root" id="509c14bb-1dda-445d-a21b-d127bcbf4cb3" data-root-id="1580"></div>





Plot 3 shows the frequency of day-ahead prices in 2017. Prices are sorted in bins with a width of 5€. Bars show the frequency of each bin normalized by the total number of hours of the year (How often did price-range x occur?, left axis). The yellow curve shows the integrated frequency (How long was the price below x?, right axis). The data is approximately normal-distributed. 30-35 €/MWh is the most frequent bin. 4.1% of the year, prices were in this range. 0 €/MWh has a cumulated relative frequency of 0.017. Hence, 1.7% of the year (150 hours), prices were in the negative range. There is a "dent" in the bar graph and in the line around 15-20 €/MWh. This price range occurred less frequently than expected. To be investigated!

## Cumulated data


```python
# plot 4: cumsums
df_edge_prices = getEdgePriceStats(df, bin_width=1)
plotEdgePriceStats(df_edge_prices)
```



    <div class="bk-root">
        <a href="https://bokeh.pydata.org" target="_blank" class="bk-logo bk-logo-small bk-logo-notebook"></a>
        <span id="1873">Loading BokehJS ...</span>
    </div>











  <div class="bk-root" id="5ca224d4-c1ee-4886-b58e-d1f4dcbea960" data-root-id="1786"></div>





The three lines answer three different questions: 
- How much time of the year (%) was the market price below x? (blue, identical to the yellow line in plot 3)
- How much energy (MWh) was generated at a market price below x? (yellow)
- How much would it cost (€) to buy all generated electricity available for prices cheaper than x? (green)

Market prices were negative during 150 hours of the year. The renewable electricity generated in these hours amounts to 4.86 TWh, representing 3.51% of all wind- and solar electricity generated in 2017. The cumulated value of this electricity was -130.39 Mio €.

Net zero value is reached around 12.5 €/MWh. I.e. if one had bought all solar- and wind electricity available on the market for less than 12.5 €/MWh, one would have earned 130.39 Mio € from removing surplus electricity and spent 130.39 Mio € on non-surplus electricity, making the total (21.51 TWh) effectively free.
