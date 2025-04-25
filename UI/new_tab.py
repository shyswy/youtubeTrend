import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import urllib.parse
import pandas as pd
import os
import glob
from Library.word_visualization import generate_Comments_WC
import math
import base64
from Library.comments_summarizer import summarize_youtube_comments_by_id

# 현재 스크립트의 디렉토리 경로를 가져옴
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'youtube_data')

# YouTube 스타일의 CSS
youtube_styles = {
    'container': {
        'backgroundColor': '#0f0f0f',
        'color': 'white',
        'minHeight': '100vh',
        'padding': '20px',
        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif"
    },
    'header': {
        'backgroundColor': '#0f0f0f',
        'padding': '15px 20px',
        'borderBottom': '1px solid #303030',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between',
        'position': 'sticky',
        'top': '0',
        'zIndex': '1000',
        'backdropFilter': 'blur(10px)',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.1)'
    },
    'title': {
        'color': 'white',
        'fontSize': '24px',
        'fontWeight': 'bold',
        'margin': '0',
        'textShadow': '0 2px 4px rgba(0,0,0,0.2)'
    },
    'videoContainer': {
        'maxWidth': '1600px',
        'margin': '20px auto',
        'backgroundColor': '#0f0f0f',
        'borderRadius': '12px',
        'overflow': 'hidden',
        'display': 'flex',
        'gap': '20px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
        'height': '500px'
    },
    'videoPlayer': {
        'flex': '1',
        'minWidth': '0',
        'borderRadius': '12px',
        'overflow': 'hidden',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
        'height': '100%'
    },
    'channelInfo': {
        'width': '400px',
        'backgroundColor': '#181818',
        'padding': '20px',
        'borderRadius': '12px',
        'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
        'height': '100%',
        'overflowY': 'auto',
        'paddingBottom': '50px'
    },
    'channelHeader': {
        'display': 'flex',
        'alignItems': 'center',
        'marginBottom': '15px',
        'padding': '10px',
        'backgroundColor': '#272727',
        'borderRadius': '8px'
    },
    'channelLogo': {
        'width': '60px',
        'height': '60px',
        'borderRadius': '50%',
        'marginRight': '15px',
        'boxShadow': '0 2px 10px rgba(0,0,0,0.2)'
    },
    'channelName': {
        'color': 'white',
        'fontSize': '18px',
        'fontWeight': 'bold',
        'marginBottom': '15px',
        'padding': '10px',
        'backgroundColor': '#272727',
        'borderRadius': '8px'
    },
    'videoStats': {
        'color': '#aaaaaa',
        'fontSize': '14px',
        'marginBottom': '10px',
        'display': 'flex',
        'alignItems': 'center',
        'gap': '10px',
        'padding': '10px',
        'backgroundColor': '#272727',
        'borderRadius': '8px',
        'transition': 'all 0.3s ease'
    },
    'videoStats:hover': {
        'backgroundColor': '#303030',
        'transform': 'translateY(-2px)'
    },
    'videoDescription': {
        'color': '#aaaaaa',
        'fontSize': '14px',
        'marginBottom': '10px',
        'lineHeight': '1.5',
        'padding': '15px',
        'backgroundColor': '#272727',
        'borderRadius': '8px',
        'maxHeight': '200px',
        'overflowY': 'auto',
        'scrollbarWidth': 'thin',
        'scrollbarColor': '#3ea6ff #272727'
    },
    'videoTags': {
        'color': '#3ea6ff',
        'fontSize': '14px',
        'display': 'flex',
        'flexWrap': 'wrap',
        'gap': '8px',
        'padding': '10px',
        'backgroundColor': '#272727',
        'borderRadius': '8px',
        'overflowY': 'auto',
        'scrollbarWidth': 'thin',
        'scrollbarColor': '#3ea6ff #272727',
        'marginBottom': '30px'
    },
    'tag': {
        'backgroundColor': '#272727',
        'padding': '6px 12px',
        'borderRadius': '20px',
        'cursor': 'pointer',
        'transition': 'all 0.3s ease',
        'border': '1px solid #3ea6ff',
        'color': '#3ea6ff',
        'textDecoration': 'none',
        'display': 'inline-block',
        'margin': '2px'
    },
    'tag:hover': {
        'backgroundColor': '#3ea6ff',
        'color': 'white',
        'transform': 'translateY(-2px)',
        'boxShadow': '0 2px 10px rgba(62,166,255,0.3)'
    },
    'infoContainer': {
        'display': 'flex',
        'alignItems': 'center',
        'gap': '15px',
        'marginTop': '10px',
        'flexWrap': 'wrap'
    },
    'infoBadge': {
        'backgroundColor': '#272727',
        'color': '#aaaaaa',
        'padding': '8px 16px',
        'borderRadius': '20px',
        'fontSize': '14px',
        'border': '1px solid #303030',
        'transition': 'all 0.3s ease'
    },
    'infoBadge:hover': {
        'backgroundColor': '#303030',
        'transform': 'translateY(-2px)'
    },
    'commentsTable': {
        'maxWidth': '1560px',
        'margin': '20px auto',
        'backgroundColor': '#181818',
        'borderRadius': '12px',
        'padding': '20px',
        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
        'boxShadow': '0 4px 20px rgba(0,0,0,0.2)'
    },
    'pagination': {
        'backgroundColor': '#272727',
        'color': 'white',
        'border': 'none',
        'padding': '8px 16px',
        'margin': '0 4px',
        'borderRadius': '20px',
        'cursor': 'pointer',
        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
        'fontSize': '14px',
        'fontWeight': '500',
        'transition': 'all 0.3s ease'
    },
    'pagination:hover': {
        'backgroundColor': '#3ea6ff',
        'transform': 'translateY(-2px)'
    },
    'paginationActive': {
        'backgroundColor': '#3ea6ff',
        'color': 'white',
        'border': 'none',
        'padding': '8px 16px',
        'margin': '0 4px',
        'borderRadius': '20px',
        'cursor': 'pointer',
        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
        'fontSize': '14px',
        'fontWeight': '500',
        'boxShadow': '0 2px 10px rgba(62,166,255,0.3)'
    }
}

