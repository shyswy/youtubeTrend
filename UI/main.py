import dash
from dash import html, dcc, Input, Output, dash_table, State, ctx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import glob
import urllib.parse
from web_crawl import get_youtuber_Ranking
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from word_visualization import generate_Title_WC
from new_tab import video_app
import traceback

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
    # 현재 스크립트의 디렉토리 경로를 가져옴
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'youtube_data')
    
    print(f"Looking for data files in: {data_dir}")
    data_files = glob.glob(os.path.join(data_dir, '*_video.csv'))
    print(f"Found {len(data_files)} data files")
    
    all_data = []
    weekly_data = []
    
    for file in data_files:
        print(f"Processing file: {file}")
        try:
            df = pd.read_csv(file, encoding='utf-8-sig')
            print(f"Successfully loaded {len(df)} rows from {file}")
            
            # 컬럼 이름 변경 및 매핑
            df = df.rename(columns={
                'id': 'video_id',
                'channelTitle': 'channel',
                'viewCount': 'views',
                'likeCount': 'likes',
                'publishedAt': 'published_at'
            })
            
            # 필요한 컬럼만 선택
            df = df[['video_id', 'title', 'channel', 'category', 'views', 'likes', 'description', 'url', 'published_at', 'country']]
            
            # 파일명에서 국가와 카테고리 추출
            file_name = os.path.basename(file)  # 파일 이름만 추출
            country = file_name.split('_')[0]  # KR 또는 US
            category = file_name.split('_')[1] if len(file_name.split('_')) > 1 else 'weekly'
            
            if 'weekly' in file_name:
                df['category_name'] = 'weekly'
                df['country_name'] = '한국' if country == 'KR' else '미국'
                weekly_data.append(df)
                print(f"Added to weekly data: {len(df)} rows")
            else: 
                df['category_name'] = category
                df['country_name'] = '한국' if country == 'KR' else '미국'
                all_data.append(df)
                print(f"Added to all data: {len(df)} rows")
                
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
    
    print(f"Total all_data rows: {sum(len(df) for df in all_data)}")
    print(f"Total weekly_data rows: {sum(len(df) for df in weekly_data)}")
    
    if not all_data and not weekly_data:
        raise ValueError("No data was loaded from any files")
    
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame(), pd.concat(weekly_data, ignore_index=True) if weekly_data else pd.DataFrame()

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

# 클라이언트 사이드 콜백 수정
app.clientside_callback(
    """
    function(data) {
        if (data && data.url) {
            window.open(data.url, '_blank');
            return null;
        }
        return null;
    }
    """,
    Output('dummy-output', 'children'),
    Input('clicked-url', 'data')
)

