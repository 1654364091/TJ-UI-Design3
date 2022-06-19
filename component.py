# 看板组件


from dash import dcc, html


def div_dropdown(title, content_list, style):
    return html.Div([
        dcc.Dropdown(
            id=title,
            options=[{'label': i, 'value': i} for i in content_list],
            value=content_list[0]
        )
    ],className=style)


def div_graph(title, style):
    return html.Div([
        dcc.Graph(
            id=title,
            animate=True
        )
    ],className=style)


def div_radio(title,content_list,style):
    return html.Div([
        dcc.RadioItems(
            id=title,
            options=[{'label': i, 'value': i} for i in content_list],
            value=content_list[0],
            labelStyle={'padding': '0 20px', 'display': 'inline-block'}
        )
    ],className=style)

