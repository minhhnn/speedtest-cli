#!/usr/bin/env python
import web
import plot_speedtest

PLOT_NAME = '/tmp/speedtest_logs/bandwidth.png'

urls = (
'/bandwidth', 'showplot',
)

class showplot:
  def GET(self):
    plot_speedtest.create_plot(PLOT_NAME)
    web.header("Content-Type", 'image/png')   # set HTTP header
    return open(PLOT_NAME,"rb").read() # open image for reading
  
  app = web.application(urls, globals())
  if __name__ == "__main__":
    app.run()