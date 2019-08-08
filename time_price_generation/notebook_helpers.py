import numpy as np
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource
from bokeh.palettes import Category10
from bokeh.models.tools import HoverTool
from bokeh.models import LinearAxis, Range1d
import pandas as pd

width = 900
height = 600

def plotGenerationData(df):
    p = figure(title="", x_axis_label='date', x_axis_type='datetime',
               y_axis_label='power generated [MW]', plot_width=width, plot_height=height)
    p.line(x=df["utc_timestamp"], y=df["DE_wind_plus_solar_generation_actual"], line_width=1, alpha=0.7, legend="combined",
           line_color=Category10[3][2])
    p.line(x=df["utc_timestamp"], y=df["DE_wind_generation_actual"], line_width=1, alpha=0.7, legend="wind",
           line_color=Category10[3][1])
    p.line(x=df["utc_timestamp"], y=df["DE_solar_generation_actual"], line_width=1, alpha=0.7, legend="solar",
           line_color=Category10[3][0])



    # add hover tool for data exploration
    p.add_tools(HoverTool(
        tooltips = [
            ("index", "$index"),
            ("time stamp", "@x{%F %T}"),
            ("power", "@y{0.2f} MW")
        ],
        formatters={
            "x": "datetime"
        }
    ))

    # make legend clickable
    p.legend.click_policy = "hide"

    # show graphic
    output_notebook()
    show(p)
    pass

def plotPriceData(df):

    p = figure(title="", x_axis_label='date', x_axis_type='datetime',
               y_axis_label='day-ahead price [€/MWh]', plot_width=width, plot_height=height)

    # combined generation data is muted by default
    p.extra_y_ranges = {"CDF": Range1d(start=0, end=df["DE_wind_plus_solar_generation_actual"].max() * 1.05)}
    p.add_layout(LinearAxis(y_range_name="CDF", axis_label="combined power generation [MW]"), 'right')
    generation = p.line(x=df["utc_timestamp"], y=df["DE_wind_plus_solar_generation_actual"], line_width=1, alpha=0.7, legend="combined generation",
           line_color=Category10[3][2], muted_color=Category10[3][2], muted_alpha=0.2, y_range_name="CDF")
    generation.muted = True

    # price data
    p.line(x=df["utc_timestamp"], y=df["DE_price_day_ahead"], line_width=1, alpha=0.7, legend="market price",
           line_color=Category10[3][0], muted_color=Category10[3][0], muted_alpha=0.2)
    p.y_range = Range1d(
        df["DE_price_day_ahead"].min() * (1 + 0.05), df["DE_price_day_ahead"].max() * (1 + 0.05)
    )

    # add hover tool for data exploration
    p.add_tools(HoverTool(
        tooltips = [
            ("index", "$index"),
            ("date", "@x{%F %T}"),
            ("price", "@y{0.2f} €/MWh")
        ],
        formatters={
            "x": "datetime"
        }
    ))

    # make legend clickable
    p.legend.click_policy = "mute"

    # show graphic
    output_notebook()
    show(p)
    pass

