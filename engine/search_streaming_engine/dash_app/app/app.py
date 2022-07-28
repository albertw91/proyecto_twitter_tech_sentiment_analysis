from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd

app = Dash(__name__)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
"""
df = pd.DataFrame({
    "Ambito": ["funcionamiento", "atencion_cliente", "atencion_cliente", "funcionamiento", "funcionamiento", "funcionamiento"],
    "Conteo": [4, 1, 2, 2, 4, 5],
    "Sentimiento": ["Positivo", "Negativo", "Negativo", "Negativo", "Negativo", "Positivo"]
})
"""


app.layout = html.Div(children=[
    html.H1(children='Análisis de sentimiento de dispositivos electrónicos'),

    html.Div(children='''
        
    '''),

    dcc.Graph(
        id='live-update-graph'#,
        #figure=fig
    ),
    dcc.Graph(
        id='recent-tweets-table',
            ), 
        #style={'display': 'inline-block', 'width' : '60%'}
            
    dcc.Interval(
            id='interval-component',
            interval=8*1000, # in milliseconds
            n_intervals=0
    )
])


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    df = pd.read_csv("/dash_app/data/stream_tweet_groupby.csv", sep = ",", encoding= "latin-1", dtype = {'sentiment_code': str})

    df["sentiment_bin"] = df["sentiment_code"].apply(lambda x: str(x[0]))
    sentiment_dict = {"0": "negativo", "1": "positivo"}
    df["sentiment_bin"] = df["sentiment_bin"].apply(lambda x: sentiment_dict[x])

    fig = px.bar(df, x="sentiment_code", y="count", color ="sentiment_bin", barmode="group", 
        title="Conteo de opiniones en Streaming")
    #fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    return fig


@app.callback(Output('recent-tweets-table', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_table_live(n):
    # connect to mongo and store in pandas dataframe
    df = pd.read_csv("/dash_app/data/stream_tweet.csv", sep = ",", encoding= "utf-8", dtype = {'sentiment_code': str})
#id_str,created_at,screen_name,text,user_followers,sentiment,funcionality,client_attention,sentiment_cod

    df["sentiment_bin"] = df["sentiment_code"].apply(lambda x: str(x[0]))
    sentiment_dict = {"0": "negativo", "1": "positivo"}
    df["sentiment_bin"] = df["sentiment_bin"].apply(lambda x: sentiment_dict[x])

    
    values = [[date for date in df.head(5)['created_at']],
                [text for text in df.head(5)['text']],
                [sentiment_bin for sentiment_bin in df.head(5)['sentiment_bin']],
                ]
    
    trace0 = go.Table(
      columnorder = [1,2,3,4],
      columnwidth = [15,60,15,15],
      header = dict(
        values = [['<b>Date</b>'],['<b>Text</b>'],
                      ['<b>Sentiment Score</b>']],
        line = dict(color = 'blue'),
        fill = dict(color = '#1B95E0'),
        align = ['left','center'],
        font = dict(color = 'white', size = 16),
        height = 40
      ),
      cells = dict(
        values = values,
        line = dict(color = 'blue'),
        fill = dict(color = ['white']),
        align = ['left', 'center'],
        font = dict(color = 'black', size = 14),
        height = 30
        ))
      
    data = [trace0]
    layout = dict(title='<b>Tweets más recientes</b>', height=700,
                  titlefont=dict(size=20))
    
    fig = dict(data=data, layout=layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)