import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import urllib.parse
import pandas as pd
import os

# 새 탭용 Dash 앱 생성
video_app = dash.Dash(__name__, requests_pathname_prefix='/new_tab/')

# YouTube 스타일의 CSS
youtube_styles = {
    'container': {
        'backgroundColor': '#0f0f0f',
        'color': 'white',
        'minHeight': '100vh',
        'padding': '20px'
    },
    'header': {
        'backgroundColor': '#0f0f0f',
        'padding': '15px 20px',
        'borderBottom': '1px solid #303030',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'space-between'
    },
    'title': {
        'color': 'white',
        'fontSize': '24px',
        'fontWeight': 'bold',
        'margin': '0'
    },
    'videoContainer': {
        'maxWidth': '1200px',
        'margin': '20px auto',
        'backgroundColor': '#0f0f0f',
        'borderRadius': '12px',
        'overflow': 'hidden',
        'display': 'flex',
        'gap': '20px'
    },
    'videoPlayer': {
        'flex': '1',
        'minWidth': '0'
    },
    'channelInfo': {
        'width': '300px',
        'backgroundColor': '#181818',
        'padding': '20px',
        'borderRadius': '12px'
    },
    'channelHeader': {
        'display': 'flex',
        'alignItems': 'center',
        'marginBottom': '15px'
    },
    'channelLogo': {
        'width': '60px',
        'height': '60px',
        'borderRadius': '50%',
        'marginRight': '15px'
    },
    'channelName': {
        'color': 'white',
        'fontSize': '18px',
        'fontWeight': 'bold',
        'marginBottom': '15px'
    },
    'videoStats': {
        'color': '#aaaaaa',
        'fontSize': '14px',
        'marginBottom': '10px',
        'display': 'flex',
        'alignItems': 'center',
        'gap': '10px'
    },
    'videoDescription': {
        'color': '#aaaaaa',
        'fontSize': '14px',
        'marginBottom': '10px',
        'lineHeight': '1.5'
    },
    'videoTags': {
        'color': '#3ea6ff',
        'fontSize': '14px',
        'display': 'flex',
        'flexWrap': 'wrap',
        'gap': '8px'
    },
    'tag': {
        'backgroundColor': '#272727',
        'padding': '4px 8px',
        'borderRadius': '4px',
        'cursor': 'pointer'
    },
    'infoContainer': {
        'display': 'flex',
        'alignItems': 'center',
        'gap': '15px',
        'marginTop': '10px'
    },
    'infoBadge': {
        'backgroundColor': '#272727',
        'color': '#aaaaaa',
        'padding': '5px 10px',
        'borderRadius': '15px',
        'fontSize': '14px'
    },
    'commentsTable': {
        'maxWidth': '1200px',
        'margin': '20px auto',
        'backgroundColor': '#181818',
        'borderRadius': '12px',
        'padding': '20px',
        'fontFamily': 'Roboto, Arial, sans-serif'
    },
    'pagination': {
        'backgroundColor': '#272727',
        'color': 'white',
        'border': 'none',
        'padding': '8px 16px',
        'margin': '0 4px',
        'borderRadius': '4px',
        'cursor': 'pointer',
        'fontFamily': 'Roboto, Arial, sans-serif',
        'fontSize': '14px',
        'fontWeight': '500'
    },
    'paginationActive': {
        'backgroundColor': '#3ea6ff',
        'color': 'white',
        'border': 'none',
        'padding': '8px 16px',
        'margin': '0 4px',
        'borderRadius': '4px',
        'cursor': 'pointer',
        'fontFamily': 'Roboto, Arial, sans-serif',
        'fontSize': '14px',
        'fontWeight': '500'
    }
}

