import numpy as np
import matplotlib.pyplot as plt

import framemethods
from scrape import *
from sklearn.preprocessing import MinMaxScaler
from player import Nationality


# TODO: Make this annotation stuff nicer
def update_annotations(ind, annotations, scatter_plot, data, x_axis, y_axis):
    """Updates the plot annotations for the point that the mouse is hovering on.
    The annotations will look like:

    player index player name (x_axis coordinate, y_axis coordinate)"""

    # Get point coordinate and add annotation
    pos = scatter_plot.get_offsets()[ind["ind"][0]]
    annotations.xy = pos
    # Find the corresponding index in the dataframe
    idx = data.index[(data[x_axis] == pos[0]) & (data[y_axis] == pos[1])]
    # Add the annotation text
    text = "{} ({}, {})".format(data.Name[idx].to_string(), pos[0], pos[1])
    annotations.set_text(text)
    annotations.get_bbox_patch().set_alpha(0.4)


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
                update_annotations(ind, annotations, scatter_plot, data, x_axis, y_axis)
                annotations.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annotations.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    plt.show()


def tour_result(nat, data):
    result_list = []
    new_data = framemethods.nationality(data, nat)
    print(len(new_data.index))

    for result in Result:
        print(result.name)
        print(result.name[::-1])
        result_data = new_data.drop(
            new_data[(new_data.wimbledon_results != result.name) & (new_data.us_results != result.name[::-1])].index)
        result_list.append(len(result_data.index))
    print(result_list)
    return result_list


def plot_tour_results(data):
    """Using the matplotlib discrete distribution as horizontal bar chart template"""
    tour_results = [r.name for r in Result]

def plot_tour_results_nationality(data):
    """Using the matplotlib discrete distribution as horizontal bar chart template"""

    tour_results = [r.name for r in Result]

    nationality_list = [nat.name for nat in Nationality if nat.name != 'any']

    # print(nationality_list)

    country_results = [tour_result(nat.name, data) for nat in Nationality if nat.name != 'any']

    # print(country_results)

    country_results_dict = dict(zip(nationality_list, country_results))

    # print(country_results_dict)

    # country_results_dict = {
    #     'Germany': tour_result('Germany', data),
    #     'France': tour_result('France', data),
    #     'United States': tour_result('United States', data),
    #     'Spain': tour_result('Spain', data),
    #     'Great Britain': tour_result('Great Britain', data)
    # }

    def survey(results, category_names):
        """
        Parameters
        ----------
        results : dict
            A mapping from question labels to a list of answers per category.
            It is assumed all lists contain the same number of entries and that
            it matches the length of *category_names*.
        category_names : list of str
            The category labels.
        """
        labels = list(results.keys())
        data = np.array(list(results.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = plt.get_cmap('RdYlGn')(
            np.linspace(0.15, 0.85, data.shape[1]))

        fig, ax = plt.subplots(figsize=(9.2, 5))
        ax.invert_yaxis()
        ax.xaxis.set_visible(False)
        ax.set_xlim(0, np.sum(data, axis=1).max())

        for i, (colname, color) in enumerate(zip(category_names, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            rects = ax.barh(labels, widths, left=starts, height=0.5,
                            label=colname, color=color)

            r, g, b, _ = color
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            ax.bar_label(rects, label_type='center', color=text_color)
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                  loc='lower left', fontsize='small')

        return fig, ax

    survey(country_results_dict, tour_results)
    plt.show()


def maximum(column):
    return column.max(), column.idxmax()


def minmaxscale(data):
    """Scales the data in the career_record and highest_rankings columns"""
    data.astype({'highest_rankings': 'float64'}).dtypes
    data_numbers = data.drop(
        ["Name", "Birth", "wikilink", "Nationality", "australian_results", "french_results", "wimbledon_results",
         "us_results"], axis=1)
    arr = data_numbers.to_numpy()
    trans = MinMaxScaler()
    arr = trans.fit_transform(arr)
    data_scaled = pandas.DataFrame(arr, columns=['career_record', 'highest_rankings'])
    return data_scaled


def gradient_descent(data):
    """Fit an exponential decay curve to the career_record/highest_rankings plot using gradient descent"""
    # TODO: scale back
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
