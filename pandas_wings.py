#! /usr/bin/env python
from pprint import pprint

import pandas as pd
import matplotlib.pyplot as plt


def ok_comment(comment: pd.Series):
    return ((comment.str.contains("large", na=True) &  ~comment.str.contains("both", na=False))
            | (comment == "")  | (comment == "NA") )


def linespoints_plot_for_each_fairy(df: pd.DataFrame, x_axis: str = 'Age'):
    df.sort_values(['Name', x_axis], ascending=[True, True])
    for key, grp in df.groupby('Name'):
        plt.scatter(grp[x_axis], grp['Mean, both sides'], label=key)
        plt.plot(grp[x_axis], grp['Mean, both sides'], linestyle='-', alpha=0.5)  # Connect points

    plt.title('Scatter plot of smaller wing size (mean) vs age')
    plt.xlabel(x_axis, fontsize=18)
    plt.ylabel('Mean of smaller wing length', fontsize=18)
    plt.legend()
    plt.show()


def main():

    deep_woods_fairies = ['Tiny Sugarbottom', 'Cookie Cinnamondust', 'Onyx Shadowhorn',
                          'Aqua Pumpkinbell', 'Tournant Palmriver', 'Julie Dapplesplash']
    lake_and_marsh_fairies = ['Fifi Flickerwind', 'Flora Hazeltoes', 'Oregano Firetwill', 'Twig Willowfig',
                             'Aven Morningmoon', 'Valorie Grassypond', 'Starfish Turtlefrost',
                             'Trumpet Pepperbutter', 'Lapis Crystalmint', 'Quinn Falconsprout']

    infile = "winglength.xlsx"
    # ampty spaces are used for missing values; we want them to be NA:  keep_default_na=False
    df = pd.read_excel(infile, sheet_name='wing data',  keep_default_na=False)
    # get rid of the legend columns
    df.drop(columns=df.filter(like='Unnamed').columns, inplace=True)
    # inspect the table
    print(df)
    df.to_excel('test.xlsx')
    # list all unique names
    print(pd.unique(df['Name']))
    print()

    # let's say we want only the lower wing stats
    df.drop(columns=df.filter(like='upper').columns, inplace=True)

    # keep only those rows in the dataframe where the elements of the column 'Name'
    # are in the list of lake_and_marsh_fairies
    df = df[df['Name'].isin(lake_and_marsh_fairies)]
    # boolean indexing. - at least one bulls eye should be visible
    df = df[~((df['Left inner wing OK'] == 'N') & (df['Right inner wing OK'] == 'N'))]
    df.to_excel('test.xlsx')
 

########################################
if __name__ == "__main__":
    main()
