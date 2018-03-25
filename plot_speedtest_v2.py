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
  #print df
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

  fig, ax1 = plt.subplots()
  plt.title('Bandwidth Report (last 24 hours)')

  downloadLine = ax1.plot(data['timestamp'],data['download'], '-g', label='download')
  uploadLine = ax1.plot(data['timestamp'],data['upload'], '-b', label='upload')
  ax1.set_ylabel('Bandwidth (Mbps)')
  ax1.set_xlabel('Date/Time')
  ax1.set_ylim(0.0,100.0)
  ax1.set_xticks('45')
  ax1.grid()

  ax1.yaxis.set_major_locator(ticker.MultipleLocator(10))
  ax1.yaxis.set_minor_locator(ticker.MultipleLocator(1))
  
  hfmt = dates.DateFormatter('%m/%d %H:%M')
  ax1.xaxis.set_major_formatter(hfmt)
  fig.subplots_adjust(bottom=.25)

  #loc = ax1.xaxis.get_major_locator()
  #loc.set_xticks[dates.HOURLY] = 24
  #loc.set_xticks[dates.MINUTELY] = 60

  print data['timestamp'][0]

  ax2 = ax1.twinx()
  pingLine = ax2.plot(data['timestamp'],data['ping'], '-r', label='ping')
  ax2.set_ylabel('Ping (ms)')
  ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
  ax2.yaxis.set_minor_locator(ticker.MultipleLocator(1))
  ax2.set_ylim(0.0, 100)

  lines = downloadLine + uploadLine + pingLine
  labs = [l.get_label() for l in lines]
  ax1.legend(lines, labs, loc=9, bbox_to_anchor=(0.5, -0.25), ncol=3)

  fig.savefig(file_plot_name)

if __name__ == '__main__':
  main()