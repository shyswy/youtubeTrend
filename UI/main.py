import dash
from dash import html, dcc, Input, Output, dash_table, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import glob
from web_crawl import get_youtuber_Ranking
from word_visualization import generate_Title_WC

# 카테고리 한글 이름 매핑
category_names = {
    'all': '전체',
    'music': '음악',
    'sports': '스포츠',
    'comedy': '코미디',
    'people': 'v-log',
    'entertainment': '엔터테인먼트',
    'news': '뉴스'
}

# 데이터 로드
def load_data():
    data_files = glob.glob('youtube_data/*.csv')
    all_data = []
    weekly_data = []
    
    for file in data_files:
        df = pd.read_csv(file, encoding='utf-8-sig')
        # 파일명에서 국가와 카테고리 추출
        country = file.split('_')[1].split('\\')[-1]
        category = file.split('_')[2] if len(file.split('_')) > 2 else 'weekly'
        
        if 'weekly' in file:
            df['category_name'] = 'weekly'
            df['country_name'] = '한국' if country == 'korea' or country == 'KR' else '미국'
            weekly_data.append(df)
        else:
            df['category_name'] = category
            df['country_name'] = '한국' if country == 'korea' or country == 'KR' else '미국'
            all_data.append(df)
    
    return pd.concat(all_data, ignore_index=True), pd.concat(weekly_data, ignore_index=True) if weekly_data else None

# 크롤링 데이터 로드 함수 추가
def load_crawled_data():
    crawled_data = get_youtuber_Ranking()
    return pd.DataFrame(crawled_data)

# 데이터 로드
df, weekly_df = load_data()
crawled_df = load_crawled_data()

# Dash 앱 생성
app = dash.Dash(__name__)
app.title = "YouTube 인기 동영상 순위"
app.config.suppress_callback_exceptions = True  # 콜백 예외 허용

# 스타일 정의
styles = {
    'container': {
        'padding': '30px',
        'fontFamily': "'Noto Sans KR', sans-serif",
        'backgroundColor': '#f8f9fa',
        'minHeight': '100vh'
    },
    'header': {
        'textAlign': 'center',
        'marginBottom': '40px',
        'color': '#2c3e50',
        'fontSize': '2.5rem',
        'fontWeight': '700',
        'textShadow': '2px 2px 4px rgba(0,0,0,0.1)'
    },
    'mainContent': {
        'display': 'flex',
        'gap': '30px',
        'marginBottom': '40px'
    },
    'leftPanel': {
        'flex': '1',
        'padding': '25px',
        'borderRadius': '15px',
        'boxShadow': '0 8px 16px rgba(0,0,0,0.1)',
        'backgroundColor': 'white',
        'transition': 'transform 0.3s ease'
    },
    'rightPanel': {
        'width': '400px',
        'padding': '25px',
        'borderRadius': '15px',
        'boxShadow': '0 8px 16px rgba(0,0,0,0.1)',
        'backgroundColor': 'white',
        'transition': 'transform 0.3s ease'
    },
    'filterSection': {
        'marginBottom': '30px',
        'padding': '20px',
        'borderRadius': '12px',
        'backgroundColor': 'white',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.05)',
        'textAlign': 'right',
        'marginRight': '20px'
    },
    'videoList': {
        'marginBottom': '30px',
        'padding': '20px',
        'borderRadius': '12px',
        'backgroundColor': 'white',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.05)'
    },
    'videoGrid': {
        'display': 'grid',
        'gridTemplateColumns': 'repeat(3, 1fr)',
        'gap': '15px',
        'overflow': 'hidden',
        'position': 'relative',
        'width': '100%',
        'height': '100%'
    },
    'videoGridContainer': {
        'display': 'flex',
        'overflow': 'hidden',
        'position': 'relative',
        'width': '100%',
        'height': '300px',
        'perspective': '1000px',
        'maxWidth': '1200px',
        'margin': '0 auto'
    },
    'videoCard': {
        'borderRadius': '12px',
        'overflow': 'hidden',
        'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
        'cursor': 'pointer',
        'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
        'backgroundColor': 'white',
        'width': '100%',
        'height': '100%',
        'display': 'flex',
        'flexDirection': 'column',
        'transform': 'scale(1)',
        'transformOrigin': 'center center'
    },
    'videoCard:hover': {
        'transform': 'translateY(-5px)',
        'boxShadow': '0 8px 16px rgba(0,0,0,0.2)'
    },
    'videoThumbnail': {
        'width': '100%',
        'height': '180px',
        'objectFit': 'cover',
        'borderRadius': '12px 12px 0 0'
    },
    'videoInfo': {
        'padding': '15px',
        'flex': '1',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'space-between'
    },
    'videoTitle': {
        'margin': '0',
        'fontSize': '14px',
        'fontWeight': '600',
        'color': '#2c3e50',
        'display': '-webkit-box',
        '-webkit-line-clamp': '2',
        '-webkit-box-orient': 'vertical',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis'
    },
    'videoChannel': {
        'margin': '10px 0 0 0',
        'color': '#666',
        'fontSize': '12px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'nowrap'
    },
    'bottomSection': {
        'padding': '30px',
        'borderRadius': '15px',
        'boxShadow': '0 8px 16px rgba(0,0,0,0.1)',
        'marginBottom': '30px',
        'backgroundColor': 'white'
    }
}

