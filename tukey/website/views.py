from django.shortcuts import render
import numpy as np

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
    entry_data = np.full((k, 1), float(0))
    average = np.full((k, 1), float(0))
    variance = np.full((k, 1), float(0))

    for j in range(n):
        for i in range(k):
            cell = 'cell_' + str(j) + '_' + str(i)
            
            repetitions = float(request.GET[cell])
            entry_data[i] = (float(entry_data[i]) + float(request.GET[cell]))

    for i in range(k):
        average[i] = np.average(float(entry_data[i]))

    for i in range(k):
        variance[i] = np.var(float(entry_data[i]))

    data = {
        'table': repetitions,
        'averages': average,
        'variances': variance
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
