from dash import Dash, html, dependencies, dcc
import plotly.express as px
import pandas as pd
from component import *
import numpy as np
from utils import *

app = Dash(__name__)

# 总数据
df = pd.read_csv(r"data/googleplaystore.csv")

# 取值离散且有限的指标
category_list = df['Category'].unique()
type_list = df['Type'].unique()
content_rating_list = df['Content Rating'].unique()
genres_llist = df['Genres'].unique()

# css样式
title_style = {"margin": "auto auto"}

app.layout = html.Div([
    # 背景
    html.Div([], className="bg-style"),
    # 标题
    html.H1('Google Play Store DashBoard', className="title-style"),

    # 下载量排行榜
    html.Div([

    ], className="download-rank-style"),

    # 对比:各评分区间的下载量、评论量
    html.Div([
        div_radio('rating-radio', content_rating_list, "content-rating-radio-style"),

        html.Div([
        # 下载量-评分 柱状图
        div_graph('installs-rating', "bar-style"),
        # 评论量-评分 柱状图
        div_graph('reviews-rating', "bar-style")
        ],className="compare-style"),

        # 细化:4~5 之间的“下载量-评分”、“评论量-评分”
        html.Div([
        # 下载量-评分 柱状图
        div_graph('installs-rating-detail', "bar-style"),
        # 评论量-评分 柱状图
        div_graph('reviews-rating-detail', "bar-style")
        ],className="compare-style")
    ]),

    # 细化:评分占比、下载量和app大小的关系
    html.Div([

    ])

    # 溯源:app的详情（待定）
])


@app.callback(
    dependencies.Output('installs-rating', 'figure'),
    dependencies.Output('reviews-rating', 'figure'),
    dependencies.Input('rating-radio', 'value')
)
def refresh_by_rating_radio(radio):
    # 选择一个content rating，更新两个柱状图数据
    ratings = ['[0,1)', '[1,2)', '[2,3)', '[3,4)', '[4,5)', '5']
    reviews = [0, 0, 0, 0, 0, 0]
    installs = [0, 0, 0, 0, 0, 0]
    for index, row in df[(df['Content Rating'] == radio)].iterrows():
        if not np.isnan(row['Rating']):
            reviews[int(float(row['Rating']))] += row['Reviews']
            installs[int(float(row['Rating']))] += row['Installs']

    return create_bar(ratings, "Rating", installs, "Installs", "Install-Rating"), \
           create_bar(ratings, "Rating", reviews, "Reviews", "Review-Rating")


@app.callback(
    dependencies.Output('installs-rating-detail', 'figure'),
    dependencies.Output('reviews-rating-detail', 'figure'),
    dependencies.Input('rating-radio', 'value')
)
def refresh_detail_by_rating_radio(radio):
    # 选择一个content rating，更新两个柱状图数据
    ratings = ['[4,4.2)', '[4.2,4.4)', '[4.4,4.6)', '[4.6,4.8)', '[4.8,5)','5']
    reviews = [0, 0, 0, 0, 0, 0]
    installs = [0, 0, 0, 0, 0, 0]
    for index, row in df[(df['Content Rating'] == radio)].iterrows():
        if not np.isnan(row['Rating']):
            pos = int((float(row['Rating'])-4.0)/0.2)
            # print(pos)
            if pos >= 0:
                reviews[pos] += row['Reviews']
                installs[pos] += row['Installs']

    return create_bar(ratings, "Rating", installs, "Installs", "Install-Rating(rating:4~5)"), \
           create_bar(ratings, "Rating", reviews, "Reviews", "Review-Rating(rating:4~5)")




if __name__ == '__main__':
    app.run_server(debug=True)
