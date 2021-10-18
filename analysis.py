import numpy as np
import pandas
import matplotlib.pyplot as plt

from scrape import *
from sklearn.preprocessing import MinMaxScaler



def plot_dataframe(data, x_axis, y_axis):
    data.plot(y=y_axis, x=x_axis, kind='scatter')


def minmaxscale(data):
    data_numbers = data.drop(["Name", "Birth", "wikilink", "career_titles"], axis=1)
    arr = data_numbers.to_numpy()
    trans = MinMaxScaler()
    arr = trans.fit_transform(arr)
    data_scaled = pandas.DataFrame(arr, columns=['career_record', 'highest_ranking'])
    return data_scaled

def gradient_descent(data_scaled):
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

    for i in range(5):
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
