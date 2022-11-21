import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from collections import deque
import re, subprocess



def check_CPU_temp():
    temp = None
    err, msg = subprocess.getstatusoutput('cat /sys/class/thermal/thermal_zone0/temp')
    if not err:
        m = re.search(r'-?\d\.?\d*', msg)   # a solution with a  regex
        try:
            temp = float(m.group())/1000
        except ValueError: # catch only error needed
            pass
    return temp

clk = 17
dt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

def get_enc_value(counter,clkLastState):
    while True:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                    if dtState != clkState:
                            counter += 1
                    else:
                            counter -= 1
                    return counter
            clkLastState = clkState
            sleep(0.01)



X = deque(maxlen=100)
X.append(1)
Y = deque(maxlen=100)
Y.append(get_enc_value(counter,clkLastState))

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('Encoder value'),
    html.Div('Example from peppe8o.com'),
    dcc.Graph(id='live-graph', animate=True),
    dcc.Interval(id="refresh", interval=1 * 1000, n_intervals=0)
    ]
)

@app.callback(Output("live-graph", "figure"), [Input("refresh", "n_intervals")])
def update(n_intervals):
    X.append(X[-1]+1)
    Y.append(get_enc_value(counter,clkLastState))
    data = go.Scatter(
            x=list(X),
            y=list(Y),
            name='RPI Temp',
            showlegend=True,
            mode= 'lines'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                yaxis=dict(range=[min(Y),max(Y)]),)}

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port='8050')