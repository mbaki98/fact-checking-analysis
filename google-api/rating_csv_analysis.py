import os
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np
import csv
import pandas as pd
import seaborn as sns
import re
import matplotlib.ticker as ticker


def plot():
    directory = 'frequency-csv'
    for filename in os.listdir(directory):
        if 'csv' not in filename or 'rating_scales' in filename:
            continue

        print(filename)
        group_labels = ['Website', 'Year', 'Rating']
        title = re.split("\W+|_", filename)[0].upper()
        df = pd.read_csv(f'{directory}/{filename}')

        cp = sns.catplot(data=df, x='Frequency', y='Rating', row='Year',
                         kind='bar', errorbar=None)

        cp.fig.subplots_adjust(top=0.96)
        cp.fig.suptitle(f'{title} Ratings')

        labels = cp.axes[-1][0].get_xticklabels()
        ticks = cp.axes[-1][0].get_xticks()
        print(labels)

        for ax in cp.axes.flatten():
            print(type(ax))
            plt.setp(ax.set_xlabel("Frequency"), visible=True)
            plt.setp(ax.set_xticks(ticks), visible=True)
            plt.setp(ax.set_xticklabels(labels), visible=True)
            print(ax.get_xticklabels())

        plt.subplots_adjust(hspace=0.2)
        plt.savefig(f'{title}.png')
        plt.show()


def main():
    plot()


if __name__ == "__main__":
    main()
