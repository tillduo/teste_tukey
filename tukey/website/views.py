from django.shortcuts import render
import numpy as np

# Global variable
k = None
n = None
alfa = None
table = None
q = None
average = None
variance = None
mq_in = None

# Primary Function
def hello_world(request):
    return render(request, 'index.html')


def create_table(request):
    global k, n, alfa, q, table

    k = int(request.GET['k'])
    n = int(request.GET['n'])
    alfa = float(request.GET['alfa'])
    q = float(request.GET['q'])

    items = [k, k * n - k]
    table = generate_matrix(n, k)

    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'q': q,
            'items': items,
            'table': table}

    return render(request, 'index.html', data)


def calcule_tukey(request):
    global average, variance, mq_in, hsd

    items = [k, k * n - k]
    table_values = get_table_values(request)
    update_table(table_values)
    average = get_average(table_values)
    variance = get_variance(table_values)
    mq_in = get_mq()
    hsd = get_hsd()
    table_differences = generate_matrix_differences(k)
    descending_averages = get_descending_averages(average)
    codes = define_averages_code(descending_averages, k, hsd)

    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'q': q,
            'hsd': hsd,
            'table': table,
            'table_differences': table_differences,
            'average': average,
            'codes': codes,
            'descending_averages': descending_averages,
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


def generate_matrix_differences(k):
    row = []
    list = []
    first = True

    for j in range(k + 1):
        if first:
            row.append('Médias')
        else:
            row.append('Média T{}'.format(j))

        for i in range(k):
            if first:
                row.append('Média T{}'.format(i + 1))
            else:
                difference = average[j-1] - average[i]
                if((j-1) <= i):
                    difference = '-'
                else:
                    if (difference < 0):
                        difference = difference * (-1)

                row.append(difference)

        list.append(row)
        row = []
        first = False
    return list

def get_descending_averages(average):
    ascending_averages = np.sort(average)
    descending_averages = ascending_averages[::-1]
    return descending_averages

def define_averages_code(descending_averages, k, hsd):
    codes = np.full((1,k), 999)

    for i in range(k):
        if(i < k-1):
            if(i == 0):
                codes[0][i] = i
            if(descending_averages[i+1] > (descending_averages[i] - hsd)):
                codes[0][i+1] = i
            if(codes[0][i] == 999):
                codes[0][i] = codes[0][i+1]
        else:
            if(descending_averages[i-1] < (descending_averages[i] + hsd)):
                codes[0][i] = codes[0][i-1]
            else:
                codes[0][i] = i    

    return codes


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


def get_hsd():
    hsd = (float(q) * (np.sqrt(mq_in/n)))

    return np.around(np.nan_to_num(hsd), 3)    


def update_table(repetitions):
    global table

    for j in range(1, n + 1):
        for i in range(1, k + 1):
            table[j][i] = repetitions[j-1][i-1]

    return table
    