# 스타일 정의
styles = {
    'container': {
        'padding': '20px',
        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
        'backgroundColor': '#0f0f0f',
        'minHeight': '100vh',
        'color': '#ffffff'
    },
    'header': {
        'textAlign': 'center',
        'marginBottom': '40px',
        'color': '#ffffff',
        'fontSize': '2rem',
        'fontWeight': '500',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'gap': '30px',
        'flexWrap': 'wrap'
    },
    'headerTitle': {
        'display': 'flex',
        'alignItems': 'center',
        'gap': '15px',
        'background': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
        'padding': '20px 40px',
        'borderRadius': '16px',
        'boxShadow': '0 4px 20px rgba(0, 0, 0, 0.2)',
        'transition': 'all 0.3s ease',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'backdropFilter': 'blur(10px)'
    },
    'headerTitle:hover': {
        'transform': 'translateY(-2px)',
        'boxShadow': '0 6px 25px rgba(0, 0, 0, 0.3)',
        'borderColor': 'rgba(255, 255, 255, 0.2)'
    },
    'headerIcon': {
        'fontSize': '2.8rem',
        'color': '#ff0000',
        'filter': 'drop-shadow(0 2px 4px rgba(0,0,0,0.2))'
    },
    'filterContainer': {
        'display': 'flex',
        'alignItems': 'center',
        'gap': '20px',
        'backgroundColor': 'rgba(39, 39, 39, 0.8)',
        'backdropFilter': 'blur(10px)',
        'padding': '15px 25px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.2)',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'filterLabel': {
        'color': '#ffffff',
        'fontSize': '14px',
        'fontWeight': '500',
        'marginRight': '8px',
        'opacity': '0.9'
    },
    'filterDropdown': {
        'backgroundColor': 'rgba(31, 31, 31, 0.9)',
        'color': '#ffffff',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'borderRadius': '8px',
        'padding': '8px 15px',
        'fontSize': '14px',
        'width': '130px',
        'transition': 'all 0.3s ease'
    },
    'filterDropdown:hover': {
        'borderColor': 'rgba(255, 255, 255, 0.2)',
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.2)'
    },
    'mainContent': {
        'display': 'flex',
        'gap': '30px',
        'marginBottom': '40px',
        'maxWidth': '1600px',
        'margin': '0 auto'
    },
    'leftPanel': {
        'flex': '1',
        'padding': '25px',
        'borderRadius': '16px',
        'backgroundColor': 'rgba(31, 31, 31, 0.8)',
        'backdropFilter': 'blur(10px)',
        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.2)',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'rightPanel': {
        'width': '400px',
        'padding': '25px',
        'borderRadius': '16px',
        'backgroundColor': 'rgba(31, 31, 31, 0.8)',
        'backdropFilter': 'blur(10px)',
        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.2)',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'videoList': {
        'marginBottom': '25px',
        'padding': '20px',
        'borderRadius': '12px',
        'backgroundColor': 'rgba(39, 39, 39, 0.8)',
        'backdropFilter': 'blur(10px)',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'videoGridContainer': {
        'display': 'flex',
        'overflow': 'auto',
        'position': 'relative',
        'width': '100%',
        'height': '400px',
        'perspective': '1000px',
        'scrollbarWidth': 'thin',
        'scrollbarColor': '#272727 #1f1f1f',
        'padding': '5px'
    },
    'videoGrid': {
        'display': 'grid',
        'gridTemplateColumns': 'repeat(1, 1fr)',
        'gap': '20px',
        'padding': '10px'
    },
    'videoCard': {
        'borderRadius': '12px',
        'overflow': 'hidden',
        'backgroundColor': 'rgba(39, 39, 39, 0.8)',
        'backdropFilter': 'blur(10px)',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'width': '100%',
        'height': '100%',
        'display': 'flex',
        'flexDirection': 'column',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'videoCard:hover': {
        'transform': 'translateY(-5px)',
        'boxShadow': '0 8px 20px rgba(0, 0, 0, 0.3)',
        'borderColor': 'rgba(255, 255, 255, 0.2)'
    },
    'videoThumbnail': {
        'width': '100%',
        'height': '180px',
        'objectFit': 'cover',
        'borderRadius': '12px 12px 0 0',
        'transition': 'transform 0.3s ease'
    },
    'videoCard:hover .videoThumbnail': {
        'transform': 'scale(1.05)'
    },
    'videoInfo': {
        'padding': '15px',
        'flex': '1',
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '10px'
    },
    'videoTitle': {
        'margin': '0',
        'fontSize': '14px',
        'fontWeight': '500',
        'color': '#ffffff',
        'display': '-webkit-box',
        '-webkit-line-clamp': '2',
        '-webkit-box-orient': 'vertical',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'lineHeight': '1.4'
    },
    'videoChannel': {
        'margin': '0',
        'color': '#aaaaaa',
        'fontSize': '12px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'nowrap',
        'opacity': '0.8'
    },
    'bottomSection': {
        'padding': '20px',
        'borderRadius': '12px',
        'backgroundColor': '#1f1f1f',
        'marginBottom': '20px'
    }
}

