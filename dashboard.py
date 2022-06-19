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

# 得分
rating_label_list = ['[0,1)', '[1,2)', '[2,3)', '[3,4)', '[4,5)', '5']
rating_value_list = [0 for item in range(len(rating_label_list))]

for index, row in df.iterrows():
    if not np.isnan(row['Rating']):
        rating_value_list[int(float(row['Rating']))] += 1

# 收费情况
fee_label_list = ['Free', 'Paid']
fee_value_list = [0, 0]
for index, row in df.iterrows():
    if row[6] == 'Free':
        fee_value_list[0] += 1
    else:
        fee_value_list[1] += 1

# install-size
sizes, installs = ["0~1M", "1~10M", "10~30M", "30~50M", "50~100M", "100M+"], [0, 0, 0, 0, 0, 0]
for index, row in df.iterrows():
    if row['Size'].endswith("k"):
        installs[0] += 1
    if row['Size'].endswith("M"):
        size = eval(row['Size'].replace("M", ""))
        if 1 <= size < 10:
            installs[1] += 1
        elif 10 <= size < 30:
            installs[2] += 1
        elif 30 <= size < 50:
            installs[3] += 1
        elif 50 <= size < 100:
            installs[4] += 1
        else:
            installs[5] += 1


# 下载量前20的app
install_number_list = []
rank_list = [str(i+1) for i in range(20)]
name_list = []
df.sort_values("Installs",ascending=False,ignore_index=True,inplace=True)
for index,row in df.iterrows():
    if index == 20:
        break
    name_list.append(row["App"])
    install_number_list.append(int(row["Installs"]))
# rank_list.reverse()
# name_list.reverse()
# install_number_list.reverse()
# print(install_number_list)
# print(rank_list)
# print(name_list)


app.layout = html.Div([
    # 背景
    html.Div([], className="bg-style"),
    # 标题
    html.H1('Google Play Store DashBoard', className="title-style"),

    # 下载量排行榜
    dcc.Graph(
        id='Installs-Ranking',
        animate=True,
        figure=create_bar_h(rank_list,"Ranking",install_number_list,"Installs",name_list,"Top 20 Downloaded Apps")
    ),

    html.Hr(),

    # 对比:各评分区间的下载量、评论量
    html.Div([
        div_radio('rating-radio', content_rating_list, "content-rating-radio-style"),

        html.Div([
            # 下载量-评分 柱状图
            div_graph('installs-rating', "bar-style"),
            # 评论量-评分 柱状图
            div_graph('reviews-rating', "bar-style")
        ], className="compare-style"),

        # 细化:4~5 之间的“下载量-评分”、“评论量-评分”
        html.Div([
            # 下载量-评分 柱状图
            div_graph('installs-rating-detail', "bar-style"),
            # 评论量-评分 柱状图
            div_graph('reviews-rating-detail', "bar-style")
        ], className="compare-style")
    ]),

    html.Hr(),

    # 细化:评分占比、收费情况占比
    html.Div([
        # app得分占比情况
        html.Div([
            html.P("Percentage of rating", className="pie-title-style"),
            dcc.Graph(
                id='rating-pie',
                animate=True,
                figure=create_pie(rating_label_list, rating_value_list)
            )
        ], className="pie-style"),
        # app 是否收费占比情况
        html.Div([
            html.P("Charging of fees", className="pie-title-style"),
            dcc.Graph(
                id='fee-pie',
                animate=True,
                figure=create_pie(fee_label_list, fee_value_list)
            )
        ], className="pie-style")
    ], className="compare-style"),

    # 细化：下载量和app大小的关系
    html.Div([
        dcc.Graph(
            id='installs-size',
            animate=True,
            figure=create_scatter(sizes, 'Size', installs, 'Installs', None, 'Installs-AppSize')
        )
    ],className="scatter-style"),

    # html.Hr(),
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
    ratings = ['[4,4.2)', '[4.2,4.4)', '[4.4,4.6)', '[4.6,4.8)', '[4.8,5)', '5']
    reviews = [0, 0, 0, 0, 0, 0]
    installs = [0, 0, 0, 0, 0, 0]
    for index, row in df[(df['Content Rating'] == radio)].iterrows():
        if not np.isnan(row['Rating']):
            pos = int((float(row['Rating']) - 4.0) / 0.2)
            # print(pos)
            if pos >= 0:
                reviews[pos] += row['Reviews']
                installs[pos] += row['Installs']

    return create_bar(ratings, "Rating", installs, "Installs", "Install-Rating(rating:4~5)"), \
           create_bar(ratings, "Rating", reviews, "Reviews", "Review-Rating(rating:4~5)")


if __name__ == '__main__':
    app.run_server(debug=True)
