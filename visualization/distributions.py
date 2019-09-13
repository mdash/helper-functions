"""Perform useful descriptive visualizations of variable distributions

Classes:
-----------------
VarDistributions -- Plot distributions of various variables given a dataframe
"""

import pandas as pd
import numpy as np

import ipywidgets as widgets
from ipywidgets import HBox, Layout, Output, VBox
from IPython.display import display, clear_output
import qgrid

import plotly
import plotly.graph_objs as go
import plotly.offline as pyo
import plotly.express as px
import plotly.figure_factory as ff

# Set plotly notebook mode to work offline
pyo.init_notebook_mode()


class VarPlots():
    """Plot distributions of various variables given a dataframe

    Functions:
    plot_freq -- frequency plots based on variable type(continuous/categorical)
    plot_box -- boxplot for continuous variables
    """

    def __init__(self, df):
        # input dataframe and variables to plot distributions of

        self.widget_style = {'description_width': 'initial',
                             'widget_width': 'initial'}
        self.data = df
        self.var_list = self.data.columns.values

        # extract column datatypes
        self.col_types = {col: self.data[col].dtype.name
                          for col in self.data.columns.values}

    # TODO add functions for box plot
    def counts_by_column(self):
        # plot histogram or barplot based on input column data type

        # TODO testing
        button = widgets.Button(description="Submit",
                                style=self.widget_style)

        col_picker = widgets.Dropdown(
                                        options=[(x, x)
                                                    for x in self.var_list],
                                        value=self.var_list[0],
                                        description='Select Column:',
                                        style=self.widget_style
                                    )
        chart_picker = widgets.Dropdown(
                                        options=["Bar", "Histogram"],
                                        value="Bar",
                                        description='Select Plot Type:',
                                        style=self.widget_style
                                        )                            
        container = widgets.VBox(children=[col_picker, chart_picker,
                                            button])
        display(container)
        
        def process_data(v):
            # process data and display chart on button click
            
            clear_output()

            select_col = col_picker.value
            select_chart = chart_picker.value
            
            # plot histogram
            fig = go.Figure()
            figx = self.data[select_col].sort_values()
            if len(figx) == np.sum(pd.isnull(figx)):
                string_display = '<br><h4>Column contains only'+\
                                    'null values</h4>'
                text_widg = widgets.HTML(value=string_display)
                container = widgets.VBox(children=[col_picker,
                                                    chart_picker, button,
                                                    text_widg])
                return
            
            # TODO make modular
            if figx.dtype != 'object':
                figx = figx.fillna(0).values
            else:
                figx = figx.fillna('NA').values
            unique, counts = np.unique(figx, return_counts=True)
            
            if select_chart == 'Bar':
                # bin values and plot out charts
                if len(unique) > 7:
                    hist, bins = np.histogram(figx, bins=7)
                    labels = ['{0:.0f}'.format(bins[i]) + '-'
                                + '{0:.0f}'.format(bins[i+1])
                                for i in range(len(bins) - 1)]
                    fig.add_trace(go.Bar(x=labels, y=hist))
                    fig.layout = go.Layout(title={'text': 'Count of records by '+select_col.capitalize().replace('_',' '),
                                                'x': 0.5,
                                                'xanchor': 'center'})
                else: 
                    fig.add_trace(go.Bar(x=unique, y=counts))
                    fig.layout = go.Layout(title={'text': 'Count of records by '+select_col.capitalize().replace('_',' '),
                                                'x': 0.5,
                                                'xanchor': 'center'})
            else:
                # assert object data type can be plotted in histogram
                assert self.col_types[select_col] != 'object',\
                    "Object columns cannot be plotted in histogram."\
                        + "Please reselect the column"
                
                # plot histogram
                fig.add_trace(go.Histogram(x=figx, histfunc='count'))
                fig.layout = go.Layout(title={'text': 'Count of records by '+select_col.capitalize().replace('_',' '),
                                            'x': 0.5,
                                            'xanchor': 'center'})
            string_display = f'<br><h4>Number of unique values: {len(unique)}</h4>'
            text_widg = widgets.HTML(value=string_display)
            container = widgets.VBox(children=[col_picker,
                                                chart_picker, button,
                                                text_widg,
                                                go.FigureWidget(fig)])
            display(container)
        
        button.on_click(process_data)