import math
import datetime as dt

import DateTime
import numpy as np
import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import DatePicker, Button, TextInput, MultiChoice



#below function will feed data frame to other functions
def load_data(ticker1, ticker2, start, end):
    #df-> data frame
    df1 = yf.download(ticker1, start, end)
    df2 = yf.download(ticker2, start, end)
    return df1, df2

#we are gonna plot candle stick chart
#in our case we feed data frames to data parameter
#in default sync_axis is None
def plot_data(data, indicators, sync_axis = None):
    df = data
    #in here we will have a couple of days with gains and days without gains(with losses)
    gain = df.Close > df.Open
    #if you have higher price when closing than Open, you will have gain
    loss = df.Open > df.Close
    # if you have higher price when open than close, you will have loss
    width = 12 * 60 * 60 * 1000 #this will be for a half of a day

    if sync_axis is not None:
        p = figure(x_axis_type = "datetime", tools = "pan, wheel_zoom, box_zoom, reset, save", width=1000,
                   x_range = sync_axis)
    else:
        p = figure(x_axis_type = "datetime", tools = "pan, wheel_zoom, box_zoom, reset, save", width=1000)

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.25

    p.segment(df.index, df.High, df.index, df.Low, color = "black")

    #vertical var for every loss and gain, gain -> green("#00ff00"), loss -> red("#ff0000"),
    p.vbar(df.index[gain], width, df.Open[gain], df.Close[gain], fill_color = "#00ff00", line_color = "#00ff00")
    p.vbar(df.index[loss], width, df.Open[loss], df.Close[loss], fill_color="#ff0000", line_color="#ff0000")

    for indicator in indicators:
        if indicator == "30 Day SMA":
            df["SMA30"] = df["Close"].rolling(30).mean()
            p.line(df.index, df.SMA30, color = "purple", legend_label="30 Day SMA")
        elif indicator == "100 Day SMA":
            df["SMA100"] = df["Close"].rolling(100).mean()
            p.line(df.index, df.SMA100, color = "purple", legend_label="100 Day SMA")
        elif indicator == "Linear regression Line":
            par = np.polyfit(range(len(df.index.values)), df.Close.values, 1, full = True)
            slope = par[0][0]
            intercept = par[0][1]
            y_pred = [slope * i + intercept for i in range(len(df.index.values))]
            p.segment(df.index[0], y_pred, df.index[-1], y_pred[-1], legend_label = "Linear regression", color = "red")
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"

    return p

#below function will be triggered when a button is clicked
def on_button_click(ticker1, ticker2, start, end, indicators):
    df1, df2 = load_data(ticker1, ticker2, start, end)
    #plot 1
    p1 = plot_data(df1, indicators)
    p2 = plot_data(df2, indicators, sync_axis=p1.x_range)
    curdoc().clear()
    curdoc().add_root(layout)
    curdoc().add_root(row(p1, p2))

#for these given default values are stock1, stock2
stock1_text = TextInput(title = "Stock 1")
stock2_text = TextInput(title = "Stock 2")

#strftime -> provide date in a specific string format, given values for arguments are default ones
date_picker_from = DatePicker(title = "Start Date", value = "2020-01-01", min_date = "2000-01-01",
                              max_date = dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title = "End Date", value = "2020-02-01", min_date = "2000-01-01",
                              max_date = dt.datetime.now().strftime("%Y-%m-%d"))

#instead of just plotting stock price, we want to plot indicators, (in here we can do technical analysis as well)
#but this program will do,
#choices -> 30day moving average, 100 day moving average, linear regression
# Now we create indicator choice element
indicator_choice = MultiChoice(options = ["100 Day SMA", "30 Day SMA", "Linear Regression Line"])
#when these options are triggered , it will go to on_button_click function

#below button type is a green button
load_button = Button(label = "Load Data", button_type = "success")


load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value,
                                            date_picker_from.value, date_picker_to.value,
                                            indicator_choice.value))


#now the layout
#the cloumn layout will be stacked over eachother
layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)

curdoc().clear()
curdoc().add_root(layout)

#testing
"""on_button_click("GOOG", "MSFT",
                    "2020-01-01", "2021-01-01",
                    ["100 Day SMA", "30 Day SMA", "Linear Regression Line"]
                )"""




#To run this we need a bokeh server
#to do that,
# open cmd
# go to your program directory,
# type-> bokeh serve --show main.py
# the main.py is the python files name,

#if this doesnt work just click ctrl+w and again click ctrl+shift+t