def makePriceHistogram(df, bin_width=5, iNumberQueryPoints=100):

    y_overlimit = 0.01

    # define edges
    price_min = df["DE_price_day_ahead"].min()
    price_max = df["DE_price_day_ahead"].max()
    edge_min = bin_width * np.floor(price_min/bin_width)
    edge_max = bin_width * np.ceil(price_max/bin_width)
    edges = np.arange(edge_min,edge_max+1,bin_width)

    frequ, edges = np.histogram(df["DE_price_day_ahead"], bins=edges, density=True)

    # histogram: freuqency of each price
    c = ColumnDataSource(data=dict(
        top = frequ,
        left = edges[:-1],
        right = edges[1:],
        middle = (edges[:-1] + edges[1:]) / 2
    ))
    p = figure(title="", x_axis_label='day-ahead price [€/MWh]',
               y_axis_label='rel. freuqency [number hours/8760]', plot_width=width, plot_height=height)
    r1 = p.quad(source=c, top="top", bottom=0, left="left", right="right",
           line_color="white", alpha=0.5, legend="rel. frequency")
    p.y_range = Range1d(
        frequ.min() * (1 - y_overlimit), frequ.max() * (1 + y_overlimit)
    )

    # add hover tool for histogram
    p.add_tools(HoverTool(
        renderers=[r1],
        tooltips = [
        ("index", "$index"),
        ("rel. freuqency", "@top"),
        ("(left,middle,right)", "(@left, @middle, @right)"),
    ]))

    # cummulated frequency on second axis
    afPrices = np.sort(np.append(0, np.linspace(price_min, price_max, iNumberQueryPoints)))
    lfAvailability = [(df["DE_price_day_ahead"] <= price).mean() for price in afPrices]
    c = ColumnDataSource(data=dict(
        x = afPrices,
        y = lfAvailability,
    ))
    p.extra_y_ranges = {"CDF": Range1d(start=0, end=1)}
    p.add_layout(LinearAxis(y_range_name="CDF", axis_label="cum. rel. frequency [number hours/8760]"), 'right')
    r2 = p.line(source=c, x = "x", y = "y", line_color="orange", line_width=4, alpha=0.7, legend="cum. rel. frequency", y_range_name="CDF")

    # add hover tool for line
    p.add_tools(HoverTool(
        renderers=[r2],
        tooltips = [
        ("index", "$index"),
        ("price", "@x"),
        ("cum. rel. frequency", "@y"),
    ]))

    # show graphic
    output_notebook()
    show(p)

def getEdgePriceStats(df, bin_width=10):

    # edge prices for which calculation will be done
    price_min = df["DE_price_day_ahead"].min()
    price_max = df["DE_price_day_ahead"].max()
    edge_price_min = bin_width * np.floor(price_min/bin_width)
    edge_price_max = bin_width * np.ceil(price_max/bin_width)
    edge_prices = np.arange(edge_price_min,edge_price_max+1,bin_width)

    # for edge price x, how much time / total energy / total price?
    ld = []
    for edge_price in edge_prices:
        df_edge = df.loc[df["DE_price_day_ahead"] <= edge_price]
        ld.append({
            "price [€/MWh]" : edge_price,
            "total time [h]" : len(df_edge),
            "total energy [MWh]" : sum(df_edge["DE_wind_plus_solar_generation_actual"]),
            "total cost [€]" : sum(df_edge["DE_price_day_ahead"] * df_edge["DE_wind_plus_solar_generation_actual"])
        })

    # convert to dataframe
    df_edge_prices = pd.DataFrame(ld)

    # add normalized values
    df_edge_prices["total time [%]"] = df_edge_prices["total time [h]"] / df_edge_prices["total time [h]"].max() * 100
    df_edge_prices["total energy [%]"] = df_edge_prices["total energy [MWh]"] / df_edge_prices["total energy [MWh]"].max() * 100
    df_edge_prices["total cost [%]"] = df_edge_prices["total cost [€]"] / df_edge_prices["total cost [€]"].max() * 100

    # return result
    return df_edge_prices

def plotEdgePriceStats(df_edge_prices):

    p = figure(title="", x_axis_label='day-ahead price [€/MWh]', y_axis_label='', plot_width=width, plot_height=height)

    # add line for each column
    for i, col in enumerate(df_edge_prices.columns[4:]):

        other_col = [s for s in df_edge_prices.columns if s.split("[")[0] == col.split("[")[0]][0]

        c = ColumnDataSource(data=dict(
            x=df_edge_prices["price [€/MWh]"],
            y=df_edge_prices[col],
            y2=df_edge_prices[other_col]
        ))

        r = p.line(x="x", y="y", line_width=2, alpha=0.7, source=c,
               legend=col, name=col, line_color=Category10[3][i])

        # add hover tool
        p.add_tools(HoverTool(
            renderers = [r],
            tooltips = [
                ("index", "$index"),
                ("price [€/MWh]", "@x{0.2f}"),
                (col, "@y{0.2f}"),
                (other_col, "@y2{0.00 a}")
            ]
        ))

    # show graphic
    output_notebook()
    show(p)
    pass