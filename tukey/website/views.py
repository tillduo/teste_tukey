from django.shortcuts import render
import numpy as np
import statistics as st

# Global variable
k = None
n = None
alfa = None

# Primary Function
def hello_world(request):
    return render(request, 'index.html')



def create_table(request):
    global k
    k = int(request.GET['k'])
    global n
    n = int(request.GET['n'])
    global alfa
    alfa = float(request.GET['alfa'])

    items = [k, k * n - k]

    list = generate_matrix(n, k)

    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'items': items,
            'list': list}

    return render(request, 'index.html', data)


def calcule_average(request):
    repetitions = np.full((n, k), None)
    entry_data_average = np.full((k, 1), float(0))
    entry_data_variance = np.full((k, 1), float(0))
    average = np.full((k, 1), float(0))
    variance = np.full((k, 1), float(0))
    mq_in = float(0)

    # calcula a média
    for j in range(n):
        for i in range(k):
            cell = 'cell_' + str(j) + '_' + str(i)
            
            repetitions = float(request.GET[cell])
            entry_data_average[i] = (float(entry_data_average[i]) + float(request.GET[cell]))

    for i in range(k):
        average[i] = (float(entry_data_average[i]) / n)


    # calcula a variância
    for j in range(n):
        for i in range(k):
            cell = 'cell_' + str(j) + '_' + str(i)
            
            entry_data_variance[i] = (float(entry_data_variance[i]) + float((float(request.GET[cell]) - float(average[i])) * (float(request.GET[cell]) - float(average[i]))))


    for i in range(k):
        variance[i] = (float(entry_data_variance[i]) / (n-1))

    # calcula mq_dentro
    for i in range(k):
        mq_in = mq_in + float(variance[i])    

    mq_in = mq_in / k
    
    # retorna os dados
    data = {
        'table': repetitions,
        'averages': average,
        'variances': variance,
        'mq_in': mq_in
    }

    return render(request, 'index.html', data)


# Secondary Function
def generate_matrix(n, k):
    row = []
    list = []
    first = True

    for j in range(n + 1):
        if first:
            row.append('Repetições')
        else:
            row.append('{}'.format(j))

        for i in range(k):
            if first:
                row.append('T{}'.format(i + 1))
            else:
                row.append('')

        list.append(row)
        row = []
        first = False
    return list
