from flask import Flask, render_template, request
import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import plotly
import plotly.express as px
import calendar

plt.style.use('ggplot')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
fp = ''


@app.route("/", methods=["GET", "POST"])
def home():
    data = []
    if request.method == 'POST':
        if request.files:
            uploaded_file = request.files['filename']
            filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            app.config['path'] = fp
            with open(filepath) as file:
                csv_file = csv.reader(file)
                for row in csv_file:
                    data.append(row)
            return render_template('main.html', data="file_uploaded")
    return render_template('main.html', data='')


@app.route("/1")
def button():
    ar=np.array((2))
    return "uploaded"


app.config['FILE_UPLOADS'] = 'C:\\Users\\priya\\PycharmProjects\\Project\\static\\File\\uploads'


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('login.html')


@app.route("/2", methods=["GET", "POST"])
def btn2():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    return render_template('2.html', dataset=[dataset.to_html()], titles=[''])


@app.route("/3", methods=["GET", "POST"])
def btn3():
    if request.method == 'GET':
        num1 = request.values.get("num", type=int)
        if not num1:
            return render_template('3.html', head=[], titles=[''])
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)
        head = dataset.head(num1)
        return render_template('3.html', head=[head.to_html()], titles=[''], start=num1)


@app.route("/4", methods=["GET", "POST"])
def btn4():
    if request.method == 'GET':
        num1 = request.values.get("numb", type=int)
        if not num1:
            return render_template('4.html', tail=[], titles=[''])
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)
        tail = dataset.tail(num1)
        return render_template('4.html', tail=[tail.to_html()], titles=[''], last=num1)


@app.route("/5", methods=["GET", "POST"])
def btn5():
    miss = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)
        miss = dataset.isnull().any()
        # x = miss.split(" ")

    return render_template('5.html', dataset=[miss.values], titles=[''])


@app.route("/5/1", methods=["GET", "POST"])
def btn6():
    value = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)
        value = dataset.isnull().sum()

    return render_template('5.html', value=[value], titles=[''])


@app.route("/7", methods=["GET", "POST"])
def btn7():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    obj = (dataset.dtypes == 'object')
    object_cols = list(obj[obj].index)

    unique_values = {}
    for col in object_cols:
        unique_values[col] = dataset[col].unique().size

    fig = px.bar(dataset, x='CATEGORY', barmode='group', title="Category Data")
    fig1 = px.bar(dataset, x='CATEGORY', color='PURPOSE', barmode='group', title="Category Data with Purpose")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('7.html', graphJSON=graphJSON, graphJSON1=graphJSON1)


@app.route("/8", methods=["GET", "POST"])
def btn8():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    fig = px.bar(dataset, x='PURPOSE', barmode='group', title="Data For Each Purpose")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('8.html', graphJSON=graphJSON)


@app.route("/9", methods=["GET", "POST"])
def btn9():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    fig = px.bar(dataset, y='MILES', color='CATEGORY', barmode='group', title="Data For Each Trip")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('9.html', graphJSON=graphJSON)


# day-night
@app.route("/10", methods=["GET", "POST"])
def btn10():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    dataset['date'] = pd.DatetimeIndex(dataset['START_DATE']).date
    dataset['time'] = pd.DatetimeIndex(dataset['START_DATE']).hour
    # changing into categories of day and night
    dataset['DN'] = pd.cut(x=dataset['time'],
                           bins=[0, 10, 15, 19, 24],
                           labels=['Morning', 'Afternoon', 'Evening', 'Night'])

    fig = px.histogram(dataset['DN'], text_auto='.2s', title="Day-Night Data")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('10.html', graphJSON=graphJSON)


# Month total rides count vs Month ride max count
@app.route("/11", methods=["GET", "POST"])
def btn11():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    dataset['MONTH'] = pd.DatetimeIndex(dataset['START_DATE']).month
    month_label = {1.0: 'Jan', 2.0: 'Feb', 3.0: 'Mar', 4.0: 'April',
                   5.0: 'May', 6.0: 'June', 7.0: 'July', 8.0: 'Aug',
                   9.0: 'Sep', 10.0: 'Oct', 11.0: 'Nov', 12.0: 'Dec'}
    dataset["MONTH"] = dataset.MONTH.map(month_label)
    mon = dataset.MONTH.value_counts(sort=False)
    df = pd.DataFrame({"MONTHS": mon.values,
                       "VALUE COUNT": dataset.groupby('MONTH',
                                                      sort=False)['MILES'].max()})

    fig = px.line(df)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('11.html', graphJSON=graphJSON)


