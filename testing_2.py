# importing show from bokeh.io
# to show the button
from bokeh.io import show

# importing button and customJS package
# from bokeh.models
from bokeh.models import Button, CustomJS

# Creating a button variable where
# we are specifying the properties of the
# button such as label on the button and
# the button type(Different color)
button = Button(label = "Click on the button",
				button_type = "danger")

# js_on_click sets up a javascript handler
# for state changes and also when we
# are clicking on the button. a message
# is printed on the console
button.js_on_click(CustomJS(code = "console.log('button: You have clicked on the button!')"))

# showing the above button
show(button)
