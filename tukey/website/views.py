from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import string

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

def whats_tukey_test(request):
    return render(request, 'whats-tukey-test.html')

def about_tool(request):
    return render(request, 'about-tool.html')


def create_table(request):
    global k, n, alfa, q, table

    k = int(request.GET['k'])
    n = int(request.GET['n'])
    alfa = float(request.GET['alfa'])

    items = [k, k * n - k]
    q = get_q(items)
    table = generate_matrix(n, k)

    data = {'k': k,
            'n': n,
            'alfa': alfa,
            'q': q,
            'items': items,
            'table': table}

    return render(request, 'step2.html', data)


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
    generate_graphic(descending_averages)

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
            'mq_in': mq_in,
            'columns': len(average)}

    return render(request, 'results.html', data)


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
                difference = np.around(average[j-1] - average[i], 3)
                if((j-1) <= i):
                    difference = '-'
                else:
                    if (difference < 0):
                        difference = np.around(difference * (-1), 3)

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
    previous_codes = list(string.ascii_lowercase)
    codes = [''] * k

    for i in range(k): # pega todos os elementos, começando do
        if i < k:
            codes[i] = codes[i] + previous_codes[0]
        for j in range(i+1, k): # pega os "proximos" elementos. ex: se o "i" é o 0, aqui o "j" vale 1, 2, 3, 4, 5
            if descending_averages[i] <= (descending_averages[j]+hsd): #compara o i com cada um dos j
                codes[j] = codes[j] + previous_codes[0] # aqui ele atribui o código pro índice do elemento "atual"
            else:
                codes[j] = codes[j] + ''
        previous_codes.pop(0)


    return codes


def get_table_values(request):
    repetitions = np.zeros((n, k))
    get_data = request.GET.dict()

    for j in range(n):
        for i in range(k):            
            repetitions[j][i] = float(get_data.get('cell_'+str(j)+'_'+str(i)))

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


def get_q(items):
    csv = pd.read_csv('website/static/csv/alfa_{}.csv'.format(alfa))
    k = items[0] # verificar o que fazer caso for maior que 100
    df = items[1] - 1  # verificar o que fazer caso for maior que 120, usar inf?

    q = np.around(csv[csv.columns[k]][df], 3)

    return 'Valor desconhecido' if np.isnan(q) else q


def generate_graphic(average):
    index = ['']

    for i in range(len(average)):
        index.append(i + 1)
        plt.bar(i + 1, average[i])
  
    plt.axis([0, len(average) + 1, 0, max(average) + 1])
    plt.title("Médias")
    plt.xlabel("Quantidade")
    plt.ylabel("Valor")
    plt.savefig('website/static/images/grafic.png')
    plt.close()