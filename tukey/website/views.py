from django.shortcuts import render
import numpy as np
import pandas as pd

# global variable
k = None
n = None
alfa = None
table = None
average = None
variance = None
mq_in = None

# Primary Function
def hello_world(request):
    return render(request, 'index.html')


def create_table(request):
    global k, n, alfa, table
    k = int(request.GET['k'])
    n = int(request.GET['n'])
    alfa = float(request.GET['alfa'])

    generate_matrix()

    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'table': table}

    return render(request, 'index.html', data)


def calcule_tukey(request):
    global k, n, alfa, table, average, variance, mq_in 

    get_average()
    get_variance()
    get_mq()
    
    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'table': table,
            'average': average,
            'variance': variance,
            'mq_in': mq_in}

    return render(request, 'index.html', data)


# Secondary Function
def generate_matrix():
    global table
    table = pd.DataFrame()

    for i in range(1, max(k, n) + 1):
        if n >= i:
            table['T{}'.format(i)] = np.nan
        if k >= i:
            table.loc[i] = np.nan

    return table


def get_table_values():
    global table

    for j in range(n):
        for i in range(k):
            cell = 'cell_' + str(j) + '_' + str(i)      
            table[table.column[i]][j] = float(request.GET[cell])
            # ou table[table.column[j]][i] = float(request.GET[cell])
      
    return table


def get_average():
    global average, table
    average = []

    for i in range(max(k, n)):
        average.append(table[table.columns[i]].mean())
    
    return average


def get_variance():
    global variance, table
    variance = []

    for i in range(max(k, n)):
        variance.append(table[table.columns[i]].var() / table[table.columns[i]].size)
  
    return variance

def get_mq():
    global mq_in, variance
    mq_in = sum(variance) / len(variance)
  
    return mq_in