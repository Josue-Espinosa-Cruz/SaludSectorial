import pandas as pd
import numpy as np
from math import ceil
import json as js

import plotly.graph_objects as go
import plotly.express as xp

from dash import Dash, html, dcc, Input, Output, dash_table


### DATAFRAMES
sseOp = pd.read_csv("sseOp.csv", index_col=[0,1,2,3], header=[0,1])
PobMun = pd.read_csv("PobMun.csv", index_col=[0,1])
PobEst = pd.read_csv("D:/Proyectos/1_Ciencia de Datos/1_CLUES/PobEst.csv", index_col=[0])


### GEOJSON
# Estados
EstadosLink = "D:/Proyectos/1_Ciencia de Datos/1_CLUES/Datos/GeoStatistic/GeoJson_Limites/EstadosKM2.json"
jsEstados = js.load(open(EstadosLink, "r"))

for Estados in jsEstados["features"]:
    Estados["id"] = Estados["properties"]["gid"]

# Municipios
MunLink = "D:/Proyectos/1_Ciencia de Datos/1_CLUES/MunGeo.json"
munGeneral = js.load(open(MunLink, "r"))


### VARIABLES GLOBALES
# Establecimientos en Operación
Op_Estab = sseOp.index.get_level_values(2).unique().tolist()
Op_Estab.insert(0,"TODAS")

#All_Estab = sseOp.index.get_level_values(2).unique().tolist()

#Instituciones en Operacion
Op_Inst = sseOp.index.get_level_values(3).unique().tolist()
Op_Inst.insert(0,"TODAS")

#All_Inst = sseOp.index.get_level_values(3).unique().tolist()

CatLink = "D:/Proyectos/1_Ciencia de Datos/1_CLUES/Categorias.json"
Categorias = js.load(open(CatLink, "r"))

#NombreEst = sseOpEs.index.values #sseOp.index.get_level_values(0).unique().values  #sseOpEs.index.values
none = slice(None)

