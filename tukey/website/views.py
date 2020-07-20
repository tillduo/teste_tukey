from django.shortcuts import render
import numpy as np

# Global variable
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

    items = [k, k * n - k]
    table = generate_matrix(n, k)

    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'items': items,
            'table': table}

    return render(request, 'index.html', data)


def calcule_tukey(request):
    global average, variance, mq_in

    items = [k, k * n - k]
    table_values = get_table_values(request)
    update_table(table_values)
    average = get_average(table_values)
    variance = get_variance(table_values)
    mq_in = get_mq()
    
    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'table': table,
            'average': average,
            'variance': variance,
            'mq_in': mq_in}

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
                row.append('0')

        list.append(row)
        row = []
        first = False
    return list


def get_table_values(request):
    repetitions = np.zeros((n, k))

    for j in range(n):
        for i in range(k):            
            repetitions[j][i] = float(request.GET['cell_' + str(j) + '_' + str(i)])

    return repetitions


def get_average(repetitions):
    entry_data_average = []

    for j in range(k):
        averages = []
        for i in [cell[j] for cell in repetitions]:           
            averages.append(float(i))
        entry_data_average.append(np.mean(averages))

    return np.around(entry_data_average, 2)


def get_variance(repetitions):
    entry_data_variance = []

    for j in range(k):
        variances = []
        for i in [cell[j] for cell in repetitions]:
            variances.append(i)
        entry_data_variance.append(np.var(variances, ddof=1))

    return np.around(np.nan_to_num(entry_data_variance), 2)


def get_mq():
    mq = np.mean(variance)

    return np.around(np.nan_to_num(mq), 3)


def update_table(repetitions):
    global table

    for j in range(1, n + 1):
        for i in range(1, k + 1):
            table[j][i] = repetitions[j-1][i-1]

    return table
    