# 레이아웃 정의
app.layout = html.Div([
    # 헤더
    html.Div([
        html.Div([
            html.Span("📺", style=styles['headerIcon']),
            html.H1("YouTube 인기 동영상 순위", style={'margin': '0', 'color': '#ffffff'})
        ], style=styles['headerTitle']),
        html.Div([
            html.Div([
                html.Label("국가:", style=styles['filterLabel']),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[
                        {'label': '전체', 'value': '전체'},
                        {'label': '한국', 'value': '한국'},
                        {'label': '미국', 'value': '미국'}
                    ],
                    value='전체',
                    style=styles['filterDropdown']
                )
            ]),
            html.Div([
                html.Label("카테고리:", style=styles['filterLabel']),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': v, 'value': k} for k, v in category_names.items()],
                    value='all',
                    style=styles['filterDropdown']
                )
            ])
        ], style=styles['filterContainer'])
    ], style=styles['header']),
    
    # 메인 콘텐츠 영역
    html.Div([
        # 왼쪽 패널: 순위표
        html.Div([
            html.H3(id='table-title', style={
                'textAlign': 'center',
                'color': '#ffffff',
                'marginBottom': '25px',
                'fontWeight': '600'
            }),
            dash_table.DataTable(
                id='rank-table',
                columns=[
                    {'name': '순위', 'id': 'rank', 'type': 'numeric'},
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
                    'backgroundColor': '#1f1f1f',
                    'margin': '20px 0',
                    'maxHeight': '400px'  # 테이블 최대 높이 제한
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',  # 패딩 줄임
                    'maxWidth': '300px',
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                    'fontSize': '14px',
                    'border': 'none',
                    'color': '#ffffff',
                    'backgroundColor': '#1f1f1f'
                },
                style_header={
                    'backgroundColor': '#272727',
                    'color': '#ffffff',
                    'fontWeight': '500',
                    'fontSize': '14px',
                    'textAlign': 'center',
                    'padding': '10px',  # 패딩 줄임
                    'border': 'none'
                },
                style_data={
                    'cursor': 'pointer',
                    'borderBottom': '1px solid #272727',
                    'transition': 'background-color 0.2s ease',
                    'backgroundColor': '#1f1f1f'
                },
                style_data_conditional=[
                    {
                        'if': {'state': 'active'},
                        'backgroundColor': '#272727',
                        'border': 'none'
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#272727'
                    }
                ],
                page_size=10,
                page_current=0,
                active_cell={'row': 0, 'column': 0}
            ),
            dcc.Store(id='clicked-url'),
        ], style=styles['leftPanel']),
        
        # 오른쪽 패널: 인기 동영상 리스트
        html.Div([
            # 카테고리별 비율 파이 차트
            html.Div([
                html.H4("카테고리별 비율", style={
                    'marginBottom': '20px',
                    'color': '#ffffff',
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
                    'color': '#ffffff',
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
                        for _, row in weekly_df.iterrows()  # 모든 행을 표시
                    ], style=styles['videoGrid'])
                ], style=styles['videoGridContainer']),
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
                html.H3(id='wordcloud-title', style={'textAlign': 'center', 'marginBottom': '20px'}),
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
    }),
    html.Div(id='dummy-output', style={'display': 'none'})  # 이거 필수
], style=styles['container'])

# 콜백 함수
@app.callback(
    Output('clicked-url', 'data'),
    [Input('rank-table', 'active_cell')],
    [State('rank-table', 'data'),
     State('country-dropdown', 'value'),
     State('category-dropdown', 'value')],
    prevent_initial_call=True
)
def open_new_tab(active_cell, table_data, selected_country, selected_category):
    if not active_cell or 'row' not in active_cell or active_cell['column'] != 1:
        return dash.no_update
        
    row = active_cell['row']
    if row >= len(table_data):
        return dash.no_update
        
    title = table_data[row].get('title')
    if not title:
        return dash.no_update
        
    # 해당 title에 맞는 URL을 가져오되, 여러 값이 있을 경우 첫 번째 값만 선택
    url_series = df[df['title'] == title]['url']
    if url_series.empty:
        return dash.no_update
        
    video_id = url_series.iloc[0].split('v=')[-1]
    # 새 탭에서 열릴 Dash 앱의 URL을 생성
    new_tab_url = f'/new_tab?video_id={video_id}&country={selected_country}&category={selected_category}&video_title={urllib.parse.quote(title)}'
    return {'url': new_tab_url}

