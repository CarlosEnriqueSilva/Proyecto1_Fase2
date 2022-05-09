# -*- coding: utf-8 -*-
"""
Created on Sat May  7 09:20:50 2022

@author: Sara Calle, Carlos Silva, Juliana Velasco
"""

import dash
from dash import html
from dash import dcc, callback_context
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from chart_studio import plotly
import plotly as py
import plotly.graph_objs as go
import time
from joblib import dump, load
import pandas as pd

#Crear variables necesarias
studyGuardado = 'Sin datos...'
conditionGuardado = 'Sin datos...'
resultado = 'Sin datos...'

#Cargar el modelo
pipeline = load('modelo.joblib')

#Funciones a utilizar
def correrModelo(s, c):
    r = 'Sin datos'
    if s == None or c == None:
        r = 'Sin datos'
    else:
        global pipeline
        data = [[s, c]]
        df_a = pd.DataFrame(data, columns = ['study', 'condition'])
        res = pipeline.predict(df_a)[0]
        r = 'N.A'
        if res == 1:
            r = 'No Elegible (1)'
        elif res == 0:
            r = 'Elegible (0)'
    return r


#Creación de la aplicación
app = dash.Dash(external_stylesheets = [dbc.themes.SOLAR])

#Logo de analytics para diseño del Navbar
logoNavBar = app.get_asset_url('navBarLogo.png')

#Ventana donde van a ingresar el texto a analizar
modal = html.Div(
    [
        dbc.Button("Analizar Texto", id="open-centered"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Ingresar texto a analizar"), close_button=True),
                dbc.ModalBody(
                    dbc.Form(
                        [
                            dbc.Row(
                                [
                                    dbc.Label("Ingresar Study: "),
                                    dbc.Input(type="text", placeholder = "Texto...", id = 'text-input')
                                ]
                                ),
                            html.Br(),
                            dbc.Row(
                                [
                                    dbc.Label("Ingresar Condition: "),
                                    dbc.Input(type="text", placeholder = "Texto...", id = 'text2-input')
                                ]
                                ),
                            html.Br(),
                            dbc.Button("Submit", id='fav-submit', color="primary"),
                            ]    
                    )
                    ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Close", id="close-centered", className="ms-auto", n_clicks=0,),
                    ]
                ),
            ],
            id="modal-centered",
            centered=True,
            is_open=False,
        ),
    ],
)

#Creación de la barra de navegacion
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = logoNavBar, height = "50px")),
                        dbc.Col(dbc.NavbarBrand("Clinical Trials Analitics", className = "ms-2")),
                        ],
                    align = "center",
                    className = "g-0",
                ),
                style = {"textDecoration": "none"},
            ),
            modal,
            ]
        ),
        color = "dark",
        dark = True,
    
)

#Crear la tarjeta donde se observan las respuestas
filaTarjeta = dbc.Row(
    [
     dbc.Col(id = 'cardStudy', children = [
         dbc.Card(
             dbc.CardBody(
                 [
                    html.H2('Study description', className="card-title"),
                    html.Br(),
                    html.Br(),
                    html.H4(id = "studyOutput", className="card-subtitle", children = [studyGuardado]),
                    html.Br(),
                    html.Br(), 
                     ]
                 )
             )
         ]
    ),
     dbc.Col(id = 'cardCondition', children = [
         dbc.Card(
             dbc.CardBody(
                 [
                    html.H2('Condition description', className="card-title"),
                    html.Br(),
                    html.Br(),
                    html.H4(id = "conditionOutput", className="card-subtitle", children = [conditionGuardado]),
                    html.Br(),
                    html.Br(), 
                     ]
                 )
             )
         ]
    ),
    dbc.Col(id = 'cardResultados', children = [
         dbc.Card(
             dbc.CardBody(
                 [
                    html.H2('Resultados', className="card-title"),
                    html.Br(),
                    html.Br(),
                    html.H4(id = "resultadosOutput", className="card-subtitle", children = [resultado]),
                    html.Br(),
                    html.Br(), 
                     ]
                 )
             )
         ]
    )
     
  ]
)
          

