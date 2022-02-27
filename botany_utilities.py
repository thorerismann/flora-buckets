from PIL import Image as PILImage
from matplotlib import colors
import numpy as np

def mutually_exclusive_plant_charac(data, new_col="allstats", old_col="inv", exclude="X"):
  """Removes all rows from a data frame that where the value of old_col is equal to exclude.

  :param data: A data frame
  :type data:pd.DataFrame
  :param new_col:The name of the column once the data
      has been excluded.
  :type new_col: str
  :param old_col: The name of the column that contains the
      value to exclude.
  :type old_col: str
  :param exclude: The value to remove.
  :type exclude: str, int, tuple
  :return: The data frame without the excluded value.
  """
  a = data[data[old_col] != exclude].copy()
  a[new_col] = a[old_col]

  return a

def display_image_ipython(file_location, thumb=(1200, 700), rotates=0):
  """Convenience method to use PIL and Ipython to display images.

  :param file_location: The location of the file relative location of the file
  :type file_location: string
  :param thumb: The size of the image
  :type thumb: tuple, integers
  :return: displays the image or a message that the image could not be displayed
  :rtype: displayed image, or string
  """

  try:
    if rotates == 0:
      r = PILImage.open(file_location).convert("RGBA")
      r = r.resize(thumb)
    else:

      r = PILImage.open(file_location).convert("RGBA")
      r = r.resize(thumb)
      r = r.rotate(angle=rotates, expand=False)

    return r

  except:
    print(f"could not load image {file_location} ")

def make_a_summary_table(ax, data, colLabels, a_color="black", font_size=12, s_et_bottom_row=True):
  """Formats matplotlib table object.

  Args:
  ax: object: matplotlib table object
  data: array: the 2d array used to generate the table object
  cols_to_use: array: the list of column names
  a_color: str: matplotlib named color, face and edgecolor of table cells
  font_size: int: the font size for the table cells
  s_et_bottom_row: bool: whether or not to draw bottom line on the last row

  Returns:
  The table object formatted.
  """

  # this needs to be shut down at each instance
  ax.auto_set_font_size(False)

  # collect the individual table celss
  the_cells = ax.get_celld()

  # use the line color from the settings
  line_color = colors.to_rgba(a_color)

  # add an alpha to the RGB
  banded_color = (*line_color[:-1], 0.1)

  # the different areas of formatting
  top_row = [(0, i) for i in np.arange(len(colLabels))]
  bottom_row = [(len(data), i) for i in np.arange(len(colLabels))]
  data_rows = [x for x in list(the_cells.keys()) if x not in top_row]

  for a_cell in top_row:
    ax[a_cell].visible_edges = "B"
    ax[a_cell].set_text_props(**{"fontsize": font_size})
    ax[a_cell].set_edgecolor("black")
    ax[a_cell].PAD = .2
    ax[a_cell].set_linewidth = 1
    ax[a_cell].set_height(.5 / (len(data)))

  for a_cell in data_rows:
    ax[a_cell].set_height(.5 / (len(data)))
    ax[a_cell].visible_edges = "BT"
    ax[a_cell].set_text_props(**{"fontsize": font_size})
    ax[a_cell].set_edgecolor(banded_color)
    ax[a_cell]._text.set_horizontalalignment("center")
    ax[a_cell].set_linewidth = .1

  if s_et_bottom_row is True:

    for a_cell in bottom_row:
      ax[a_cell].visible_edges = "B"
      ax[a_cell].set_edgecolor(line_color)
      ax[a_cell].set_linewidth = 1

  return ax

def a_simple_formatted_table(ax, data, colLabels=[], a_color="black", colWidths=[], bbox=[], **kwargs):
  """Makes a table with rows from a matplotlib axes object and a 2d array. Header row is
  spererated from table body by a thicker black line.

  :param ax: An axes
  :type ax: matplotlib axes
  :param data: An array of the table values not including column names or labels
  :type data: array
  :param colLabels: The labels for the data table columns
  :type colLabels: array
  :param a_color: The color of the cell borders
  :type a_color: str
  :param colWidths: The width of each column in fractions of 1
  :type colWdiths: array, x < 1
  :param bbox: The location of the table in figure space
  :type bbox: array
  :return: A table on the provided axis
  :rtype: matplotlib.axes

  """
  a = ax.table(data, colLabels=colLabels, colWidths=colWidths, bbox=bbox, loc="lower center", **kwargs)
  t = make_a_summary_table(a, data, colLabels, a_color=a_color, font_size=12, s_et_bottom_row=False)
  return t


def a_stacked_bar_chart(ax, bars, xaxis=[], totals={}, palette={}, **kwargs):
  """Makes a stacked barchart given a matplotlib < ax > object
  and a dictionary of values for each "row" of the stack.

  :param ax: A matplotlib axes object
  :type ax: matplotlib.axes
  :param bars: Dictionary of values for each row
  :type bars: dict
  :param xaxis: The values that define the xaxis, can be
       date or categorical
  :type xaxis: array
  :param totals: A dictionary for a second non stacked bar chart.
  :type totals: dict
  :Return: A matplotlib axes object with a stacked barchart.
  """
  # set the bottom of the stacked bar chart
  bottom = 0

  if totals:
    # this is a seperate independent stack
    # its value does not effect the value of <bottom>
    ax.bar(xaxis, totals["data"], bottom=bottom, label=totals["label"], zorder=0)
  else:
    pass

  for a_bar in bars:
    if palette:
      ax.bar(xaxis, bars[a_bar]["data"], bottom=bottom, label=a_bar, color=palette[a_bar], zorder=2)
    else:
      ax.bar(xaxis, bars[a_bar]["data"], bottom=bottom, label=a_bar, zorder=2)

    # add the value of data to bottom
    bottom += bars[a_bar]["data"]

  return ax


def a_single_column_table(ax, data, fs=12, colWidths=[.7, .3], bbox=[0, 0, 1, 1], kwargs={}):
  """Makes a table with rows from a matplotlib axes object and a 2d array. Header row is
  spererated from table body by a thicker black line.

  :param ax: An axes
  :type ax: matplotlib axes
  :param data: An array of the table values not including column names or labels
  :type data: array
  :param fs: The font size for the cell data
  :type fs: float, int
  :param colWidths: The width of each column in fractions of 1
  :type colWdiths: array, x < 1
  :param bbox: The location of the table in figure space
  :type bbox: array
  :return: A table on the provided axis
  :rtype: matplotlib.axes
  """

  a = ax.table(data, colWidths=colWidths, bbox=bbox, loc="lower center", **kwargs)
  a.auto_set_font_size(False)
  a.set_fontsize(fs)

  return a
