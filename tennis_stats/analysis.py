import numpy as np
import matplotlib.pyplot as plt

import framemethods
from scrape import *
from sklearn.preprocessing import MinMaxScaler
from player import Nationality
from tournaments import Result, Tour
from matplotlib.patches import Rectangle


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
    Possible axes are the numerical columns of the player dataframe.
    Hovering over point displays name of player and their dataframe index"""

    # Make the plot
    x = data[x_axis]
    y = data[y_axis]
    fig, ax = plt.subplots()
    scatter_plot = plt.scatter(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title('tennis_stats plot')

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


def tour_result(data, nat, tour):
    """
    :param data: dataframe
    :param nat: Nationality.name
    :param tour: Tour.name
    :return: List of numbers of distinct players of given Nationality to achieve each Result in the Tour
    """
    result_list = []
    new_data = framemethods.nationality(data, nat)

    for result in Result:
        result_data = new_data.drop(
            new_data[(new_data[tour] != result.name) & (new_data[tour] != result.name[::-1])].index)
        result_list.append(len(result_data.index))

    return result_list


def plot_tour_results(data):
    """
    :param data: dataframe

    Using the matplotlib discrete distribution as horizontal bar chart template

    y-axis: Supported tours as in the Tour enum

    x-axis: Number of distinct players to achieve each result in each tour as given by the
            Result enum"""
    possible_tour_results = [r.name for r in Result]

    tours = [t.name for t in Tour]

    tours_result_list = [tour_result(data, 'any', tour_name) for tour_name in tours]

    tours_dict = dict(zip(tours, tours_result_list))

    plot_title = 'Tournament results'
    bar_graph(tours_dict, possible_tour_results, plot_title)
    plt.show()


def plot_tour_results_nationality(data, tour):
    """
    :param data: dataframe
    :param tour: Tour.name

    Using the matplotlib discrete distribution as horizontal bar chart template

    y-axis: Supported nationalities

    x-axis: Number of distinct players to achieve each result as given by the Result enum"""

    possible_tour_results = [r.name for r in Result]

    nationality_list = [nat.name for nat in Nationality if nat.name != 'any']

    country_results = [tour_result(data, nat.name, tour) for nat in Nationality if nat.name != 'any']

    country_results_dict = dict(zip(nationality_list, country_results))

    plot_title = tour + ' results'

    bar_graph(country_results_dict, possible_tour_results, plot_title)
    plt.show()


def bar_graph(results, category_names, plot_title):
    """
    Parameters
    ----------
    results : dict
        A mapping from labels (nationality, tour name, etc) to a list of results per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    plot_title: str
        Title of the resulting plot
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
    ax.set_title(plot_title)

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths

        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)

    # Adding the number of players for each result and hiding the zero values
    for p in ax.get_children()[:-1]:  # skip the last patch as it is the background
        if isinstance(p, Rectangle):
            x, y = p.get_xy()
            w, h = p.get_width(), p.get_height()
            r, g, b, _ = p.get_facecolor()
            text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
            if w > 0:  # anything that has a width of 0 will not be annotated
                ax.text(x + 0.5 * w, y + 0.5 * h, '%i' % w, va='center', ha='center', color=text_color)

    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 0),
              loc='upper left', fontsize='small')

    return fig, ax


def minmaxscale(data):
    """Scales the data in the career_record and highest_rankings columns"""
    data.astype({'highest_rankings': 'float64'}).dtypes
    data_numbers = data.drop(
        ["Name", "Birth", "wikilink", "Nationality", "Australian", "French", "Wimbledon",
         "USopen"], axis=1)
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