# 레이아웃 정의
app.layout = html.Div([
    # 헤더
    html.Div([
        html.H1("📺 YouTube 인기 동영상 순위", style=styles['header']),
    ]),
    
    # 필터 섹션
    html.Div([
        html.Div([
            html.Label("국가 선택:", style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='country-dropdown',
                options=[
                    {'label': '전체', 'value': '전체'},
                    {'label': '한국', 'value': '한국'},
                    {'label': '미국', 'value': '미국'}
                ],
                value='전체',
                style={'width': '150px', 'display': 'inline-block', 'marginRight': '20px'}
            ),
            html.Label("카테고리 선택:", style={'marginRight': '10px'}),
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': v, 'value': k} for k, v in category_names.items()],
                value='all',
                style={'width': '150px', 'display': 'inline-block'}
            )
        ], style=styles['filterSection'])
    ]),
    
    # 메인 콘텐츠 영역
    html.Div([
        # 왼쪽 패널: 순위표
        html.Div([
            html.H3(id='table-title', style={
                'textAlign': 'center',
                'color': '#2c3e50',
                'marginBottom': '25px',
                'fontWeight': '600'
            }),
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
                    'border': 'none',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 8px rgba(0,0,0,0.05)',
                    'margin': '20px 0'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '15px',
                    'maxWidth': '300px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'fontFamily': "'Noto Sans KR', sans-serif",
                    'fontSize': '14px',
                    'border': 'none'
                },
                style_header={
                    'backgroundColor': '#2c3e50',
                    'color': 'white',
                    'fontWeight': '600',
                    'fontSize': '15px',
                    'textAlign': 'center',
                    'padding': '15px',
                    'border': 'none'
                },
                style_data={
                    'cursor': 'pointer',
                    'borderBottom': '1px solid #eee',
                    'transition': 'background-color 0.3s ease'
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
                page_size=10,
                page_current=0,
                active_cell=None
            )
        ], style=styles['leftPanel']),
        
        # 오른쪽 패널: 인기 동영상 리스트
        html.Div([
            # 카테고리별 비율 파이 차트
            html.Div([
                html.H4("카테고리별 비율", style={
                    'marginBottom': '20px',
                    'color': '#2c3e50',
                    'fontWeight': '600'
                }),
                dcc.Graph(
                    id='category-pie-chart',
                    style={
                        'height': '300px',
                        'width': '100%'
                    }
                )
            ], style=styles['videoList']),
            
            # 주간 인기 동영상
            html.Div([
                html.H4("주간 인기 동영상", style={
                    'marginBottom': '20px',
                    'color': '#2c3e50',
                    'fontWeight': '600'
                }),
                html.Div([
                    html.Div(id='weekly-videos-container', children=[
                        html.A(
                            href=row['url'],
                            target='_blank',
                            style={'textDecoration': 'none', 'color': 'inherit', 'width': '100%'},
                            children=[
                                html.Div([
                                    html.Img(src=f"https://img.youtube.com/vi/{row['video_id']}/mqdefault.jpg", 
                                            style=styles['videoThumbnail']),
                                    html.Div([
                                        html.H5(row['title'], style=styles['videoTitle']),
                                        html.P(row['channel'], style=styles['videoChannel'])
                                    ], style=styles['videoInfo'])
                                ], style=styles['videoCard'])
                            ]
                        )
                        for _, row in weekly_df.head(3).iterrows() if weekly_df is not None
                    ], style=styles['videoGrid'])
                ], style=styles['videoGridContainer'])
            ], style=styles['videoList'])
        ], style=styles['rightPanel']),
    ], style=styles['mainContent']),
    
    # 하단 섹션
    html.Div([
        # 상단 그리드 (조회수 vs 좋아요 분석 + 워드클라우드)
        html.Div([
            # 조회수 vs 좋아요 분석
            html.Div([
                html.H3("조회수 vs 좋아요 분석", style={'textAlign': 'center', 'marginBottom': '20px'}),
                dcc.Graph(id='scatter-plot', style={'height': '500px'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': 'white',
                'borderRadius': '15px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
                'marginRight': '20px'
            }),
            
            # 워드클라우드
            html.Div([
                html.H3("동영상 제목 워드클라우드", style={'textAlign': 'center', 'marginBottom': '20px'}),
                html.Div([
                    html.Img(
                        id='word-cloud-img',
                        style={
                            'width': '100%',
                            'height': '500px',
                            'objectFit': 'contain',
                            'border': '2px solid #ccc',
                            'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
                            'borderRadius': '10px'
                        }
                    )
                ], style={'textAlign': 'center'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': 'white',
                'borderRadius': '15px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
            })
        ], style={
            'display': 'flex',
            'marginBottom': '30px',
            'gap': '20px'
        }),
        
        # 실시간 인기 유튜버
        html.Div([
            html.H3("실시간 인기 유튜버", style={'textAlign': 'center', 'marginBottom': '20px'}),
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
                    'width': '800px',
                    'overflowY': 'hidden',
                    'margin': '0 auto'
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
        ], style={
            'padding': '20px',
            'backgroundColor': 'white',
            'borderRadius': '15px',
            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'textAlign': 'center'
        })
    ], style={
        'padding': '30px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '15px',
        'marginTop': '30px'
    })
], style=styles['container'])

# 콜백 함수
@app.callback(
    [Output('rank-table', 'data'),
     Output('scatter-plot', 'figure'),
     Output('table-title', 'children'),
     Output('category-dropdown', 'value')],
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('rank-table', 'page_current')]
)
def update_table_and_graph(selected_country, selected_category, page_current):
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
    
    # 테이블 데이터 준비 (페이지네이션 적용)
    start_idx = page_current * 10
    end_idx = start_idx + 10
    table_data = filtered_df[['rank', 'title', 'channel', 'views', 'likes', 'category']].iloc[start_idx:end_idx]
    
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
    
    return table_data.to_dict('records'), fig, table_title, selected_category

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

# 콜백 함수 추가
@app.callback(
    Output('category-pie-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_pie_chart(selected_country):
    # 데이터 필터링
    filtered_df = df.copy()
    if selected_country != '전체':
        filtered_df = filtered_df[filtered_df['country_name'] == selected_country]
    
    # 카테고리별 동영상 수 계산
    category_counts = filtered_df['category_name'].value_counts()
    
    # 파이 차트 생성
    fig = px.pie(
        values=category_counts.values,
        names=category_counts.index,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # 차트 스타일링
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>비율: %{percent}<br>개수: %{value}'
    )
    
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=2,
            tracegroupgap=1
        ),
        margin=dict(t=10, b=60, l=0, r=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=400,
        height=300
    )
    
    return fig

# 주간 인기 동영상 업데이트 콜백
@app.callback(
    Output('weekly-videos-container', 'children'),
    [Input('country-dropdown', 'value')]
)
def update_weekly_videos(selected_country):
    if weekly_df is None:
        return []
    
    filtered_df = weekly_df.copy()
    if selected_country != '전체':
        filtered_df = filtered_df[filtered_df['country_name'] == selected_country]
    
    return [
        html.A(
            href=row['url'],
            target='_blank',
            style={'textDecoration': 'none', 'color': 'inherit', 'width': '100%'},
            children=[
                html.Div([
                    html.Img(src=f"https://img.youtube.com/vi/{row['video_id']}/mqdefault.jpg", 
                            style=styles['videoThumbnail']),
                    html.Div([
                        html.H5(row['title'], style=styles['videoTitle']),
                        html.P(row['channel'], style=styles['videoChannel'])
                    ], style=styles['videoInfo'])
                ], style=styles['videoCard'])
            ]
        )
        for _, row in filtered_df.head(3).iterrows()
    ]

# 워드클라우드 업데이트 콜백
@app.callback(
    Output('word-cloud-img', 'src'),
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_word_cloud(selected_country, selected_category):
    # 국가와 카테고리 매핑
    country_mapping = {
        '한국': 'KR',
        '미국': 'US',
        '전체': 'KR'  # 기본값
    }
    
    category_mapping = {
        'all': 'all',
        'entertainment': 'entertainment',
        'news': 'news',
        'people': 'people_blogs',
        'music': 'music',
        'comedy': 'comedy',
        'sports': 'sports'
    }
    
    country = country_mapping.get(selected_country, 'KR')
    category = category_mapping.get(selected_category, 'all')
    
    # 워드클라우드 이미지 생성
    img_base64 = generate_Title_WC(country, category)
    if img_base64 is None:
        return None
    
    return img_base64

# 서버 실행
if __name__ == '__main__':
    app.run_server(debug=True) 
    
