from bokeh.models.widgets import Button
from bokeh.io import curdoc

def onclick():
    print('somebody clicked the button and this can be read in the bokeh console')
button = Button(label='Update', button_type='primary')
button.on_click(onclick)

curdoc().add_root(button)