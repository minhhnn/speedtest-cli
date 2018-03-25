#!/usr/bin/env python
import os
import matplotlib.pyplot as plt
from matplotlib import dates, rcParams
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

def main():
  plot_file_name = '/tmp/speedtest_logs/bandwidth.png'
  create_plot(plot_file_name)
  os.system('open ' + plot_file_name)

def create_plot(plot_file_name):
  df = read_data()
  print df
  make_plot_file(df, plot_file_name)

def read_data():
  df = pd.io.parsers.read_csv(
    '/tmp/speedtest_logs/speedtest.log',
    names='date time ping download upload'.split(),
    header=None,
    sep=r'\s+',
    parse_dates={'timestamp':[0,1]},
    na_values=['TEST','FAILED'],
  )

  return df[-48:]   # return data for last 48 periods (i.e., 24 hours)

def make_plot_file(data, file_plot_name):
  rcParams['xtick.labelsize'] = 'xx-small'

  plt.plot(data['timestamp'],data['download'], '-g', label='download')
  plt.plot(data['timestamp'],data['upload'], '-b', label='upload')
  plt.plot(data['timestamp'],data['ping'], '-r', label='ping')
  plt.title('Bandwidth Report (last 24 hours)')
  plt.ylabel('Bandwidth (Mbps)')
  plt.ylim(0.0,100.0)
  plt.xlabel('Date/Time')
  plt.xticks(rotation='45')

  plt.legend()
  plt.grid()
  plt.legend(loc=9, bbox_to_anchor=(0.5, -0.25), ncol=3)

  current_axes = plt.gca()
  current_figure = plt.gcf()

  current_axes.yaxis.set_major_locator(ticker.MultipleLocator(10))
  current_axes.yaxis.set_minor_locator(ticker.MultipleLocator(1))
  hfmt = dates.DateFormatter('%d/%m %H:%M')
  current_axes.xaxis.set_major_formatter(hfmt)
  current_figure.subplots_adjust(bottom=.25)

  loc = current_axes.xaxis.get_major_locator()
  loc.maxticks[dates.HOURLY] = 24
  loc.maxticks[dates.MINUTELY] = 60

  current_figure.savefig(file_plot_name)

if __name__ == '__main__':
  main()