# 게이지 스타일 정의
gauge_styles = {
    'red-gauge': {
        'width': '50%',
        'height': '100px',
        'backgroundColor': '#ff4444',
        'display': 'inline-block',
        'verticalAlign': 'top'
    },
    'blue-gauge': {
        'width': '50%',
        'height': '100px',
        'backgroundColor': '#4444ff',
        'display': 'inline-block',
        'verticalAlign': 'top'
    }
}

# 게이지 컨테이너 스타일
gauge_container_style = {
    'width': '100%',
    'height': '100px',
    'backgroundColor': '#272727',
    'borderRadius': '8px',
    'overflow': 'hidden',
    'marginTop': '10px',
    'boxShadow': '0 2px 10px rgba(0,0,0,0.2)',
    'border': '1px solid #303030',
    'whiteSpace': 'nowrap'  # 추가: 내부 요소들이 줄바꿈되지 않도록
}

# CSS 스타일 추가
app_css = {
    'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td',
    'rule': '''
        font-family: "Roboto", "Noto Sans KR", sans-serif !important;
    '''
}

# 스크롤바 스타일 추가
scrollbar_css = {
    'selector': '::-webkit-scrollbar',
    'rule': '''
        width: 8px;
        height: 8px;
    '''
}

scrollbar_thumb_css = {
    'selector': '::-webkit-scrollbar-thumb',
    'rule': '''
        background-color: #3ea6ff;
        border-radius: 4px;
    '''
}

scrollbar_track_css = {
    'selector': '::-webkit-scrollbar-track',
    'rule': '''
        background-color: #272727;
        border-radius: 4px;
    '''
}

# 레이아웃 정의
video_app = dash.Dash(
    __name__, 
    requests_pathname_prefix='/new_tab/',
    assets_folder='assets',  # assets 폴더 위치 지정
    suppress_callback_exceptions=True
)