# 콜백 함수
@app.callback(
    [Output('rank-table', 'data'),
     Output('scatter-plot', 'figure'),
     Output('table-title', 'children'),
     Output('category-dropdown', 'value'),
     Output('rank-table', 'active_cell')],
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('rank-table', 'active_cell'),
     Input('rank-table', 'page_current')]
)
def update_table_and_graph(selected_country, selected_category, active_cell, page_current):
    category_mapping = {
            'all': 'all',
            'entertainment': 'entertainment',
            'news': 'news',
            'people': 'people_blogs',
            'music': 'music',
            'comedy': 'comedy',
            'sports': 'sports'
        }

    category = category_mapping.get(selected_category, 'all')
    # 데이터 필터링
    if category=='all':
        filtered_df = df[df['category'] == 'all']
        # 국가 필터링
        if selected_country != '전체':
            filtered_df = filtered_df[filtered_df['country_name'] == selected_country]
    # 카테고리 필터링 (전체가 아닌 경우에만)
    elif category != 'all':
        filtered_df = df[df['category'] == category]
        # 국가 필터링
        if selected_country != '전체':
            filtered_df = filtered_df[filtered_df['country_name'] == selected_country]

    
    # 순위 계산
    filtered_df = filtered_df.sort_values('views', ascending=False)
    filtered_df['rank'] = range(1, len(filtered_df) + 1)
    
    # 테이블 데이터 준비 (페이지네이션 적용)
    page_size = 10  # 페이지당 10개 행
    start_idx = page_current * page_size
    end_idx = start_idx + page_size
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
    
    # 차트 스타일링
    fig.update_layout(
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='#ffffff'),
        xaxis=dict(
            gridcolor='#272727',
            zerolinecolor='#272727',
            tickfont=dict(color='#ffffff')
        ),
        yaxis=dict(
            gridcolor='#272727',
            zerolinecolor='#272727',
            tickfont=dict(color='#ffffff')
        ),
        legend=dict(
            bgcolor='#1f1f1f',
            bordercolor='#272727',
            borderwidth=1,
            font=dict(color='#ffffff')
        )
    )
    
    # 필터가 변경되면 active_cell 초기화
    if ctx.triggered_id in ['country-dropdown', 'category-dropdown']:
        active_cell = None
    
    return (table_data.to_dict('records'), fig, table_title, 
            selected_category, active_cell)

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
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='#ffffff'),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            bgcolor='#1f1f1f',
            bordercolor='#272727',
            borderwidth=1,
            font=dict(color='#ffffff')
        ),
        margin=dict(t=10, b=60, l=0, r=10),
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
        for _, row in filtered_df.iterrows()  # 모든 행을 표시
    ]

# 워드클라우드 업데이트 콜백
@app.callback(
    Output('word-cloud-img', 'src'),
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_word_cloud(selected_country, selected_category):
    try:
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
        
        print(f"Generating word cloud for country: {country}, category: {category}")
        
        # 워드클라우드 이미지 생성
        img_base64 = generate_Title_WC(country, category)
        if img_base64 is None:
            print("Word cloud generation returned None")
            return None
        
        print("Word cloud generated successfully")
        return img_base64  # 이미 base64 URL이 포함되어 있으므로 그대로 반환
    except Exception as e:
        print(f"Error in update_word_cloud: {str(e)}")
        return None

# 워드클라우드 제목 업데이트 콜백
@app.callback(
    Output('wordcloud-title', 'children'),
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_wordcloud_title(selected_country, selected_category):
    try:
        category_display = category_names.get(selected_category, selected_category)
        return f"{selected_country} {category_display} 워드클라우드"
    except Exception as e:
        print(f"Error in update_wordcloud_title: {str(e)}")
        return "워드클라우드"

# 서버 설정
application = DispatcherMiddleware(app.server, {
    '/new_tab': video_app.server
})

if __name__ == '__main__':
    print("[dash server] run")
    try:
        run_simple('0.0.0.0', 8050, application, use_reloader=True) 
    except Exception as e:
        print("[dash server] error")
        traceback.print_exc()
