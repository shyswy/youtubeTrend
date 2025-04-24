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
app = dash.Dash(__name__, 
    suppress_callback_exceptions=True,
    external_stylesheets=['https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap']
)

# 앱 스타일 추가
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .Select-control, .Select-menu-outer {
                background-color: #1f1f1f !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            .Select-menu-outer {
                z-index: 9999 !important;
            }
            .Select-value-label, .Select-option {
                color: white !important;
            }
            .Select-option:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            .Select-arrow {
                border-color: white transparent transparent !important;
            }
            .Select.is-open > .Select-control {
                background-color: #1f1f1f !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
            }
            .Select-placeholder {
                color: rgba(255, 255, 255, 0.5) !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.title = "YouTube 인기 동영상 순위"

# 클라이언트 사이드 콜백만 사용하도록 수정

app.clientside_callback(
    """
    function(data) {
        if (data && data.url && !window.lastOpenedUrl) {
            window.lastOpenedUrl = data.url;
            window.open(data.url, '_blank');
            setTimeout(() => {
                window.lastOpenedUrl = null;
            }, 1000);
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
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'position': 'relative',
        'zIndex': 1000
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
        'transition': 'all 0.3s ease',
        'cursor': 'pointer',
        'fontFamily': "'Noto Sans KR', sans-serif",
        'fontWeight': '400'
    },
    'filterDropdown:hover': {
        'borderColor': 'rgba(255, 255, 255, 0.2)',
        'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.2)'
    },
    'pagination': {
        'display': 'flex',
        'justifyContent': 'center',
        'alignItems': 'center',
        'gap': '15px',
        'marginTop': '5px',
        'backgroundColor': 'rgba(39, 39, 39, 0.8)',
        'padding': '15px',
        'borderRadius': '12px',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'paginationButton': {
        'backgroundColor': 'rgba(39, 39, 39, 0.8)',
        'color': '#ffffff',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'borderRadius': '8px',
        'padding': '8px 15px',
        'fontSize': '14px',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'minWidth': '80px'
    },
    'paginationButton:hover': {
        'backgroundColor': 'rgba(255, 255, 255, 0.1)',
        'borderColor': 'rgba(255, 255, 255, 0.2)'
    },
    'paginationInfo': {
        'color': '#ffffff',
        'fontSize': '14px',
        'padding': '8px 15px',
        'backgroundColor': 'rgba(31, 31, 31, 0.8)',
        'borderRadius': '8px',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'minWidth': '150px',
        'textAlign': 'center'
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
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'display': 'flex',
        'flexDirection': 'column',
        'gap': '20px'
    },
    'rightPanel': {
        'width': '450px',
        'padding': '25px',
        'borderRadius': '16px',
        'backgroundColor': 'rgba(31, 31, 31, 0.8)',
        'backdropFilter': 'blur(10px)',
        'boxShadow': '0 4px 15px rgba(0, 0, 0, 0.2)',
        'border': '1px solid rgba(255, 255, 255, 0.1)'
    },
    'videoList': {
        'marginBottom': '10px',
        'padding': '20px',
        'borderRadius': '12px',
        'backgroundColor': 'rgba(39, 39, 39, 0.8)',
        'backdropFilter': 'blur(10px)',
        'border': '1px solid rgba(255, 255, 255, 0.1)',
        'height': '375px'
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
                html.Label("Country", style=styles['filterLabel']),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[
                        {'label': '전체', 'value': '전체'},
                        {'label': '한국', 'value': '한국'},
                        {'label': '미국', 'value': '미국'}
                    ],
                    value='전체',
                    style={
                        'backgroundColor': 'rgba(31, 31, 31, 0.9)',
                        'color': '#ffffff',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                        'borderRadius': '8px',
                        'padding': '8px 15px',
                        'fontSize': '14px',
                        'width': '130px',
                        'fontFamily': "'Noto Sans KR', sans-serif",
                        'fontWeight': '400'
                    },
                    className='custom-dropdown',
                    clearable=False,
                    optionHeight=35
                )
            ]),
            html.Div([
                html.Label("Category", style=styles['filterLabel']),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': v, 'value': k} for k, v in category_names.items()],
                    value='all',
                    style={
                        'backgroundColor': 'rgba(31, 31, 31, 0.9)',
                        'color': '#ffffff',
                        'border': '1px solid rgba(255, 255, 255, 0.1)',
                        'borderRadius': '8px',
                        'padding': '8px 15px',
                        'fontSize': '14px',
                        'width': '130px',
                        'fontFamily': "'Noto Sans KR', sans-serif",
                        'fontWeight': '400'
                    },
                    className='custom-dropdown',
                    clearable=False,
                    optionHeight=35
                )
            ])
        ], style=styles['filterContainer'])
    ], style=styles['header']),
    
    # 메인 콘텐츠 영역
    html.Div([
        # 왼쪽 패널: 순위표
        html.Div([
            # 인기 동영상 순위 테이블
            html.H3(id='table-title', style={
                'textAlign': 'center',
                'color': '#ffffff',
                'marginBottom': '10px',
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
                    'margin': '5px 0',
                    'maxHeight': '400px'
                },
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
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
                    'fontWeight': '600',
                    'fontSize': '15px',
                    'textAlign': 'center',
                    'padding': '12px',
                    'border': 'none',
                    'borderBottom': '2px solid rgba(255, 255, 255, 0.1)',
                    'height': '50px'
                },
                style_data={
                    'backgroundColor': '#1f1f1f',
                    'borderBottom': '1px solid rgba(255, 255, 255, 0.1)'
                },
                css=[ {
                    'selector': 'td.cell--channel_name a',
                    'rule': '''
                        color: #ffffff !important;
                        text-decoration: none !important;
                        display: inline-block !important;
                        width: 100% !important;
                        text-align: center !important;
                        padding: 8px 0 !important;ㄴ
                        line-height: 64px !important;
                    '''
                }],
                style_cell_conditional=[
                    {'if': {'column_id': 'rank'}, 
                     'width': '100px',
                     'fontSize': '20px',
                     'fontWeight': 'bold',
                     'color': '#e74c3c'}
                ],
                page_size=10,
                page_current=0,
                active_cell={'row': 0, 'column': 0}
            ),
            # 페이지네이션 버튼
            html.Div([
                html.Button('이전', id='prev-page', style=styles['paginationButton']),
                html.Div(id='page-info', style=styles['paginationInfo']),
                html.Button('다음', id='next-page', style=styles['paginationButton'])
            ], style=styles['pagination']),
            
            dcc.Store(id='current-page', data=0),  # 현재 페이지 저장
            dcc.Store(id='total-pages', data=0),  # 총 페이지 수 저장
            dcc.Store(id='clicked-url'),
            
            # 실시간 인기 유튜버 테이블
            html.Div([
                html.H3("실시간 인기 유튜버", style={
                    'color': '#ffffff',
                    'marginTop': '30px',
                    'marginBottom': '20px',
                    'fontWeight': '600',
                    'width': '100%',
                    'textAlign': 'center'
                }),
                dash_table.DataTable(
                    id='youtuber-table',
                    columns=[
                        {'name': '순위', 'id': 'rank', 'width': '80px'},
                        {'name': '채널명', 'id': 'channel_name', 'width': '200px', 'presentation': 'markdown'},
                        {'name': '채널 이미지', 'id': 'channel_image', 'presentation': 'markdown', 'width': '200px'}
                    ],
                    data=[{
                        'rank': row['rank'],
                        'channel_name': f"[{row['channel_name']}]({row['channel_link']})",
                        'channel_image': f"[![{row['channel_name']}]({row['channel_image']})]({row['channel_link']})"
                    } for row in crawled_df.to_dict('records')],
                    markdown_options={'html': True, 'link_target': '_blank'},
                    style_table={
                        'border': 'none',
                        'borderRadius': '12px',
                        'backgroundColor': '#1f1f1f',
                        'width': '100%',
                        'tableLayout': 'fixed'
                    },
                    style_cell={
                        'textAlign': 'center',
                        'padding': '8px',
                        'backgroundColor': '#1f1f1f',
                        'color': '#ffffff',
                        'border': 'none',
                        'height': '80px',
                        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                        'fontSize': '14px'
                    },
                    style_header={
                        'backgroundColor': '#272727',
                        'fontWeight': '600',
                        'fontSize': '15px',
                        'borderBottom': '2px solid rgba(255, 255, 255, 0.1)',
                        'height': '50px',
                        'textAlign': 'center',
                    },
                    style_data={
                        'borderBottom': '1px solid rgba(255, 255, 255, 0.1)'
                    },
                    css=[{
                        'selector': 'td.cell--channel_name a',
                        'rule': '''
                            color: #ffffff;
                            text-decoration: none !important;
                            display: inline-block;
                            width: 100%;
                        '''
                    }, {
                        'selector': '.dash-table-container td.cell--channel_image img, .dash-table-container td.cell--channel_image a img',
                        'rule': '''
                            padding-left: 60px !important;
                            display: inline-block !important;
                            vertical-align: middle !important;
                        '''
                    }, {
                        'selector': '.dash-cell-value a',
                        'rule': '''
                            color: #ffffff !important;
                            text-decoration: none !important;
                        '''
                    }],
                    style_cell_conditional=[
                        {'if': {'column_id': 'rank'}, 
                         'width': '80px',
                         'fontSize': '20px',
                         'fontWeight': 'bold',
                         'color': '#e74c3c'},
                        {'if': {'column_id': 'channel_name'},
                         'width': '200px',
                         'minWidth': '200px',
                         'maxWidth': '200px'},
                        {'if': {'column_id': 'channel_image'},
                         'width': '200px',
                         'minWidth': '200px',
                         'maxWidth': '200px'}
                    ],
                    style_data_conditional=[
                        {
                            'if': {'column_id': 'channel_image'},
                            'paddingLeft': '50px'
                        }
                    ],
                    page_size=1
                ),
                dcc.Location(id='url', refresh=False),
                dcc.Interval(
                    id='interval-component',
                    interval=1700,
                    n_intervals=0
                )
            ], style={
                'width': '50%',
                'margin': '0',
                'display': 'flex',
                'flexDirection': 'column',
                'alignItems': 'left',
                'marginBottom': '10px',
                'marginLeft': '0'
            })
        ], style=styles['leftPanel']),
        
        # 오른쪽 패널: 인기 동영상 리스트
        html.Div([
            # 카테고리별 비율 파이 차트
            html.Div([
                html.H4("카테고리별 비율", style={
                    'marginBottom': '8px',
                    'marginTop': '8px',
                    'color': '#ffffff',
                    'fontWeight': '600'
                }),
                dcc.Graph(
                    id='category-pie-chart',
                    style={
                        'height': '410px',
                        'width': '100%'
                    }
                )
            ], style=styles['videoList']),
            
            # 주간 인기 동영상
            html.Div([
                html.H4("주간 인기 동영상", style={
                    'marginBottom': '10px',
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
                        for _, row in weekly_df.iterrows()
                    ], style=styles['videoGrid'])
                ], style={**styles['videoGridContainer'], 'height': '350px'}),
            ], style=styles['videoList'])
        ], style=styles['rightPanel']),
    ], style=styles['mainContent']),
    
    # 하단 섹션
    html.Div([
        # 상단 그리드 (조회수 vs 좋아요 분석 + 워드클라우드)
        html.Div([
            # 조회수 vs 좋아요 분석
            html.Div([
                html.H3("조회수 vs 좋아요 분석", style={
                    'textAlign': 'center', 
                    'marginBottom': '20px',
                    'color': '#ffffff',
                    'fontWeight': '600'
                }),
                dcc.Graph(id='scatter-plot', style={'height': '400px'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': '#1f1f1f',
                'borderRadius': '15px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
                'marginRight': '20px',
                'border': '1px solid rgba(255, 255, 255, 0.1)'
            }),
            
            # 워드클라우드
            html.Div([
                html.H3(id='wordcloud-title', style={
                    'textAlign': 'center', 
                    'marginBottom': '20px',
                    'color': '#ffffff',
                    'fontWeight': '600'
                }),
                html.Div([
                    html.Img(
                        id='word-cloud-img',
                        style={
                            'width': '100%',
                            'height': '400px',
                            'objectFit': 'contain',
                            'border': '1px solid rgba(255, 255, 255, 0.1)',
                            'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
                            'borderRadius': '10px',
                            'backgroundColor': '#272727'
                        }
                    )
                ], style={'textAlign': 'center'})
            ], style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': '#1f1f1f',
                'borderRadius': '15px',
                'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
                'border': '1px solid rgba(255, 255, 255, 0.1)'
            })
        ], style={
            'display': 'flex',
            'marginBottom': '30px',
            'gap': '20px',
            'maxWidth': '1600px',
            'margin': '0 auto'
        })
    ], style={
        'padding': '30px',
        'backgroundColor': '#0f0f0f',
        'borderRadius': '15px',
        'marginTop': '15px'
    }),
    html.Div(id='dummy-output', style={'display': 'none'}),
    html.Div(id='dummy-output-2', style={'display': 'none'})
], style=styles['container'])

# 새탭 열기
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

# 드롭다운 변경 시 페이지 초기화를 위한 콜백
@app.callback(
    Output('current-page', 'data'),
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('prev-page', 'n_clicks'),
     Input('next-page', 'n_clicks')],
    [State('current-page', 'data'),
     State('rank-table', 'data'),
     State('total-pages', 'data')],
    prevent_initial_call=True
)
def update_pagination(country, category, prev_clicks, next_clicks, current_page, data, total_pages):
    triggered_id = ctx.triggered_id
    
    # 드롭다운이 변경된 경우
    if triggered_id in ['country-dropdown', 'category-dropdown']:
        return 0  # 1페이지(인덱스 0)로 초기화
    
    # 페이지 이동 버튼이 클릭된 경우
    if not data:
        return 0
        
    if triggered_id == 'prev-page' and current_page > 0:
        current_page -= 1
    elif triggered_id == 'next-page' and current_page < total_pages - 1:
        current_page += 1
    
    return current_page

current_filtered_df = None
current_filter_key = None
# 테이블 업데이트 콜백
@app.callback(
    [Output('rank-table', 'data'),
     Output('scatter-plot', 'figure'),
     Output('table-title', 'children'),
     Output('category-dropdown', 'value'),
     Output('rank-table', 'active_cell'),
     Output('page-info', 'children'),
     Output('total-pages', 'data')],
    [Input('country-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('rank-table', 'active_cell'),
     Input('current-page', 'data')]
)
def update_table_and_graph(selected_country, selected_category, active_cell, page_current):
    global current_filtered_df, current_filter_key
    
    # 현재 필터 키 생성
    filter_key = f"{selected_country}_{selected_category}"
    
    # 필터가 변경되었거나 페이지가 변경된 경우 active_cell을 None으로 설정
    triggered_id = ctx.triggered_id
    if triggered_id in ['country-dropdown', 'category-dropdown'] or triggered_id == 'current-page':
        active_cell = None
    
    # 필터가 변경된 경우에만 데이터 재계산
    if current_filter_key != filter_key:
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
            if selected_country != '전체':
                filtered_df = filtered_df[filtered_df['country_name'] == selected_country]
        elif category != 'all':
            filtered_df = df[df['category'] == category]
            if selected_country != '전체':
                filtered_df = filtered_df[filtered_df['country_name'] == selected_country]
        
        # 순위 계산
        filtered_df = filtered_df.sort_values('views', ascending=False)
        filtered_df['rank'] = range(1, len(filtered_df) + 1)
        
        # video_id 추가
        filtered_df['video_id'] = filtered_df['url'].apply(lambda x: x.split('v=')[-1])
        
        # 전역 변수 업데이트
        current_filtered_df = filtered_df
        current_filter_key = filter_key
    else:
        filtered_df = current_filtered_df
    
    # 페이지 정보 계산
    page_size = 10
    total_pages = (len(filtered_df) + page_size - 1) // page_size
    
    # 테이블 데이터 준비 (페이지네이션 적용)
    start_idx = page_current * page_size
    end_idx = start_idx + page_size
    table_data = filtered_df[['rank', 'title', 'channel', 'views', 'likes', 'category', 'video_id']].iloc[start_idx:end_idx].to_dict('records')
    
    # 페이지 정보 업데이트
    current_page_display = page_current + 1
    page_info = f'{current_page_display} 페이지 / {total_pages} 페이지'
    
    # 테이블 제목 설정
    category_text = category_names[selected_category]
    if category_text == '전체':
        category_text = ''
    table_title = f"{selected_country} {category_text} 인기 동영상 순위"
    
    # 산점도 생성
    fig = px.scatter(
        filtered_df.head(50),
        x='views',
        y='likes',
        color='category',
        hover_data=['title', 'channel'],
        log_x=True,
        log_y=True,
        labels={
            'views': '조회수',
            'likes': '좋아요 수',
            'category': '카테고리'
        }
    )
    
    # 차트 스타일링
    fig.update_layout(
        plot_bgcolor='#1f1f1f',
        paper_bgcolor='#1f1f1f',
        font=dict(color='#ffffff'),
        xaxis=dict(
            gridcolor='#272727',
            zerolinecolor='#272727',
            tickfont=dict(color='#ffffff'),
            title='조회수'
        ),
        yaxis=dict(
            gridcolor='#272727',
            zerolinecolor='#272727',
            tickfont=dict(color='#ffffff'),
            title='좋아요 수'
        ),
        legend=dict(
            bgcolor='#1f1f1f',
            bordercolor='#272727',
            borderwidth=1,
            font=dict(color='#ffffff')
        ),
        # title=dict(
        #     text='조회수 vs 좋아요 수',
        #     font=dict(color='#ffffff', size=16),
        #     x=0.5,
        #     y=0.95
        # )
    )
    
    return (table_data, fig, table_title, 
            selected_category, active_cell, page_info, total_pages)

# 유튜버 테이블 자동 순환 콜백
@app.callback(
    Output('youtuber-table', 'data'),
    [Input('interval-component', 'n_intervals')],
    [State('youtuber-table', 'data')]
)
def update_youtuber_table(n_intervals, current_data):
    if not current_data:
        return []
    
    current_rank = int(current_data[0]['rank'])
    next_rank = (current_rank % len(crawled_df)) + 1
    next_data = [row for row in crawled_df.to_dict('records') if int(row['rank']) == next_rank]
    
    if next_data:
        return [{
            'rank': next_data[0]['rank'],
            'channel_name': f"[{next_data[0]['channel_name']}]({next_data[0]['channel_link']})",
            'channel_image': f"[![{next_data[0]['channel_name']}]({next_data[0]['channel_image']})]({next_data[0]['channel_link']})"
        }]
    
    return current_data

# 콜백 함수
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
        names=category_counts.index.map(lambda x: category_names.get(x, x)),  # 카테고리 이름 한글로 변환
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
            y=1.0,
            xanchor='center',
            x=0.5,
            bgcolor='#1f1f1f',
            bordercolor='#272727',
            borderwidth=1,
            font=dict(color='#ffffff', size=10)
        ),
        margin=dict(t=30, b=30, l=30, r=30),
        width=400,
        height=400
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
        if category_display == '전체':
            category_display = ''
        return f"{selected_country} {category_display} 워드클라우드"
    except Exception as e:
        print(f"Error in update_wordcloud_title: {str(e)}")
        return "워드클라우드"

# 채널 클릭 시 새 탭에서 열기 위한 콜백 수정
@app.callback(
    Output('url', 'href'),
    [Input('youtuber-table', 'active_cell')],
    [State('youtuber-table', 'data')]
)
def open_channel_link(active_cell, table_data):
    if active_cell and active_cell['column_id'] == 'channel_name':
        row = active_cell['row']
        
        if row < len(table_data):
            channel_link = table_data[row]['channel_link']
            return channel_link
    return dash.no_update

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