# 레이아웃 정의
video_app.layout = html.Div([
    # 헤더
    html.Div([
        html.H1("YouTube", style={'color': 'red', 'fontSize': '24px', 'margin': '0'}),
        html.Div([
            html.Span(id='country-value', style=youtube_styles['infoBadge']),
            html.Span(id='category-value', style=youtube_styles['infoBadge']),
            html.Div(id='video-title', style=youtube_styles['title'])
        ], style={'display': 'flex', 'alignItems': 'center', 'gap': '15px'})
    ], style=youtube_styles['header']),
    
    # 메인 콘텐츠
    html.Div([
        # 동영상 플레이어
        html.Div([
            html.Iframe(
                id='video-player',
                style={
                    'width': '100%',
                    'height': '450px',
                    'border': 'none',
                    'borderRadius': '12px'
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
        html.H3("댓글", style={'color': 'white', 'marginBottom': '20px', 'fontFamily': 'Roboto, Arial, sans-serif'}),
        html.Div([
            # 왼쪽: 댓글 테이블
            html.Div([
                dash.dash_table.DataTable(
                    id='comments-table',
                    columns=[
                        {'name': '작성자', 'id': 'comment_author'},
                        {'name': '댓글', 'id': 'comment_text'},
                        {'name': '좋아요', 'id': 'comment_likes'},
                    ],
                    style_table={
                        'overflowX': 'auto',
                        'borderRadius': '8px',
                        'border': '1px solid #303030'
                    },
                    style_cell={
                        'backgroundColor': '#181818',
                        'color': 'white',
                        'textAlign': 'left',
                        'padding': '12px',
                        'border': '1px solid #303030',
                        'fontFamily': 'Roboto, Arial, sans-serif',
                        'fontSize': '14px'
                    },
                    style_header={
                        'backgroundColor': '#272727',
                        'fontWeight': '500',
                        'border': '1px solid #303030',
                        'fontFamily': 'Roboto, Arial, sans-serif',
                        'fontSize': '14px',
                        'padding': '12px',
                        'textTransform': 'none',
                        'letterSpacing': 'normal'
                    },
                    style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '1.5',
                        'border': '1px solid #303030'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#1a1a1a'
                        }
                    ],
                    style_as_list_view=True,
                    page_size=10,
                    sort_action='native',
                    filter_action='native',
                    page_action='native',
                    style_cell_conditional=[
                        {'if': {'column_id': 'text'}, 'width': '60%'},
                        {'if': {'column_id': 'author'}, 'width': '20%'},
                        {'if': {'column_id': 'likeCount'}, 'width': '20%'}
                    ],
                    css=[{
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner td',
                        'rule': 'font-family: Roboto, Arial, sans-serif !important;'
                    }, {
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner th',
                        'rule': 'font-family: Roboto, Arial, sans-serif !important; font-weight: 500 !important;'
                    }, {
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner .dash-spreadsheet-menu',
                        'rule': 'font-family: Roboto, Arial, sans-serif !important;'
                    }, {
                        'selector': '.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner .dash-spreadsheet-pagination',
                        'rule': 'font-family: Roboto, Arial, sans-serif !important; font-size: 14px !important; color: white !important;'
                    }]
                )
            ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'}),

            # 오른쪽: 워드클라우드 공간
            html.Div([
                html.H3("댓글 키워드", style={'color': 'white', 'marginBottom': '20px', 'fontFamily': 'Roboto, Arial, sans-serif'}),
                html.Div(
                    id='wordcloud-container',
                    style={
                        'height': '400px',
                        'backgroundColor': '#181818',
                        'borderRadius': '8px',
                        'border': '1px solid #303030',
                        'padding': '20px'
                    }
                )
            ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'})
    ], style=youtube_styles['commentsTable']),
    
    dcc.Location(id='url', refresh=False)
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
     Output('comments-table', 'data')],
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
        
        # 매핑된 카테고리 값 가져오기
        mapped_category = category_mapping.get(category, 'all')
        
        video_title = urllib.parse.unquote(params.get('video_title', ''))

        if video_id:
            # YouTube 임베드 URL 생성
            embed_url = f'https://www.youtube.com/embed/{video_id}'

            try:
                # CSV 파일 경로 생성
                parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                video_file_path = os.path.join(parent_dir, 'csvCollection', f'KR_{mapped_category}_video.csv')
                comments_file_path = os.path.join(parent_dir, 'csvCollection', f'KR_{mapped_category}_comments.csv')
                
                print(f"비디오 파일 경로: {video_file_path}")  # 디버깅용
                print(f"댓글 파일 경로: {comments_file_path}")  # 디버깅용
                
                # 비디오 CSV 파일이 존재하는지 확인
                if not os.path.exists(video_file_path):
                    print(f"비디오 파일이 존재하지 않습니다: {video_file_path}")  # 디버깅용
                    return "", f"파일을 찾을 수 없습니다: {video_file_path}", country, category, "", "", "", "", "", []
                    
                # 비디오 CSV 파일 읽기
                video_df = pd.read_csv(video_file_path)
                print(f"비디오 CSV 컬럼: {video_df.columns.tolist()}")  # 디버깅용
                
                # video_id와 일치하는 행 찾기
                matching_video = video_df[video_df['id'] == video_id]
                print(f"일치하는 비디오 행 개수: {len(matching_video)}")  # 디버깅용
                if matching_video.empty:
                    print(f"video_id({video_id})와 일치하는 비디오가 없습니다.")  # 디버깅용
                    return "", f"해당 video_id({video_id})를 찾을 수 없습니다.", country, category, "", "", "", "", "", []
                
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
                    views = f"👁️ {matching_video['viewCount'].iloc[0]}회" if 'viewCount' in matching_video.columns else "👁️ 조회수 정보 없음"
                    likes = f"👍 {matching_video['likeCount'].iloc[0]}개" if 'likeCount' in matching_video.columns else "👍 좋아요 정보 없음"
                    description = matching_video['description'].iloc[0]
                    tags = matching_video['tags'].iloc[0].split('|') if 'tags' in matching_video.columns and pd.notna(matching_video['tags'].iloc[0]) else []
                except Exception as e:
                    print(f"데이터 추출 중 오류 발생: {str(e)}")  # 디버깅용
                    channel_name = "채널 정보 없음"
                    views = "👁️ 조회수 정보 없음"
                    likes = "👍 좋아요 정보 없음"
                    description = "설명 없음"
                    tags = []
                
                
                # 태그 생성
                tag_elements = [html.Span(tag, style=youtube_styles['tag']) for tag in tags]
                
                return embed_url, video_title, country, category, "채널: "+channel_name, views, likes, description, tag_elements, comments_data
                
            except Exception as e:
                return "", f"오류 발생: {str(e)}", country, category, "", "", "", "", "", []
    
    return "", "동영상을 찾을 수 없습니다.", "", "", "", "", "", "", "", []

if __name__ == '__main__':
    video_app.run(debug=True)