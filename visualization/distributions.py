"""Perform useful descriptive visualizations of variable distributions

Classes:
VarDistributions -- Plot distributions of various variables given a dataframe
"""

import pandas as pd
import numpy as np


class VarDistributions():
    """Plot distributions of various variables given a dataframe

    Functions:
    plot_freq -- frequency plots based on variable type(continuous/categorical)
    plot_box -- boxplot for continuous variables
    """

    def __init__(self, df, plot_vars):
        # input dataframe and variables to plot distributions of

        self.data = df
        self.var_list = plot_vars

        # extract column datatypes
        self.col_types = {col: self.data[col].dtype.name
                          for col in self.data.columns.values}

        # assert datatypes can be plotted
        self.error_flag = False
        self.obj_cols = []
        for col in self.var_list:
            if self.col_types[col] == 'object':
                self.obj_cols.append(col)
                self.error_flag = True
        obj_cols_string = '\n'.join([x + '\n' for x in self.obj_cols])
        assert ~self.error_flag,\
            f"Object columns cannot be plotted:{obj_cols_string}"

        # print info about columns not being plotted
        cols_not_plotted = '\n'.join([x + ':' + self.col_types[col] + '\n'
                                     for x in self.data.columns.values
                                     if x not in self.var_list])
        print(f'List of variables excluded:{cols_not_plotted}')

        # TODO test code above
        # TODO add functions for histogram, box plot