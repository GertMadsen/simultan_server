import dateutil.parser
import pygal

file_name = "./logs/clients.txt"



with open(file_name) as fp:
    x_labels = []
    y_values = []
    for line in fp:
        timestamp,_,serve_time = line.split(",")
        serve_time = int(serve_time)
        x_labels.append(timestamp)
        y_values.append(serve_time)


line_chart = pygal.Line(stroke=False)
line_chart.title = 'Test'
line_chart.x_labels = x_labels
line_chart.add('Request time', y_values)
line_chart.render_in_browser()
