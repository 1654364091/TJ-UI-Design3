from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# 总数据
df = pd.read_csv(r"data/googleplaystore.csv")

# 取值离散且有限的指标
category_list = df['Category'].unique()
type_list = df['Type'].unique()
content_rating_list = df['Content Rating'].unique()
genres_llist = df['Genres'].unique()

# css样式
title_style = {"margin":"auto auto"}


app.layout = html.Div([
    # 背景
    html.Div([],className="bg-style"),
    # 标题
    html.H1('Google Play Store DashBoard',className="title-style"),


])

if __name__ == '__main__':
    app.run_server(debug=True)
