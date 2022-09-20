import os
from pprint import pprint
from matplotlib import pyplot as plt
import numpy as np
import csv
import pandas as pd
import seaborn as sns
import re
import matplotlib.ticker as ticker


def plot_matplot():
    directory = 'frequency-csv'

    group_labels = ['Website', 'Year', 'Rating']
    df = pd.read_csv('frequency-csv/rating_scales.csv')
    df = df[df.Year > 2015]
    df = df.reset_index(drop=True)

    # number_of_websites = 3  # count the amount of fact checking websites and make this amount of rows
    # number_of_years = 5  # count the amount of years (2015-2022) and make this columns

    # fig, axs = plt.subplots(number_of_websites, number_of_years)

    cp = sns.catplot(data=df, y='Frequency', x='Rating', col='Year',
                     kind='bar', errorbar=None, orient='v')

    cp.fig.subplots_adjust(top=0.96)
    # cp.fig.suptitle(f'{title} Ratings')

    cp.tick_params('x', labelrotation=45)

    # for ax in cp.axes:
    #     for patch in ax.patches:
    #         current_width = patch.get_width()
    #         diff = current_width - 20
    #
    #         patch.set_width(20)
    #
    #         patch.set_x(patch.get_x() + diff * .5)

    print(cp.axes)
    print(cp.axes_dict)

    # for subplots in cp.fig.subplots():
    #     subplots.tick_params('x', labelrotation=45)

    # plt.subplots_adjust(hspace=0.2)
    # plt.savefig(f'{title}.png')

    # plt.tight_layout()
    plt.show()


def plot_seaborn():
    directory = 'frequency-csv'
    for filename in os.listdir(directory):
        if 'csv' not in filename or 'rating_scales' in filename:
            continue

        print(filename)
        group_labels = ['Website', 'Year', 'Rating']
        title = re.split("\W+|_", filename)[0].upper()
        df = pd.read_csv(f'{directory}/{filename}')
        df = df[df.Year > 2015]
        df = df.reset_index(drop=True)

        cp = sns.catplot(data=df, y='Frequency', x='Rating', col='Year',
                         kind='bar', errorbar=None, orient='v')

        cp.fig.subplots_adjust(top=0.96)
        cp.fig.suptitle(f'{title} Ratings')

        labels = cp.axes[-1][0].get_xticklabels()
        ticks = cp.axes[-1][0].get_xticks()
        print(labels)

        for ax in cp.axes.flatten():
            print(type(ax))
            plt.setp(ax.set_xlabel("Frequency"), visible=True)
            plt.setp(ax.set_xticks(ticks), visible=True)
            plt.setp(ax.set_xticklabels(labels), visible=True, rotation=67.5)
            print(ax.get_xticklabels())

        plt.subplots_adjust(hspace=0.2)
        # plt.savefig(f'../../plots/{title}.png')
        plt.savefig(f'../../plots/{title}.png', bbox_inches='tight')
        # plt.tight_layout()
        # plt.autoscale()
        plt.show()


def main():
    # plot_matplot()
    plot_seaborn()


if __name__ == "__main__":
    main()
