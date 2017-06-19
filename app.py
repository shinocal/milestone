from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
from quandl.errors.quandl_error import NotFoundError 

import datetime
import simplejson as json
import pandas as pd
import requests
from bokeh.plotting import figure
from bokeh.embed import components

app = Flask(__name__)

def index():
  i=datetime.datetime.now()

  startdate='%s%s%s' % (i.year,i.month-1,i.day)
  enddate='%s%s%s' % (i.year,i.month,i.day)
  user_input=request.form['tkr']

  if len(str(i.month))==1:
    startdate='%s%s%s%s' % (i.year,0,i.month-1,i.day)
    enddate='%s%s%s%s' % (i.year,0,i.month,i.day)

  api_url='https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date.gte=%s&date.lt=%s&ticker=%s&api_key=MUSMX7hgtssoAwLpwFnb' % (startdate,enddate,user_input) 

  r=requests.get(api_url)
  data=r.json()
  df=pd.DataFrame(data['datatable']['data'])

  closing_price=df[5]

  var=[];

  for n in range(len(closing_price)-1):
    var.append(closing_price[n])
  
  from bokeh.plotting import figure, output_file, save

  x=range(1,len(closing_price))
  p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')
  p.line(x, var, legend="Temp.", line_width=2)