app = Dash(__name__,external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    
    dcc.Store(id='store-data', data=[], storage_type='memory'), # 'local' or 'session'
    dcc.Store(id='store_Mun', data=[], storage_type='memory'), # 'local' or 'session'
    
    html.Div([
        html.Div([
            
            html.Div([
                html.Div(["Filtrar Tipo de Establecimiento"],style={'font-weight': 'bold'}),
            
                dcc.Dropdown(
                    id = 'establecimiento',
                    options = [{"label":i.title(),"value":i} for i in Op_Estab],
                    value = "TODAS",
                    clearable = False
                )
            ]),
            
            html.Div([
                html.Div(["Filtrar Institución"],style={'font-weight': 'bold'}),
            
                dcc.Dropdown(
                    id = 'institucion',
                    options = [{"label":i,"value":i} for i in Op_Inst],
                    value = "TODAS",
                    clearable = False
                )
            ])
            
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            
            html.Div(["Característica Principal"],style={'font-weight': 'bold'}),
            
            dcc.Dropdown(
                id = 'cat_selector',
                options = [{"label":i,"value":i} for i in Categorias["label"].keys()],
                value = "Consultorios",
                clearable = True
            ),
            
            html.Div(["Característica Secundaria"],style={'font-weight': 'bold'}),
            
            dcc.Dropdown(
                id = 'subcat_selector',
                options = [{"label":i,"value":j} for i,j in zip(Categorias["label"]["Consultorios"], Categorias["values"]["Consultorios"])],
                value = 'Total De Consultorios',
                clearable = True
            )
            
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'display': 'block'}),
    
    
    html.Div([
        
        html.Div([
            
            html.Div([
                
                html.Div([
                    dcc.RadioItems(
                        id = "prop_graphMex",
                        options = [{"label":i[0], "value":i[1]} for i in [["Absoluto",0],["Cada 100K habitantes",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center'}),
                    
                
                html.Div([
                    dcc.RadioItems(
                        id = "color_graphMex",
                        options = [{"label":i[0], "value":i[1]} for i in [["Secuencial",0],["Divergente en Mediana",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center'}),
                
                
                dcc.Graph(
                    id='graphMex',
                    clickData={'points': [{'location': 9,'hovertext': 'CIUDAD DE MEXICO'}]}
                )
            ]),
            
            html.Div([
                
                html.Div([
                    dash_table.DataTable(
                        id = "tblEst",
                        #page_action='none',
                        page_size = 16,
                        fixed_rows={'headers': True},
                        style_table={'height': 425},
                        #style_cell={
                        #    'width': '{}%'.format(len(sseOpEs[["Unidades"]].reset_index().columns)),
                        #    'textOverflow': 'ellipsis',
                        #    'overflow': 'hidden',
                        #    'border': '1px solid grey' 
                        #},
                        style_header={'border': '1px solid black' },
                    )
                ], style={"display":"inline-block",
                          'width': '49%'}),

                html.Div([
                    dcc.Graph(
                        id = "graph_VioMex",
                        config={
                            'scrollZoom': False,
                            'modeBarButtonsToRemove': ["zoom", "pan", "select", 
                                                       "lasso2d", "zoomIn", "zoomOut", 
                                                       "autoScale"],
                            'displaylogo': False
                        }
                    )
                ], style={"display":"inline-block",
                          'width': '49%'})

            ], style={"text-align":"right"})
            
        ], style={"display":"inline-block",'width': '49%'}),
        
        html.Div([
            
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        id = "prop_graphEst",
                        options = [{"label":i[0], "value":i[1]} for i in [["Absoluto",0],["Cada 100k habitantes",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center'}),
                    
                
                html.Div([
                    dcc.RadioItems(
                        id = "color_graphEst",
                        options = [{"label":i[0], "value":i[1]} for i in [["Secuencial",0],["Divergente en Mediana",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    )
                ], style={'textAlign': 'center'}),
                
                dcc.Graph(
                    id='graphEst'
                )
            ]),
            
            html.Div([
                
                html.Div([
                    dash_table.DataTable(
                        id = "tblMun",
                        #page_action='none',
                        page_size = 16,
                        fixed_rows={'headers': True},
                        style_table={'height': 425},
                        #style_cell={
                        #    'width': '{}%'.format(len(sseOpEs[["Unidades"]].reset_index().columns)),
                        #    'textOverflow': 'ellipsis',
                        #    'overflow': 'hidden',
                        #    'border': '1px solid grey' 
                        #},
                        style_header={'border': '1px solid black' },
                    )
                ], style={"display":"inline-block",
                          'width': '49%'}),

                html.Div([
                    dcc.Graph(
                        id = "graph_VioMun",
                        config={
                            'scrollZoom': False,
                            'modeBarButtonsToRemove': ["zoom", "pan", "select", 
                                                       "lasso2d", "zoomIn", "zoomOut", 
                                                       "autoScale"],
                            'displaylogo': False
                        }
                    )
                ], style={"display":"inline-block",
                          'width': '49%'})

            ])
            
            
        ], style={
            "display":"inline-block",
            'width': '49%'
        })
    ]),
    
    html.Div([
        
        html.Div([
            
            html.Div([
                
                html.Div(["Manipulación de los Datos"], 
                         style={'textAlign': 'center', 'font-weight': 'bold'}),
        
                html.Div([
                    dcc.RadioItems(
                        id = "group_ANOVA",
                        options = [{"label":i[0],"value":i[1]} for i in [["Por Municipios",0],["Por Unidades",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    ),
                ], style={'textAlign': 'center'}),

                html.Div([
                    dcc.RadioItems(
                        id = "prop_ANOVA",
                        options = [{"label":i[0],"value":i[1]} for i in [["Absoluto",0],["Cada 100K habitantes",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    ),
                ], style={'textAlign': 'center'}),

                html.Div([
                    dcc.RadioItems(
                        id = "Outlier_ANOVA",
                        options = [{"label":i[0],"value":i[1]} for i in [["Con Outliers",0],["Sin Outliers",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    ),
                ], style={'textAlign': 'center'}),
                
            ], style={"display":"inline-block",'width': '49%',"text-align": "center"}),
            
            html.Div([
                
                html.Div(["Manipulación de la Gráfica"], 
                         style={'textAlign': 'center', 'font-weight': 'bold'}),
        
                html.Div([
                    dcc.RadioItems(
                        id = "norm_ANOVA",
                        options = [{"label":i[0],"value":i[1]} for i in [["Por Diferencia de Medias",0],["Por Normalidad",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    ),
                ], style={'textAlign': 'center'}),

                html.Div([
                    dcc.RadioItems(
                        id = "std_ANOVA",
                        options = [{"label":i[0],"value":i[1]} for i in [["Sin Desviación Estándar",0],["Con Desviación Estandar",1]]],
                        value = 0,
                        labelStyle = {'display': 'inline-block'}
                    ),
                ], style={'textAlign': 'center'}),
                
            ], style={"display":"inline-block",'width': '49%',"text-align": "center"})
        ]),
        
        
        
        html.Div([
            dcc.Graph(
                id = "graph_ANOVA",
                config={'scrollZoom': False,
                        'modeBarButtonsToRemove': ["zoom", "pan", "select", 
                                                   "lasso2d", "zoomIn", "zoomOut", 
                                                   "autoScale"],
                        'displaylogo': False
                       }
            )
        ], style={'textAlign': 'center'})
        
    ])
    
])


# ACTUALIZACIÓN DE INSTITUCIONES DISPONIBLES
@app.callback(
    Output('institucion', 'options'),
    Input('establecimiento', 'value')
)
def update_filter(establecimiento_value):
    print(establecimiento_value)
    if establecimiento_value == "TODAS":
        options = sseOp.index.get_level_values(3).unique().insert(0,"TODAS")
    else:
        value = sseOp.loc[(none, none, establecimiento_value, none)].index.get_level_values(2).unique()
        
        if len(value) > 1:
            options = value.insert(0,"TODAS")
        else:
            options = value
    print(options)
    return [{"label":i,"value":i} for i in options] 

@app.callback(
    Output('institucion', 'value'),
    [Input('institucion', 'options'),
     Input("institucion","value")]
)
def update_filter(institucion_options, institucion_value):
    
    for Option in institucion_options:
        if institucion_value == Option["value"]:
            return institucion_value
    
    return institucion_options[0]["value"]
    
# ACTUALIZACIÓN DE TIPO DE ESTABLECIMIENTOS DISPONIBLES
@app.callback(
    Output('establecimiento', 'options'),
    Input('institucion', 'value')
)
def update_filter(institucion_value):
    
    if institucion_value == "TODAS":
        options = sseOp.index.get_level_values(2).unique().insert(0,"TODAS")
    else:
        value = sseOp.loc[(none, none, none, institucion_value)].index.get_level_values(2).unique()
        
        if len(value) > 1:
            options = value.insert(0,"TODAS")
        else:
            options = value
        
    return [{"label":i.title(),"value":i} for i in options]


# ACTUALIZACIÓN DE CATEGORÍAS Y SUBCATEGORIAS (VALUES-LABEL)
@app.callback(
    Output('subcat_selector', 'options'),
    Input('cat_selector', 'value')
)
def update_filter(cat_selector_value):
    
    subcat = [{"label":i,"value":j} for i,j in zip(Categorias["label"][cat_selector_value], Categorias["values"][cat_selector_value])]
    
    return subcat

@app.callback(
    Output('subcat_selector', 'value'),
    Input('subcat_selector', 'options')
)
def update_filter(subcat_selector_options):
    
    return subcat_selector_options[0]["value"]


# GUARDAR INFORMACION MÉXICO
@app.callback(
    Output('store-data', 'data'),
    [Input('establecimiento', 'value'),
     Input('institucion', 'value'),
     Input('cat_selector', 'value'),
     Input('subcat_selector', 'value')]
)
def update_output(establecimiento_value, institucion_value, cat_value, subcat_value):
    ### CREAR TABLA CON TODOS LOS ESTADOS
    
    filtro = (none,none,none,none)
    cat = [("Otros","Clave Estado")]
    
    df2 = sseOp.loc[filtro,cat].groupby(["Nombre Estado",("Otros","Clave Estado")]).sum()
    
    df2 = df2.reset_index(1)
    df2.columns = df2.columns.droplevel(0)
    
    ### INFORMACIÓN PRINCIPAL
    if establecimiento_value == "TODAS":
        establecimiento_value = none
        
    if institucion_value == "TODAS":
        institucion_value = none
    
    filtro = (none,none,establecimiento_value,institucion_value)
    cat = [(cat_value, subcat_value)]
    
    df = sseOp.loc[filtro,cat].groupby(["Nombre Estado"]).sum()
    
    df.columns = df.columns.droplevel(0)
    
    
    ### CREAR TABLA CON CEROS
    dfFinal = df2.join(df, how="left")
    dfFinal = dfFinal.fillna(0).sort_values("Clave Estado", ascending=True)
    
    
    ### AÑADIR INFORMACION POBLACIONAL
    dfFinal = dfFinal.join(PobEst, how="inner")
    dfFinal["Mil_Hab"] = round((dfFinal[subcat_value]*100000)/dfFinal["POBTOT"], 2)
    dfFinal = dfFinal.drop(["POBTOT"], axis=1).reset_index()
    
    return dfFinal.to_json(orient='split')


# ACTUALIZACIÓN DEL GRÁFICO MÉXICO
@app.callback(
    Output('graphMex', 'figure'),
    [Input('store-data', 'data'), 
     Input('subcat_selector', 'value'), 
     Input("prop_graphMex","value"), 
     Input("color_graphMex","value")]
)
def update_output(store_data,subcat_value,prop_value,color_value):
    
    df = pd.read_json(store_data, orient='split')
    
    if prop_value == 0:
        seleColor = subcat_value
    else:
        seleColor = "Mil_Hab"
        
    if color_value == 0:
        Range = (0, df[seleColor].max()) if (df[seleColor].max() != 0) else (0,100)
        Midpoint = None
        Scale = "blues"
    else:
        Range = None
        Midpoint = df[seleColor].median()
        Scale = xp.colors.diverging.Picnic
    
    fig_map = xp.choropleth(data_frame = df,
                            locations = "Clave Estado", 
                            hover_name  = "Nombre Estado",
                            hover_data = {"Clave Estado":False},
                            range_color = Range,
                            geojson = jsEstados,
                            color = seleColor, 
                            color_continuous_scale = Scale,#xp.colors.diverging.Picnic, #"blues", 
                            color_continuous_midpoint = Midpoint,
                            scope = 'north america')

    fig_map.update_geos(fitbounds = "locations", visible = False, resolution = 50);
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                          dragmode = False,
                          coloraxis_colorbar_x=-0.15);
    
    return fig_map


# ACTUALIZACIÓN DE LA TABLA MËXICO
@app.callback(
    Output('tblEst', 'data'),
    [Input('store-data', 'data'),
     Input("prop_graphMex","value")]
)
def update_output(store_data, prop_value):
    
    df = pd.read_json(store_data, orient='split')
    df = df.rename(columns={df.columns[2]:"Total"})
    
    if prop_value == 0:
        df = df.drop(["Clave Estado", "Mil_Hab"], axis=1)
        df = df.sort_values("Total", ascending=False)
        
    else:
        df["Mil_Hab"] = round(df["Mil_Hab"], 2)
        df = df.drop(["Clave Estado", "Total"], axis=1)
        df = df.sort_values("Mil_Hab", ascending=False)
    
    return df.to_dict("records")

@app.callback(
    Output('tblEst', 'columns'),
    [Input('tblEst', 'data'), 
     Input("prop_graphMex","value")]
)
def update_output(store_data, prop_value):
    
    df = pd.DataFrame.from_records(store_data)
    
    if prop_value == 0:
        Columns = sorted(df.columns, reverse=False)
    else:
        Columns = sorted(df.columns, reverse=True)
    
    return [{"name": i, "id": i} for i in Columns]


# ACTUALIZACIÓN DEL GRÁFICO VIOLIN MÉXICO
@app.callback(
    Output('graph_VioMex', 'figure'),
    [Input('store-data', 'data'), 
     Input("prop_graphMex","value")]
)
def update_output(store_data, prop_value):
    
    df = pd.read_json(store_data, orient='split')
    
    if prop_value == 0:
        yValue = df.iloc[:,2]
    else:
        yValue = df.iloc[:,3]
    
    figVio = xp.violin(data_frame = df, y = yValue, box = True, points = "all",
                       custom_data=["Nombre Estado"],
                       color_discrete_sequence = ['#370031'],
                       orientation = "v")
    
    figVio.update_traces(hovertemplate=
                         'Value: %{y}' + 
                         "<br> Estado: %{customdata[0]} </br>")
    
    return figVio


# ALMACENAR INFORMACIÓN DEL ESTADO SELECCIONADO
@app.callback(
    Output('store_Mun', 'data'),
    [Input('establecimiento', 'value'),
     Input('institucion', 'value'),
     Input('cat_selector', 'value'),
     Input('subcat_selector', 'value'),
     Input('graphMex', 'clickData')]
)
def display_click_data(establecimiento_value, institucion_value, cat_value, subcat_value, clickData):
    
    ### CREAR TABLA CON TODOS LOS MUNICIPIOS
    
    filtro = (none,none,none,none)
    cat = [("Otros","Clave Municipio")]
    
    df2 = sseOp[sseOp[("Otros","Clave Estado")] == clickData["points"][0]['location']]
    df2 = df2.loc[filtro,cat].groupby(["Nombre Municipio",("Otros","Clave Municipio")]).sum()
    
    df2 = df2.reset_index(1)
    df2.columns = df2.columns.droplevel(0)
    
    ### CREAR TABLA CON LOS MUNICIPIOS QUE CUMPLEN LAS OPCIONES DE FILTRADO
    if establecimiento_value == "TODAS":
        establecimiento_value = none
        
    if institucion_value == "TODAS":
        institucion_value = none
    
    
    filtro2 = (clickData["points"][0]['hovertext'],none,establecimiento_value,institucion_value)
    cat2 = [(cat_value, subcat_value)]
    
    
    #df = sseOp[sseOp[("Otros","Clave Estado")] == clickData["points"][0]['location']]
    
    try:
        
        df = sseOp.loc[filtro2,cat2].groupby(["Nombre Municipio"]).sum()
        df.columns = df.columns.droplevel(0)

        ### UNIR AMBAS TABLAS Y LIMPIAR DATOS
        df2 = df2.join(df, how="left")
        df2 = df2.fillna(0).sort_values("Clave Municipio", ascending=True)
        
    except KeyError:
        df2.insert(df2.shape[1], subcat_value, [0,]*len(df2.index))
        
    
    ### JUNTAR AMBAS TABLAS
    dfFinal = df2.join(PobMun.loc[clickData["points"][0]['hovertext']], how="inner")
    dfFinal["Mil_Hab"] = round((dfFinal[subcat_value]*100000)/dfFinal["POBTOT"], 2)
    dfFinal = dfFinal.drop(["POBTOT"], axis=1).reset_index()
    
    return dfFinal.to_json(orient='split')


# ACTUALIZACIÓN DEL MAPA SOBRE MUNICIPIOS
@app.callback(
    Output("graphEst","figure"),
    [Input("store_Mun","data"), 
     Input('subcat_selector', 'value'),
     Input('graphMex', 'clickData'),
     Input("prop_graphEst","value"), 
     Input("color_graphEst","value")]
)
def update_output(store_data, subcat_value, clickData, prop_value, color_value):
    df = pd.read_json(store_data, orient='split')
    
    if prop_value == 0:
        seleColor = subcat_value
    else:
        seleColor = "Mil_Hab"
        
    if color_value == 0:
        
        if df[seleColor].max() == 0:
            Range = (0,100)
        else:
            Range = (0, df[seleColor].max())
            
        Midpoint = None
        Scale = "blues"
    else:
        Range = None
        Midpoint = df[seleColor].median()
        Scale = xp.colors.diverging.Picnic
    
    if clickData["points"][0]['hovertext'] == "COLIMA":
        Center = {"lat":19.16 ,"lon":-104.07} #{"lat":19.167107 ,"lon":-103.860833}
        Fitbounds = False
    else:
        Center = {}
        Fitbounds = "locations"
        
    
    fig_map = xp.choropleth(data_frame = df,
                            locations = "Clave Municipio", 
                            center=Center,
                            hover_name  = "Nombre Municipio",
                            hover_data = {"Clave Municipio":False},
                            range_color = Range,
                            geojson = munGeneral[int(clickData["points"][0]['location'])-1],
                            color = seleColor, 
                            color_continuous_scale = Scale, 
                            color_continuous_midpoint = Midpoint,
                            fitbounds = Fitbounds,
                            scope = 'north america')

    fig_map.update_geos(visible = False, resolution = 50, lataxis=dict(range=[18.67,19.56]), lonaxis=dict(range=[-104.96,-103.34])) #fitbounds = "locations", 
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                          dragmode = False,
                          coloraxis_colorbar_x=-0.15);
    
    return fig_map

# ACTUALIZACIÓN DE LA TABLA MUNICIPIOS
@app.callback(
    Output('tblMun', 'data'),
    [Input('store_Mun', 'data'),
     Input("prop_graphEst","value")]
)
def update_output(store_data,prop_value):
    
    df = pd.read_json(store_data, orient='split')
    
    df = df.rename(columns={df.columns[2]:"Total"})
    
    if prop_value == 0:
        df = df.drop(["Clave Municipio", "Mil_Hab"], axis=1)
        df = df.sort_values("Total", ascending=False)
        
    else:
        df["Mil_Hab"] = round(df["Mil_Hab"], 2)
        df = df.drop(["Clave Municipio", "Total"], axis=1)
        df = df.sort_values("Mil_Hab", ascending=False)
    
    return df.to_dict('records')

@app.callback(
    [Output('tblMun', 'columns'),
     Output("tblMun","page_size")],
    [Input('tblMun', 'data'), 
     Input("prop_graphEst","value")]
)
def update_output(store_data, prop_value):
    
    df = pd.DataFrame.from_records(store_data)
    
    if prop_value == 0:
        Columns = sorted(df.columns, reverse=False)
    else:
        Columns = sorted(df.columns, reverse=True)
    
    return [{"name": i, "id": i} for i in Columns], ceil(df.shape[0]/2)


# ACTUALIZACIÓN DEL GRÁFICO VIOLIN MUNICIPIOS
@app.callback(
    Output('graph_VioMun', 'figure'),
    [Input('store_Mun', 'data'),
     Input("prop_graphEst","value")]
)
def update_output(store_data, prop_value):
    
    df = pd.read_json(store_data, orient='split')
    
    if prop_value == 0:
        yValue = df.iloc[:,2]
    else:
        yValue = df.iloc[:,3]
    
    figVio = xp.violin(data_frame = df, y = yValue, box = True, points = "all",
                       color_discrete_sequence = ['#370031'],
                       custom_data=['Nombre Municipio'],
                       orientation = "v")
    
    figVio.update_traces(hovertemplate=
                         'Value: %{y}' + 
                         "<br> Municipio: %{customdata[0]} </br>")
    
    return figVio


# ACTUALIZAR COMPARACIÓN ANOVA
@app.callback(
    Output('group_ANOVA', 'options'),
    Input('prop_ANOVA', 'value')
)
def update_output(prop_value):
    
    if prop_value == 1:
        options = [{"label":i[0],"value":i[1]} for i in [["Por Municipios",0]]]
    else:
        options = [{"label":i[0],"value":i[1]} for i in [["Por Municipios",0],["Por Unidades",1]]]
        
    return options

@app.callback(
    Output('prop_ANOVA', 'options'),
    [Input('group_ANOVA', 'value')]
)
def update_output(group_value):
    
    if group_value == 1:
        options = [{"label":i[0],"value":i[1]} for i in [["Absoluto",0]]]
    else:
        options = [{"label":i[0],"value":i[1]} for i in [["Absoluto",0],["Cada 100K habitantes",1]]]
        
    return options

@app.callback(
    Output('graph_ANOVA', 'figure'),
    [Input('establecimiento', 'value'),
     Input('institucion', 'value'),
     Input('cat_selector', 'value'),
     Input('subcat_selector', 'value'),
     Input("Outlier_ANOVA","value"), 
     Input("prop_ANOVA", "value"),
     Input("group_ANOVA","value"), 
     Input("norm_ANOVA","value"), 
     Input("std_ANOVA","value")]
)
def update_output(establecimiento_value, institucion_value,
                  cat_value, subcat_value,
                  outlier_value, prop_value, group_value, 
                  norm_value, std_value):

    ### CREAR TABLA CON TODOS LOS MUNICIPIOS
    
    filtro = (none,none,none,none)
    cat = [("Otros","CLUES"),("Otros","Nombre de la Unidad")]
    
    dfTotal = sseOp.loc[filtro,cat]
    dfTotal.columns = dfTotal.columns.droplevel(0)
    dfTotal = dfTotal.reset_index([2,3], drop=True)
    
    ### CREAR TABLA DE MUNICIPIOS CON INFORMACION
    if establecimiento_value == "TODAS":
        establecimiento_value = none
        
    if institucion_value == "TODAS":
        institucion_value = none
    
    filtro = (none,none,establecimiento_value,institucion_value)
    cat = [("Otros","CLUES"),(cat_value,subcat_value)]
    
    dfInfo = sseOp.loc[filtro,cat]
    dfInfo.columns = dfInfo.columns.droplevel(0)
    dfInfo = dfInfo.reset_index([2,3], drop=True)
    
    ###################################################################
    ### GENERAR TABLA CON MUNICIPIOS AUNQUE NO SE TENGA INFORMACION
    
    dfInfo = dfInfo.reset_index([0,1])
    dfTotal = dfTotal.reset_index([0,1])

    dfInfo = dfInfo.set_index(["Nombre Estado","Nombre Municipio","CLUES"])
    dfTotal = dfTotal.set_index(["Nombre Estado","Nombre Municipio","CLUES"])

    df = dfTotal.join(dfInfo, how="left")
    df = df.reset_index([2], drop=True)
    df = df.fillna(0)
    
    ##############################################################
    
    ### DECLARAR CARACTERÍSTICAS DE GRÁFICOS
    Points = "outliers"
    
    if group_value == 0:
        hover = "Nombre Municipio"
        template = "Municipio"
        
        df = df.groupby(["Nombre Estado","Nombre Municipio"]).sum()
        
        if prop_value == 0:
            xValue = subcat_value
            
        else:
            xValue = "C/100K"
            df = df.join(PobMun, how="inner")
            df[xValue] = round((df[subcat_value]*100000)/df["POBTOT"],2)
            
        promedio = round(df.groupby(["Nombre Estado"]).mean(),2)
        STD = round(df.groupby(["Nombre Estado"]).std(ddof = 0),2)
        
        df = df.reset_index([0,1])
        
    else:
        xValue = subcat_value
        hover = "Nombre de la Unidad"
        template = "Unidad"
        
        promedio = round(df.groupby(["Nombre Estado"]).mean(),2)
        STD = round(df.groupby(["Nombre Estado"]).std(ddof = 0),2)
        
        df = df.reset_index([0,1])
    
    if outlier_value == 1:
        Estados = df["Nombre Estado"].unique()
        Points = False
        
        for Estado in Estados:
            DF1 = df[df["Nombre Estado"] == Estado].loc[:,xValue]
            
            Q1 = DF1.quantile(0.25)
            Q3 = DF1.quantile(0.75)
            
            IQR = Q3 - Q1
            Multi = 1.5
            
            conditional = DF1[~((DF1 > Q1 - (Multi*IQR)) & (DF1 < Q3 + (Multi*IQR)))]
            
            df = df.drop(conditional.index)
        
        promedio = round(df.groupby(["Nombre Estado"]).mean(),2)
        STD = round(df.groupby(["Nombre Estado"]).std(ddof = 0),2)
    
    
    if norm_value == 0:
        Norm = abs(promedio - round(df[xValue].mean(),2))
        Norm = (200 - ((Norm/Norm.max())*200)) if (Norm[xValue].max()!=0) else (200 - Norm)
    else:
        Norm = abs(promedio - round(df[xValue].mean(),2))
        Norm = Norm/STD
        Norm[xValue] = Norm[xValue].apply(lambda x: 0 if(np.isnan(x)==True) else x)
        Norm[xValue] = Norm[xValue].apply(lambda x: 1.96 if(x>1.96) else x)
        Norm = 200-(Norm/1.96)*200
    
    
    if std_value == 0:
        BoxMean = False
    else:
        BoxMean = "sd"
    
    

    
    ### GENERAR GRÁFICOS
    
    figANOVA = go.Figure()
    
    for Estado in df["Nombre Estado"].sort_values(ascending=False).unique():
        dfEst = df[df["Nombre Estado"] == Estado]
        color = Norm.loc[Estado,xValue]
        
        figANOVA.add_trace(go.Box(x = dfEst[xValue], name = Estado, boxpoints = Points, whiskerwidth = 0.5,
                                  width = 0.5, boxmean = BoxMean,
                                  marker_color = "rgb(90,90,90)", fillcolor = "rgb({},200,{})".format(color,color),
                                  customdata=dfEst[hover].values, showlegend = False, 
                                  hovertemplate='Value: %{x}' + "<br>" + template + ": %{customdata} </br>"))
        
    
    figANOVA.add_trace(go.Scatter(x = [round(df[xValue].mean(),2),] * df["Nombre Estado"].unique().shape[0], 
                                  y = df["Nombre Estado"].unique(), 
                                  mode="lines", marker=dict(color="#FF0000"),name="Prom. Global", showlegend=True, 
                                  hovertemplate = "Value: %{x}"))
    
    
    figANOVA.add_trace(go.Scatter(x = [i for i in promedio[xValue]], 
                                  y = df["Nombre Estado"].unique(), 
                                  marker_symbol = "diamond-tall", showlegend=True,
                                  mode="markers", marker=dict(color="#020100",size=8), name="Prom. Estatal"))

    figANOVA.update_layout(height = 1500, boxgap=0, boxgroupgap=0.5, showlegend=True)
    
    return figANOVA

if __name__ == '__main__':
    app.run_server(debug=False)

