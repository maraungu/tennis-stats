import numpy as np
import matplotlib.pyplot as plt

from scrape import *
from sklearn.preprocessing import MinMaxScaler


# TODO: Make this annotation stuff nicer
def update_annot(ind, annot, sc, data, x_axis, y_axis):
    """Updates the plot annotations for the point that the mouse is hovering on.
    The annotations will look like:

    player index player name (x_axis coordinate, y_axis coordinate)"""

    # Get point coordinate and add annotation
    pos = sc.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    # Find the corresponding index in the dataframe
    idx = data.index[(data[x_axis] == pos[0]) & (data[y_axis] == pos[1])]
    # Add the annotation text
    text = "{} ({}, {})".format(data.Name[idx].to_string(), pos[0], pos[1])
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)


def plot_dataframe(data, x_axis, y_axis):
    """Plots the dataframe with specified x-axis and y-axis.
    Possible axes are the numerical columns of the player dataframe."""

    # Make the plot
    x = data[x_axis]
    y = data[y_axis]
    fig, ax = plt.subplots()
    scatter_plot = plt.scatter(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title('tennis-stats plot')

    # Annotate the scatter plot
    annotations = ax.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                              bbox=dict(boxstyle="round", fc="w"),
                              arrowprops=dict(arrowstyle="->"))
    # Start with no annotations
    annotations.set_visible(False)

    # The mouse hover event
    def hover(event):
        vis = annotations.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter_plot.contains(event)
            # Update the annotations only when hovering over a data point
            if cont:
                update_annot(ind, annotations, scatter_plot, data, x_axis, y_axis)
                annotations.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annotations.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()


def max(column):
    return column.max(), column.idxmax()


def minmaxscale(data):
    """Scales the data in the career_record and highest_rankings columns"""
    data.astype({'highest_rankings': 'float64'}).dtypes
    data_numbers = data.drop(["Name", "Birth", "wikilink"], axis=1)
    arr = data_numbers.to_numpy()
    trans = MinMaxScaler()
    arr = trans.fit_transform(arr)
    data_scaled = pandas.DataFrame(arr, columns=['career_record', 'highest_rankings'])
    return data_scaled


def gradient_descent(data):
    """Fit an exponential decay curve to the career_record/highest_rankings plot using gradient descent"""
    data_scaled = minmaxscale(data)

    X = data_scaled['career_record']
    Y = data_scaled['highest_rankings']

    # building the model

    m = -4
    c = 0
    k = 1
    L = 0.01
    epochs = 1000

    n = float(len(X))

    Y_pred = k * np.exp(m * X + c)

    for i in range(epochs):
        Y_pred = k * np.exp(m * X + c)
        D_m = (-2 / n) * sum(X * Y_pred * (Y - Y_pred))  # Derivative wrt m
        D_c = (-2 / n) * sum(Y_pred * (Y - Y_pred))  # Derivative wrt c
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
    plt.ylabel('Scaled highest rankings')
    plt.title('Curve fitting with gradient descent')
    plt.show()
