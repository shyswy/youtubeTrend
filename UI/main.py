import dash
from dash import html, dcc, Input, Output, dash_table, State
import plotly.express as px
import pandas as pd
import os
import glob
from web_crawl import get_youtuber_Ranking

# 카테고리 한글 이름 매핑
category_names = {
    'all': '전체',
    'music': '음악',
    'sports': '스포츠',
    'comedy': '코미디',
    'entertainment': '엔터테인먼트',
    'news': '뉴스'
}

# 데이터 로드
def load_data():
    data_files = glob.glob('youtube_data/*.csv')
    all_data = []
    
    for file in data_files:
        df = pd.read_csv(file, encoding='utf-8-sig')
        # 파일명에서 국가와 카테고리 추출
        country = file.split('_')[1].split('\\')[-1]
        category = file.split('_')[2]
        df['category_name'] = category
        df['country_name'] = '한국' if country == 'korea'or country == 'KR' else '미국'
        all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True)

# 크롤링 데이터 로드 함수 추가
def load_crawled_data():
    crawled_data = get_youtuber_Ranking()
    return pd.DataFrame(crawled_data)

# 데이터 로드
df = load_data()
crawled_df = load_crawled_data()

# Dash 앱 생성
app = dash.Dash(__name__)
app.title = "YouTube 인기 동영상 순위"

