import numpy as np
import pandas
import matplotlib.pyplot as plt

from scrape import *
from sklearn.preprocessing import MinMaxScaler


def plot_dataframe(data, x_axis, y_axis):
    x = data[x_axis]
    y = data[y_axis]
    plt.scatter(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title('tennis-stats plot')
    plt.show()


def max(column):
    return column.max(), column.idxmax()

def minmaxscale(data):
    data.astype({'highest_rankings': 'float64'}).dtypes
    data_numbers = data.drop(["Name", "Birth", "wikilink"], axis=1)
    arr = data_numbers.to_numpy()
    trans = MinMaxScaler()
    arr = trans.fit_transform(arr)
    data_scaled = pandas.DataFrame(arr, columns=['career_record', 'highest_ranking'])
    return data_scaled


def gradient_descent(data):
    data_scaled = minmaxscale(data)

    X = data_scaled['career_record']
    Y = data_scaled['highest_ranking']

    # building the model

    m = -4
    c = 0
    k = 1
    L = 0.01
    epochs = 1000

    n = float(len(X))

    Y_pred = k * np.exp(m * X + c)

    for i in range(1000):
        Y_pred = k * np.exp(m * X + c)
        # print(Y_pred)
        # Y_pred = m * X + c # The current predicted value of Y
        D_m = (-2 / n) * sum(X * Y_pred * (Y - Y_pred))  # Derivative wrt m
        # print(D_m)
        D_c = (-2 / n) * sum(Y_pred * (Y - Y_pred))  # Derivative wrt c
        # print(D_c)
        D_k = (-2 / n) * sum((Y_pred / k) * (Y - Y_pred))
        m = m - L * D_m  # Update m
        print(m)
        c = c - L * D_c  # Update c
        k = k - L * D_k

    print(m, c, k)
    Y_pred = k * np.exp(m * X + c)
    plt.scatter(X, Y)
    plt.scatter(X, Y_pred, color='red')
    plt.xlabel('Scaled career record')
    plt.ylabel('Scaled highest ranking')
    plt.title('Curve fitting with gradient descent')
    plt.show()