@app.route("/12", methods=["GET", "POST"])
def btn12():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], format="%m-%d-%Y %H:%M")
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], format="%m-%d-%Y %H:%M")

    dayofweek = []
    weekday = []
    for x in dataset['START_DATE']:
        dayofweek.append(x.dayofweek)
        weekday.append(calendar.day_name[dayofweek[-1]])
    dataset['WEEKDAY'] = weekday

    fig = px.histogram(dataset['WEEKDAY'], title="Week-Days Data", barmode='group')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('12.html', graphJSON=graphJSON)


@app.route("/13", methods=["GET", "POST"])
def btn13():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], format="%m-%d-%Y %H:%M")
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], format="%m-%d-%Y %H:%M")

    month = []
    for x in dataset['START_DATE']:
        month.append(x.month)
    dataset['MONTH'] = month
    dataset['MONTH'] = pd.DatetimeIndex(dataset['START_DATE']).month
    month_label = {1.0: 'Jan', 2.0: 'Feb', 3.0: 'Mar', 4.0: 'April',
                   5.0: 'May', 6.0: 'June', 7.0: 'July', 8.0: 'Aug',
                   9.0: 'Sep', 10.0: 'Oct', 11.0: 'Nov', 12.0: 'Dec'}
    dataset["MONTH"] = dataset.MONTH.map(month_label)
    mon = dataset.MONTH.value_counts(sort=False)
    fig = px.histogram(dataset['MONTH'], title="Rides Per Month")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('13.html', graphJSON=graphJSON)


@app.route("/14", methods=["GET", "POST"])
def btn14():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], format="%m-%d-%Y %H:%M")
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], format="%m-%d-%Y %H:%M")
    date = []

    for x in dataset['START_DATE']:
        date.append(x.day)
    dataset['DATE'] = date
    dataset['DATE'] = pd.DatetimeIndex(dataset['START_DATE']).day
    date_label = {1.0: '1', 2.0: '2', 3.0: '3', 4.0: '4',
                  5.0: '5', 6.0: '6', 7.0: '7', 8.0: '8',
                  9.0: '9', 10.0: '10', 11.0: '11', 12.0: '12',
                  13.0: '13', 14.0: '14', 15.0: '15', 16.0: '16',
                  17.0: '17', 18.0: '18', 19.0: '19', 20.0: '20',
                  21.0: '21', 22.0: '22', 23.0: '23', 24.0: '24',
                  25.0: '25', 26.0: '26', 27.0: '27', 28.0: '28',
                  29.0: '29', 30.0: '30', 31.0: '31'}

    dataset["DATE"] = dataset.DATE.map(date_label)
    mon = dataset.DATE.value_counts(sort=False)
    df = pd.DataFrame({"DATE": mon.values})
    fig = px.histogram(dataset['DATE'], title="Rides Per Day Of A Month", )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('14.html', graphJSON=graphJSON)


@app.route("/15", methods=["GET", "POST"])
def btn15():
    dataset = ''
    if request.method == 'GET':
        data = os.listdir(app.config['FILE_UPLOADS'])[0]
        dataset = pd.read_csv(app.config['FILE_UPLOADS'] + "\\" + data)

    dataset['START_DATE'] = pd.to_datetime(dataset['START_DATE'], format="%m-%d-%Y %H:%M")
    dataset['END_DATE'] = pd.to_datetime(dataset['END_DATE'], format="%m-%d-%Y %H:%M")
    hour = []

    for x in dataset['START_DATE']:
        hour.append(x.hour)
    dataset['HOUR'] = hour
    dataset['HOUR'] = pd.DatetimeIndex(dataset['START_DATE']).hour
    hour_label = {1.0: '1', 2.0: '2', 3.0: '3', 4.0: '4',
                  5.0: '5', 6.0: '6', 7.0: '7', 8.0: '8',
                  9.0: '9', 10.0: '10', 11.0: '11', 12.0: '12', 13.0: '13', 14.0: '14', 15.0: '15', 16.0: '16',
                  17.0: '17', 18.0: '18', 19.0: '19', 20.0: '20', 21.0: '21',
                  22.0: '22', 23.0: '23', 24.0: '24', 25.0: '25'}
    dataset["HOUR"] = dataset.HOUR.map(hour_label)
    hr = dataset.HOUR.value_counts(sort=False)
    df = pd.DataFrame({"HOUR": hr.values})

    fig = px.histogram(dataset['HOUR'], title="Rides Per Hour Of A Day")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('15.html', graphJSON=graphJSON)


app.run(debug=True)