# 레이아웃 정의
app.layout = html.Div([
    # 헤더
    html.Div([
        html.H1("📺 YouTube 인기 동영상 순위", 
                style={'textAlign': 'center', 'margin-bottom': '20px'}),
    ]),
    
    # 필터 섹션
    html.Div([
        html.Div([
            html.Label("국가 선택:"),
            dcc.Dropdown(
                id='country-dropdown',
                options=[
                    {'label': '한국', 'value': '한국'},
                    {'label': '미국', 'value': '미국'},
                    {'label': '전체', 'value': '전체'}
                ],
                value='한국',
                style={'width': '200px'}
            ),
        ], style={'display': 'inline-block', 'margin-right': '20px'}),
        
        html.Div([
            html.Label("카테고리 선택:"),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': v, 'value': k} for k, v in category_names.items()],
                value='all',
                style={'width': '200px'}
            ),
        ], style={'display': 'inline-block'}),
    ], style={'padding': '20px', 'borderBottom': '1px solid #ccc'}),
    
    # 메인 콘텐츠 영역
    html.Div([
        # 왼쪽: 순위표
        html.Div([
            html.H3(id='table-title', style={'textAlign': 'center'}),
            dash_table.DataTable(
                id='rank-table',
                columns=[
                    {'name': '순위', 'id': 'rank'},
                    {'name': '제목', 'id': 'title'},
                    {'name': '채널', 'id': 'channel'},
                    {'name': '조회수', 'id': 'views', 'type': 'numeric', 'format': {'specifier': ','}},
                    {'name': '좋아요', 'id': 'likes', 'type': 'numeric', 'format': {'specifier': ','}},
                    {'name': '카테고리', 'id': 'category'}
                ],
                style_table={
                    'overflowX': 'auto',
                    'border': '1px solid #ddd',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
                    'margin': '20px 0'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '12px',
                    'maxWidth': '300px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'fontFamily': 'Arial, sans-serif',
                    'fontSize': '14px',
                    'border': 'none'
                },
                style_header={
                    'backgroundColor': '#2c3e50',
                    'color': 'white',
                    'fontWeight': 'bold',
                    'fontSize': '15px',
                    'textAlign': 'center',
                    'padding': '15px',
                    'border': 'none'
                },
                style_data={
                    'cursor': 'pointer',
                    'borderBottom': '1px solid #eee'
                },
                style_data_conditional=[
                    {
                        'if': {'state': 'active'},
                        'backgroundColor': 'rgba(44, 62, 80, 0.1)',
                        'border': '1px solid #2c3e50'
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgba(0, 0, 0, 0.02)'
                    }
                ],
                page_size=5,
                page_current=0,
                active_cell={'row': 0, 'column': 0}
            )
        ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'}),
        
        # 오른쪽: 동영상 플레이어
        html.Div([
            html.H3(id='video-title', style={'textAlign': 'center'}),
            html.Iframe(
                id='video-player',
                style={'width': '100%', 'height': '400px', 'border': 'none'}
            )
        ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'})
    ], style={'display': 'flex'}),
    
    # 그래프 섹션
    html.Div([
        html.H3("조회수 vs 좋아요 분석", style={'textAlign': 'center'}),
        html.Div([
            dcc.Graph(id='scatter-plot'),
            html.Div([
                html.H3("실시간 인기 유튜버", style={'textAlign': 'center'}),
                dash_table.DataTable(
                    id='youtuber-table',
                    columns=[
                        {'name': '순위', 'id': 'rank'},
                        {'name': '채널명', 'id': 'channel_name'},
                        {'name': '채널 이미지', 'id': 'channel_image', 'presentation': 'markdown'}
                    ],
                    data=[{
                        'rank': row['rank'],
                        'channel_name': row['channel_name'],
                        'channel_link': row['channel_link'],
                        'channel_image': f"![{row['channel_name']}]({row['channel_image']})"
                    } for row in crawled_df.to_dict('records')],
                    style_table={
                        'border': '2px solid #e74c3c',
                        'borderRadius': '12px',
                        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
                        'background': 'linear-gradient(to bottom right, #ffffff, #f8f9fa)',
                        'height': '180px',
                        'width': '400px',
                        'overflowY': 'hidden',
                        'marginTop': '20px',
                        'marginLeft': 'auto',
                        'marginRight': 'auto'
                    },
                    style_cell={
                        'textAlign': 'center',
                        'padding': '8px',
                        'whiteSpace': 'normal',
                        'height': '150px',
                        'fontFamily': '"Noto Sans KR", Arial, sans-serif',
                        'fontSize': '13px',
                        'border': 'none',
                        'verticalAlign': 'middle'
                    },
                    style_header={
                        'backgroundColor': '#e74c3c',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'fontSize': '14px',
                        'textAlign': 'center',
                        'padding': '8px',
                        'border': 'none',
                        'borderTopLeftRadius': '10px',
                        'borderTopRightRadius': '10px',
                        'height': '30px'
                    },
                    style_data={
                        'backgroundColor': 'transparent',
                        'cursor': 'default',
                        'borderBottom': '1px solid #f2f2f2',
                        'height': '150px',
                        'verticalAlign': 'middle'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': 'rank'}, 
                         'width': '15%',
                         'fontSize': '20px',
                         'fontWeight': 'bold',
                         'color': '#e74c3c'},
                        {'if': {'column_id': 'channel_name'}, 
                         'width': '35%',
                         'textAlign': 'left',
                         'paddingLeft': '10px',
                         'fontSize': '14px'},
                        {'if': {'column_id': 'channel_image'}, 
                         'width': '50%',
                         'maxWidth': '100px',
                         'maxHeight': '80px',
                         'objectFit': 'contain'}
                    ],
                    style_data_conditional=[
                        {
                            'if': {'row_index': 0},
                            'backgroundColor': 'rgba(231, 76, 60, 0.05)',
                            'transition': 'background-color 0.3s ease'
                        }
                    ],
                    page_size=1,
                    markdown_options={'html': True}
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=1700,  # 1.7초마다 업데이트
                    n_intervals=0
                )
            ], style={'textAlign': 'center'})
        ], style={'display': 'block'})
    ], style={'padding': '20px'}),
])

# 콜백 함수
@app.callback(
    [Output('rank-table', 'data'),
     Output('scatter-plot', 'figure'),
     Output('table-title', 'children'),
     Output('category-dropdown', 'value'),
     Output('video-player', 'src'),
     Output('video-title', 'children'),
     Output('rank-table', 'active_cell')],
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('rank-table', 'active_cell'),
     Input('rank-table', 'page_current')]
)
def update_table_and_graph(selected_country, selected_category, active_cell, page_current):
    # 국가가 변경되면 카테고리를 'all'로 초기화
    ctx = dash.callback_context
    if ctx.triggered[0]['prop_id'] == 'country-dropdown.value':
        selected_category = 'all'
    
    # 데이터 필터링
    filtered_df = df.copy()
    
    # 국가 필터링
    if selected_country != '전체':
        filtered_df = filtered_df[filtered_df['country_name'] == selected_country]
    
    # 카테고리 필터링 (전체가 아닌 경우에만)
    if selected_category != 'all':
        filtered_df = filtered_df[filtered_df['category_name'] == selected_category]
    
    # 순위 계산
    filtered_df = filtered_df.sort_values('views', ascending=False)
    filtered_df['rank'] = range(1, len(filtered_df) + 1)
    
    # 테이블 데이터 준비
    table_data = filtered_df[['rank', 'title', 'channel', 'views', 'likes', 'category']].head(50)
    
    # 테이블 제목 설정
    category_text = category_names[selected_category]
    table_title = f"{selected_country} {category_text} 인기 동영상 순위"
    
    # 산점도 생성
    fig = px.scatter(
        filtered_df.head(50),
        x='views',
        y='likes',
        color='category',
        hover_data=['title', 'channel'],
        log_x=True,
        log_y=True
    )
    
    # 동영상 URL과 제목 설정
    video_url = ""
    video_title = ""
    new_active_cell = None
    
    if active_cell and active_cell['row'] is not None:
        # 페이지 번호를 고려하여 실제 데이터의 인덱스 계산
        row_index = page_current * 5 + active_cell['row']  # 페이지당 5개 행
        if row_index < len(filtered_df):
            video_id = filtered_df.iloc[row_index]['url'].split('v=')[-1]
            video_url = f"https://www.youtube.com/embed/{video_id}"
            video_title = filtered_df.iloc[row_index]['title']
            new_active_cell = active_cell
    else:
        # 활성화된 셀이 없으면 현재 페이지의 첫 번째 행 표시
        if len(filtered_df) > 0:
            start_idx = page_current * 5  # 페이지당 5개 행
            if start_idx < len(filtered_df):
                video_id = filtered_df.iloc[start_idx]['url'].split('v=')[-1]
                video_url = f"https://www.youtube.com/embed/{video_id}"
                video_title = filtered_df.iloc[start_idx]['title']
                new_active_cell = {'row': 0, 'column': 0}
    
    return (table_data.to_dict('records'), fig, table_title, 
            selected_category, video_url, video_title, new_active_cell)

# 유튜버 테이블 자동 순환 콜백
@app.callback(
    Output('youtuber-table', 'data'),
    [Input('interval-component', 'n_intervals')],
    [State('youtuber-table', 'data')]
)
def update_youtuber_table(n_intervals, current_data):
    if not current_data:
        return []
    
    # 현재 데이터의 순위를 가져옴
    current_rank = int(current_data[0]['rank'])
    
    # 다음 순위 계산 (1부터 시작)
    next_rank = (current_rank % len(crawled_df)) + 1
    
    # 다음 순위의 데이터 찾기
    next_data = [row for row in crawled_df.to_dict('records') if int(row['rank']) == next_rank]
    
    if next_data:
        return [{
            'rank': next_data[0]['rank'],
            'channel_name': next_data[0]['channel_name'],
            'channel_link': next_data[0]['channel_link'],
            'channel_image': f"![{next_data[0]['channel_name']}]({next_data[0]['channel_image']})"
        }]
    
    return current_data

# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True) 