#Creacion de las graficas que muestran la calidad del modelo
pie = dcc.Graph(
        id = "pieGraph",
        figure = {
          "data": [
            {
              "values": [81, 19],
              "labels": [
                "F1-Score",
                "Negative"
              ],
              "name": "F1-Score del Modelo",
              "hoverinfo":"label+percent",
              "hole": .7,
              "type": "pie"
              
}],
          "layout": {
                "title" : dict(text ="F1-Score del Modelo",
                               font =dict(
                               size=20,
                               color = 'white')),
                "paper_bgcolor":"#111111",
                "width": "2000",
                "annotations": [
                    {
                        "font": {
                            "size": 20
                        },
                        "showarrow": False,
                        "text": "",
                        "x": 0.2,
                        "y": 0.2
                    }
                ],
                "showlegend": False              }
        }
)
bar = dcc.Graph(
        id = "3",
        figure ={
                  "data": [
                  {
                          'x':['TP', 'FP', 'TN', 'FN'],
                          'y':[959, 259, 975, 205],
                          'name':'SF Zoo',
                          'type':'bar',
                          'marker' :dict(color=[        '#05C7F2','#D90416','#D9CB04']),
                  }],
                "layout": {
                      "title" : dict(text ="Grafica del Confusion Matrix",
                                     font =dict(
                                     size=20,
                                     color = 'white')),
                      "xaxis" : dict(tickfont=dict(
                          color='white')),
                      "yaxis" : dict(tickfont=dict(
                          color='white')),
                      "paper_bgcolor":"#111111",
                      "plot_bgcolor":"#111111",
                      "width": "2000",
                      "grid": {"rows": 0, "columns": 0},
                      "annotations": [
                          {
                              "font": {
                                  "size": 20
                              },
                              "showarrow": False,
                              "text": "",
                              "x": 0.2,
                              "y": 0.2
                          }
                      ],
                      "showlegend": False                  }
              }
)
                                 
filasGraficas = dbc.Row([dbc.Col(pie, md=6), dbc.Col(bar, md=6)])


           
#Unir los diferentes componenetes en la aplicacion
app.layout = html.Div([navbar, html.Br(), filaTarjeta, html.Br(), filasGraficas])
                       

#Call back y fuuncion para abrir la primera ventana emergente
@app.callback(
    Output("modal-centered", "is_open"),
    [
     Input("open-centered", "n_clicks"),
     Input("close-centered", "n_clicks"),
     Input("fav-submit", "n_clicks"),
    ],
    [
     State("modal-centered", "is_open"),
     State("text-input","value"),
     State("text2-input","value")
    ],
)


def toggle_modal(n1, n2, n3, is_open, study_value, condition_value):
    global studyGuardado
    global conditionGuardado
    clikedButton = [p['prop_id'] for p in callback_context.triggered][0]
    if "fav-submit" in clikedButton:
        studyGuardado = study_value
        conditionGuardado = condition_value
        return not is_open
    
    elif ("open-centered" in clikedButton) or ("close-centered" in clikedButton):
        return not is_open
    return is_open      


#Calback y funcion para actualizar el estudio
@app.callback(
    Output("studyOutput", "children"),
    Input("fav-submit", "n_clicks"),
    State("text-input","value"),
    )

def updateCardStudy(botonActivacion, estudio):
    return estudio


#Callback y funcion para actualizar la condicion
@app.callback(
    Output("conditionOutput", "children"),
    Input("fav-submit", "n_clicks"),
    State("text2-input","value"),
    )

def updateCardCondition(botonActivacion, condicion):
    return condicion

#Callback y funcion para actualizar el resultado
@app.callback(
    Output("resultadosOutput", "children"),
    Input("fav-submit", "n_clicks"),
    State("text-input","value"),
    State("text2-input","value"),
    )

def updateCardResult(botonActivacion, estudio, condicion):
    resp = correrModelo(estudio, condicion)
    return resp
        
#Correr la aplicacion
if __name__ == '__main__':
    app.run_server(debug=True)

    