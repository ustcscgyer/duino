import seaborn as sns
import matplotlib.pyplot as plt
from ipywidgets import IntProgress, HTML, VBox
from IPython.display import display
import datetime as dt

class ProgressBar:
    def __init__(self, size=100, name='Progress'):
        self.size = size
        self.name = name
        self.t0 = dt.datetime.now()
        progress = IntProgress(min=0, max=size, value=0, bar_style='info')
        label0 = HTML(value='%s: %d / %d' % (self.name, 0, self.size))
        label1 = HTML(value='Time: --')

        self.box = VBox(children=[VBox([label0, label1]), progress])
        display(self.box)

    def set_value(self, value):
        t1 = dt.datetime.now()
        self.box.children[0].children[0].value = '%s: %d / %d' % (self.name, value, self.size)
        self.box.children[0].children[1].value = 'Time: %s' % str(t1-self.t0).split('.')[0]
        self.box.children[1].value = value

class ClassWrapper:
    """ To create an object holding the input value so users can do shallow copy 
    of this input. This faciliates to have two variables pointing to the same physical
    address
    """
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return repr(self.value)