video_app.layout = html.Div([
    # 스타일 추가
    dcc.Markdown('''
        <style>
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-thumb {
                background-color: #3ea6ff;
                border-radius: 4px;
            }
            ::-webkit-scrollbar-track {
                background-color: #272727;
                border-radius: 4px;
            }
        </style>
    ''', dangerously_allow_html=True),
    # 헤더
    html.Div([
        html.H1("YouTube", style={'color': 'red', 'fontSize': '24px', 'margin': '0', 'fontWeight': 'bold'}),
        html.Div([
            html.Span(id='country-value', style=youtube_styles['infoBadge']),
            html.Span(id='category-value', style=youtube_styles['infoBadge']),
            html.Span(id='videoId-value', style={'display': 'none'}),
            html.Span(id='country_code', style={'display': 'none'}),
            html.Div(id='video-title', style=youtube_styles['title'])
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '15px', 'flexWrap': 'wrap'})
    ], style=youtube_styles['header']),
    
    # 메인 콘텐츠
    html.Div([
        # 동영상 플레이어
        html.Div([
            html.Iframe(
                id='video-player',
                style={
                    'width': '100%',
                    'height': '100%',
                    'border': 'none',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 20px rgba(0,0,0,0.2)'
                }
            )
        ], style=youtube_styles['videoPlayer']),
        
        # 채널 정보
        html.Div([
            html.Div(id='channel-name', style=youtube_styles['channelName']),
            html.Div([
                html.Div(id='video-views', style=youtube_styles['videoStats']),
                html.Div(id='video-likes', style=youtube_styles['videoStats'])
            ]),
            html.Div(id='video-description', style=youtube_styles['videoDescription']),
            html.Div(id='video-tags', style=youtube_styles['videoTags'])
        ], style=youtube_styles['channelInfo'])
    ], style=youtube_styles['videoContainer']),
    
    # 댓글 테이블
    html.Div([
        # 댓글 요약문 div 추가
        html.Div([
            html.H3("댓글 요약", style={
                'color': 'white',
                'marginBottom': '10px',
                'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                'fontSize': '20px',
                'fontWeight': '600'
            }),
            html.Div([
                html.Div([
                    html.Button("요약 보기", id='show-summary-btn', 
                        style={
                        'backgroundColor': '#3ea6ff',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'borderRadius': '8px',
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'cursor': 'pointer',
                        'marginBottom': '10px',
                        'boxShadow': '0 2px 10px rgba(0,0,0,0.15)',
                        'display': 'block',  # 시작 시 보임
                    }),
                    
                    html.Div(id='summary-textbox', children='', style={
                        'display': 'none',  # 처음에는 안 보임
                        'width': '1480px',
                        'height': '50px',
                        'backgroundColor': '#1e1e1e',
                        'color': '#cccccc',
                        'fontSize': '13px',
                        'padding': '10px',
                        'borderRadius': '10px',
                        'border': '1px solid #444',
                        'overflow': 'auto',
                        'whiteSpace': 'pre-wrap'
                    })
                ]),
                ],id='comments-summary', style={
                'width': '1510px',
                'height': '70px',
                'backgroundColor': '#272727',
                'padding': '20px',
                'borderRadius': '12px',
                'color': '#aaaaaa',
                'fontSize': '14px',
                'lineHeight': '1.6',
                'marginBottom': '30px',
                'border': '1px solid #303030',
                'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
                'overflowY': 'auto',
                'overflowX': 'hidden',
                'scrollbarWidth': 'thin',
                'scrollbarColor': '#3ea6ff #272727'
            })
        ]),

        html.Div([
            # 왼쪽: 댓글 제목과 테이블
            html.Div([
                html.H3("댓글", style={
                    'color': 'white', 
                    'marginBottom': '20px', 
                    'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'textShadow': '0 2px 4px rgba(0,0,0,0.2)'
                }),
                dash.dash_table.DataTable(
                    id='comments-table',
                    columns=[
                        {'name': '작성자', 'id': 'comment_author'},
                        {'name': '댓글', 'id': 'comment_text'},
                        {'name': '좋아요', 'id': 'comment_likes'},
                    ],
                    style_table={
                        'borderRadius': '12px',
                        'border': '1px solid #303030',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
                        'height': '750px',
                        'width': '100%',
                        'tableLayout': 'fixed',  # 테이블 레이아웃을 고정
                        'overflowY': 'auto', 
                    },
                    #fixed_rows={'headers': True},  # 헤더 고정
                    style_cell={
                        'backgroundColor': '#181818',
                        'color': 'white',
                        'textAlign': 'left',
                        'padding': '15px',
                        'border': '1px solid #303030',
                        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                        'fontSize': '14px',
                        'whiteSpace': 'pre-wrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': '0'
                    },
                    style_data={
                        'whiteSpace': 'pre-wrap',
                        'height': 'auto',
                        'lineHeight': '1.5',
                        'border': '1px solid #303030',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis'
                    },
                    style_header={
                        'backgroundColor': '#272727',
                        'fontWeight': '500',
                        'border': '1px solid #303030',
                        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                        'fontSize': '14px',
                        'padding': '15px',
                        'textTransform': 'none',
                        'letterSpacing': 'normal',
                        'position': 'sticky',  # 헤더 고정을 위한 스타일
                        'top': 0,  # 헤더 고정을 위한 스타일
                        'zIndex': 1  # 헤더가 다른 내용 위에 표시되도록 함
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#1a1a1a'
                        },
                        {
                            'if': {'state': 'active'},
                            'backgroundColor': '#272727',
                            'border': '1px solid #3ea6ff'
                        }
                    ],
                    style_as_list_view=True,
                    page_size=10,
                    sort_action='native',
                    filter_action='native',
                    page_action='native',
                    style_cell_conditional=[
                        {'if': {'column_id': 'comment_text'}, 'width': '70%', 'minWidth': '70%', 'maxWidth': '70%'},
                        {'if': {'column_id': 'comment_author'}, 'width': '15%', 'minWidth': '15%', 'maxWidth': '15%'},
                        {'if': {'column_id': 'comment_likes'}, 'width': '15%', 'minWidth': '15%', 'maxWidth': '15%'}
                    ],
                    css=[{
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td',
                        'rule': 'font-family: "Roboto", "Noto Sans KR", sans-serif !important;'
                    }, {
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th',
                        'rule': 'font-family: "Roboto", "Noto Sans KR", sans-serif !important; font-weight: 500 !important;'
                    }, {
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner .dash-spreadsheet-menu',
                        'rule': 'font-family: "Roboto", "Noto Sans KR", sans-serif !important;'
                    }, {
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner .dash-spreadsheet-pagination',
                        'rule': 'font-family: "Roboto", "Noto Sans KR", sans-serif !important; font-size: 14px !important; color: white !important;'
                    }]
                )
            ], style={'width': '62%', 'display': 'flex', 'flexDirection': 'column'}),

            # 오른쪽: 워드클라우드 공간
            html.Div([
                # 여론 온도계 섹션
                html.Div([
                    html.H3("여론 온도계", style={
                        'color': 'white', 
                        'marginBottom': '20px', 
                        'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                        'fontSize': '20px',
                        'fontWeight': '600',
                        'textShadow': '0 2px 4px rgba(0,0,0,0.2)'
                    }),
                    html.Div(
                        id='sentiment-gauge',
                        children=[
                            # 게이지 컨테이너
                            html.Div([
                                # 빨간색 영역
                                html.Div(
                                    id='red-gauge',
                                    style=gauge_styles['red-gauge']
                                ),
                                # 파란색 영역
                                html.Div(
                                    id='blue-gauge',
                                    style=gauge_styles['blue-gauge']
                                ),
                            ], style=gauge_container_style),
                            # 퍼센트 표시 컨테이너
                            html.Div([
                                html.Div(
                                    id='predict_percentage',
                                    children='여론을 맞춰보세요',
                                    style={
                                        'color': '#ffffff',
                                        'display': 'inline-block',
                                        'width': '100%',
                                        'textAlign': 'center',
                                        'marginTop': '10px',
                                        'fontSize': '20px',
                                        'fontWeight': 'bold'
                                    }
                                )
                            ])
                        ],
                        style={
                            'width': '530px',
                            'height': 'auto',
                            'backgroundColor': '#181818',
                            'borderRadius': '12px',
                            'border': '1px solid #303030',
                            'padding': '20px',
                            'boxShadow': '0 4px 20px rgba(0,0,0,0.2)',
                            'marginBottom': '20px'
                        }
                    ),
                ]),
                
                html.H3("댓글 키워드", style={
                    'color': 'white', 
                    'marginBottom': '20px', 
                    'fontFamily': "'Roboto', 'Noto Sans KR', sans-serif",
                    'fontSize': '20px',
                    'fontWeight': '600',
                    'textShadow': '0 2px 4px rgba(0,0,0,0.2)'
                }),
                html.Div([html.Img(
                        id='word-cloud-img',
                        style={
                            'width': '100%',
                            'height': '100%',
                            'objectFit': 'contain',
                            'border': '2px solid #ccc',
                            'boxShadow': '2px 2px 10px rgba(0,0,0,0.1)',
                            'borderRadius': '10px'
                        }
                    )], 
                    id='wordcloud-container',
                    style={
                        'width': '530px',
                        'height': '400px',
                        'backgroundColor': '#181818',
                        'borderRadius': '12px',
                        'border': '1px solid #303030',
                        'padding': '20px',
                        'boxShadow': '0 4px 20px rgba(0,0,0,0.2)'
                    }
                )
            ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'})
    ], style=youtube_styles['commentsTable']),
    
    dcc.Location(id='url', refresh=False),
    dcc.Interval(id='init-callback-trigger', interval=1000, n_intervals=0, max_intervals=1)
], style=youtube_styles['container'])

# URL 파라미터에서 정보를 추출하고 동영상을 표시하는 콜백
@video_app.callback(
    [Output('video-player', 'src'),
     Output('video-title', 'children'),
     Output('country-value', 'children'),
     Output('category-value', 'children'),
     Output('channel-name', 'children'),
     Output('video-views', 'children'),
     Output('video-likes', 'children'),
     Output('video-description', 'children'),
     Output('video-tags', 'children'),
     Output('comments-table', 'data'),
     Output('videoId-value', 'children'),
     Output('country_code', 'children')],
    [Input('url', 'search')]
)
def display_video(search):
    if search:
        # URL 파라미터에서 정보 추출
        params = dict(urllib.parse.parse_qsl(search.lstrip('?')))
        video_id = params.get('video_id')
        country = params.get('country', '전체')
        category = params.get('category', 'all')
        
        # 카테고리 매핑
        category_mapping = {
            'all': 'all',
            'entertainment': 'entertainment',
            'news': 'news',
            'people': 'people_blogs',
            'music': 'music',
            'comedy': 'comedy',
            'sports': 'sports'
        }
        country_mapping = {
            '한국': 'KR',
            '미국': 'US',
            '전체': 'all' 
        }
        # 매핑된 카테고리 값 가져오기
        mapped_category = category_mapping.get(category, 'all')
        country = country_mapping.get(country, 'KR')
        video_title = urllib.parse.unquote(params.get('video_title', ''))

        if video_id:
            # YouTube 임베드 URL 생성
            embed_url = f'https://www.youtube.com/embed/{video_id}'

            try:
                # CSV 파일 경로 생성
                if country != 'all':
                    video_file_path = os.path.join(DATA_DIR, f'{country}_{mapped_category}_video.csv')
                    comments_file_path = os.path.join(DATA_DIR, f'{country}_{mapped_category}_comments.csv')
                    country_code = country  # country_code 초기화
                    print(f"country: {country}, category: {category}, mapped_category: {mapped_category}")  # 디버깅용
                    print(f"video_file_path: {video_file_path}")  # 디버깅용
                else:
                    # 와일드카드 패턴으로 모든 국가의 비디오 파일 찾기
                    if mapped_category == 'all':
                        # 미국과 한국의 all_video.csv 파일을 모두 찾기
                        video_file_paths = []
                        for country_code in ['US', 'KR']:
                            file_path = os.path.join(DATA_DIR, f'{country_code}_all_video.csv')
                            if os.path.exists(file_path):
                                video_file_paths.append(file_path)
                    else:
                        # 미국과 한국의 해당 카테고리 파일을 모두 찾기
                        video_file_paths = []
                        country_code = country
                        file_path = os.path.join(DATA_DIR, f'{country_code}_{mapped_category}_video.csv')
                        if os.path.exists(file_path):
                            video_file_paths.append(file_path)
                    matching_files = None
                    
                    # video_id와 일치하는 파일 찾기
                    for file_path in video_file_paths:
                        try:
                            df = pd.read_csv(file_path)
                            if 'id' in df.columns:
                                matching_rows = df[df['id'] == video_id]
                                if not matching_rows.empty:
                                    matching_files = file_path
                                    country_code = os.path.basename(file_path).split('_')[0]  # 파일명에서 국가 코드 추출
                                    print(f"일치하는 파일 찾음: {matching_files}, country_code: {country_code}")  # 디버깅용
                                    break
                            else:
                                print(f"'id' 컬럼이 없음: {file_path}")  # 디버깅용
                        except Exception as e:
                            print(f"파일 읽기 오류 {file_path}: {str(e)}")
                            continue
                    
                    if not matching_files:
                        return "", f"해당 video_id({video_id})를 찾을 수 없습니다.", country, category, "", "", "", "", "", [], "", ""

                    # 매칭된 파일의 국가 코드 추출 (파일명에서)
                    video_file_path = matching_files
                    comments_file_path = os.path.join(DATA_DIR, f'{country_code}_{mapped_category}_comments.csv')
                
                # 비디오 CSV 파일이 존재하는지 확인
                if not os.path.exists(video_file_path):
                    print(f"비디오 파일이 존재하지 않습니다: {video_file_path}")  # 디버깅용
                    return "", f"파일을 찾을 수 없습니다: {video_file_path}", country, category, "", "", "", "", "", [], "", ""
                    
                # 비디오 CSV 파일 읽기
                video_df = pd.read_csv(video_file_path)
                # video_id와 일치하는 행 찾기
                matching_video = video_df[video_df['id'] == video_id]
                if matching_video.empty:
                    print(f"video_id({video_id})와 일치하는 비디오가 없습니다.")  # 디버깅용
                    return "", f"해당 video_id({video_id})를 찾을 수 없습니다.", country, category, "", "", "", "", "", [], "", ""
                
                # 댓글 CSV 파일이 존재하는지 확인
                if not os.path.exists(comments_file_path):
                    print(f"댓글 파일이 존재하지 않습니다: {comments_file_path}")  # 디버깅용
                    comments_data = []
                else:
                    # 댓글 CSV 파일 읽기
                    comments_df = pd.read_csv(comments_file_path,
                        sep=None,
                        engine='python',
                        encoding='utf-8',
                        on_bad_lines='skip'
                    )
                    
                    print(f"댓글 CSV 컬럼: {comments_df.columns.tolist()}")  # 디버깅용
                    print(f"댓글 데이터 샘플: {comments_df.head()}")  # 디버깅용
                    
                    # video_id와 일치하는 댓글 찾기
                    matching_comments = comments_df[comments_df['video_id'] == video_id]
                    print(f"일치하는 댓글 개수: {len(matching_comments)}")  # 디버깅용
                    print(f"매칭된 댓글 데이터: {matching_comments.head()}")  # 디버깅용
                    
                    if not matching_comments.empty:
                        comments_data = matching_comments[['comment_author', 'comment_text', 'comment_likes']].to_dict('records')
                        print(f"최종 댓글 데이터: {comments_data[:2]}")  # 디버깅용
                    else:
                        comments_data = []
                
                # 값 추출 (에러 처리 추가)
                try:
                    channel_name = matching_video['channelTitle'].iloc[0] if 'channelTitle' in matching_video.columns else "채널 정보 없음"
                    
                    # 조회수 처리 (nan 체크 및 천 단위 콤마)
                    if 'viewCount' in matching_video.columns and pd.notna(matching_video['viewCount'].iloc[0]):
                        views = f"👁️ {int(matching_video['viewCount'].iloc[0]):,}회"
                    else:
                        views = "👁️ 조회수 정보 없음"
                    
                    # 좋아요 처리 (nan 체크 및 천 단위 콤마)
                    if 'likeCount' in matching_video.columns and pd.notna(matching_video['likeCount'].iloc[0]):
                        likes = f"👍 {int(matching_video['likeCount'].iloc[0]):,}개"
                    else:
                        likes = "👍 좋아요 정보 없음"
                    
                    # 설명 처리 (nan 체크)
                    description = matching_video['description'].iloc[0] if pd.notna(matching_video['description'].iloc[0]) else "설명 없음"
                    
                    # 태그 처리 (nan 체크 및 # 추가)
                    if 'tags' in matching_video.columns and pd.notna(matching_video['tags'].iloc[0]):
                        # 태그 문자열을 리스트로 변환
                        tag_str = matching_video['tags'].iloc[0]
                        # 대괄호와 공백 제거 후 리스트로 변환
                        tag_str = tag_str.replace('[', '').replace(']', '').strip()
                        tag_list = [tag.strip() for tag in tag_str.split(',') if tag.strip()]
                        
                        tags = []
                        for tag in tag_list:
                            # 태그를 클릭 가능한 링크로 변환
                            tag_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(tag)}"
                            tags.append(html.A(f"#{tag}", href=tag_url, target="_blank", style=youtube_styles['tag']))
                    else:
                        tags = []
                except Exception as e:
                    print(f"데이터 추출 중 오류 발생: {str(e)}")  # 디버깅용
                    channel_name = "채널 정보 없음"
                    views = "👁️ 조회수 정보 없음"
                    likes = "👍 좋아요 정보 없음"
                    description = "설명 없음"
                    tags = []
                
                return embed_url, video_title, country, category, "채널: "+channel_name, views, likes, description, tags, comments_data, video_id, country_code
                
            except Exception as e:
                print(f"오류 발생: {str(e)}")  # 디버깅용
                return "", f"오류 발생: {str(e)}", country, category, "", "", "", "", "", [], "", ""
    
    return "", "동영상을 찾을 수 없습니다.", "", "", "", "", "", "", "", [], "", ""

# 워드 클라우드 생성용 콜백
@video_app.callback(
    Output('word-cloud-img', 'src'),
    [Input('init-callback-trigger', 'n_intervals')],
    [State('videoId-value', 'children'),
     State('country_code', 'children'),
     State('category-value', 'children')]
)
def update_word_cloud(n, video_id, selected_country , selected_category):
    print("Update Word Cloud ", video_id, selected_country , selected_category)
    try:
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
        
        print(f"Generating word cloud for country: {selected_country}, category: {category}")
        
        # 워드클라우드 이미지 생성
        img_base64 = generate_Comments_WC(video_id, selected_country, category)
        if img_base64 is None:
            print("Word cloud generation returned None")
            return None
        
        print("Word cloud generated successfully")
        return img_base64  # 이미 base64 URL이 포함되어 있으므로 그대로 반환
    except Exception as e:
        print(f"Error in update_word_cloud: {str(e)}")
        return None 









#버튼 블라인드용 콜백
@video_app.callback(
    Output('show-summary-btn', 'style'),
    Input('show-summary-btn', 'n_clicks'),
    prevent_initial_call=True
)
def hide_button_immediately(n_clicks):
    return {'display': 'none'}

# GPT 요약용 콜백
@video_app.callback(
    [Output('summary-textbox', 'children'),
     Output('summary-textbox', 'style')],
    Input('show-summary-btn', 'n_clicks'),
    [State('videoId-value', 'children'),
     State('country_code', 'children'),
     State('category-value', 'children')],
    prevent_initial_call=True
)
def show_summary(n_clicks, vidoe_id, country, category):
    print("클릭 입력 감지 확인")
    
    div_style = {
        'display': 'block',
        'width': '1480px',
        'height': '50px',
        'backgroundColor': '#1e1e1e',
        'color': '#cccccc',
        'fontSize': '13px',
        'padding': '10px',
        'borderRadius': '10px',
        'border': '1px solid #444',
        'overflow': 'auto',
        'whiteSpace': 'pre-wrap'
    }

    return summarize_youtube_comments_by_id(vidoe_id, country, category)[0], div_style



if __name__ == '__main__':
    video_app.run(debug=True)