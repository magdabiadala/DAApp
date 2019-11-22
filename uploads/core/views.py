from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from scipy import stats
from string import ascii_letters

import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def home(request):
    print('Home')
    return render(request, 'home.html')


def about(request):
    print('About')
    return render(request, 'about.html')


def contact(request):
    print('Contact')
    return render(request, 'contact.html')


def data_analysis(request):
    print('Data analysis')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        print('\nWhat is `myfile`?')
        print(type(myfile))

        print('\nDirectly accessing `myfile` gives nothing :(')
        print(type(str(myfile.read())))
        print(str(myfile.read()))

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        print('\nHowever, when using FileSystemStorage...')
        print('\nReading filename: %s' % filename)
        print(type(fs.open(filename)))
        print(fs.open(filename))

        print('\nOpen and preview using pandas:')
        df = pd.read_csv(fs.open(filename))
        print(df)

        print('\nOr with CSV module:')
        with fs.open(filename, 'rt') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                print(row)

        print('Data analysis')

        sns.set(style="white")

        corr = df.corr()

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(11, 9))

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)

        # Draw the heatmap with the mask and correct aspect ratio
        matrix = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})


        matrix.figure.savefig(r'C:\Users\Magda\Desktop\kogni\KCK\DAApp\static\img\matrix.png')

        r_table = df.corr()
        p_table = df.apply(lambda x: df.apply(lambda y: r_xor_p(x, y,
                                                                r_xor_p='p')))

        return render(request, 'data_analysis.html',
                      {'result_present': True,
                       'results': {'r_table': r_table.to_html(),
                                   'p_table': p_table.to_html()},
                       'df': df.to_html()})

    return render(request, 'data_analysis.html')


def r_xor_p(x, y, r_xor_p='r'):
# Pearson's r or its p
#    Depending of what you would like to get.
    r, p = stats.pearsonr(x, y)

    if r_xor_p == 'r':
        return r
    else:
        return p
