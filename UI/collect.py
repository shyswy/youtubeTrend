import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

# YouTube API 키 설정
API_KEY = ""  # 실제 API 키로 교체 필요

# YouTube API 클라이언트 생성
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_popular_videos(country_code, category_id='0'):
    """
    특정 국가와 카테고리의 인기 동영상을 가져옵니다.
    country_code: 국가 코드 (예: 'KR' - 한국, 'US' - 미국)
    category_id: 카테고리 ID ('0' - 전체, '24' - 엔터테인먼트, '25' - 뉴스)
    """
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=country_code,
            videoCategoryId=category_id,
            maxResults=50
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'category_id': category_id,
                'category': {
                    '0': '전체',
                    '24': '엔터테인먼트',
                    '25': '뉴스',
                    '22': 'People & Blogs',
                    '10': '음악',
                    '23': '코미디',
                    '19': '여행 & 스타일',
                    '17': '스포츠'
                }.get(category_id, '기타'),
                'views': int(item['statistics']['viewCount']),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'description': item['snippet'].get('description', ''),
                'tags': ','.join(item['snippet'].get('tags', [])),
                'url': f"https://www.youtube.com/watch?v={item['id']}",
                'published_at': item['snippet']['publishedAt'],
                'comment_count': int(item['statistics'].get('commentCount', 0)),
                'country': country_code
            }
            videos.append(video)
        
        return pd.DataFrame(videos)
    
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None

def get_weekly_popular_videos(country_code):
    """
    특정 국가의 주간 인기 동영상을 가져옵니다.
    country_code: 국가 코드 (예: 'KR' - 한국, 'US' - 미국)
    """
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            chart="mostPopular",
            regionCode=country_code,
            maxResults=50
        )
        response = request.execute()
        
        videos = []
        for item in response['items']:
            video = {
                'video_id': item['id'],
                'title': item['snippet']['title'],
                'channel': item['snippet']['channelTitle'],
                'category': item['snippet'].get('categoryId', '0'),
                'views': int(item['statistics']['viewCount']),
                'likes': int(item['statistics'].get('likeCount', 0)),
                'description': item['snippet'].get('description', ''),
                'url': f"https://www.youtube.com/watch?v={item['id']}",
                'published_at': item['snippet']['publishedAt'],
                'country': country_code
            }
            videos.append(video)
        
        return pd.DataFrame(videos)
    
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None

# 카테고리 매핑
categories = {
    'all': '0',
    'entertainment': '24',
    'news': '25',
    'people_blogs': '22',
    'music': '10',
    'comedy': '23',
    'travel_style': '19',
    'sports': '17'
}

# 국가 코드 매핑
countries = {
    'korea': 'KR',
    'usa': 'US'
}

# 결과를 저장할 디렉토리 생성
output_dir = 'youtube_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 결과를 저장할 딕셔너리
results = {}

# 각 국가와 카테고리별로 데이터 수집
for country_name, country_code in countries.items():
    country_results = {}
    for category_name, category_id in categories.items():
        print(f"Fetching {category_name} videos for {country_name}...")
        df = get_popular_videos(country_code, category_id)
        if df is not None:
            country_results[category_name] = df
            # CSV 파일로 저장
            filename = f"{output_dir}/{country_name}_{category_name}_videos.csv"
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Saved to {filename}")
    
    # 주간 인기 동영상 데이터 수집
    print(f"Fetching weekly popular videos for {country_name}...")
    weekly_df = get_weekly_popular_videos(country_code)
    if weekly_df is not None:
        weekly_filename = f"{output_dir}/{country_name}_weekly_videos.csv"
        weekly_df.to_csv(weekly_filename, index=False, encoding='utf-8-sig')
        print(f"Saved weekly videos to {weekly_filename}")
    
    results[country_name] = country_results

# 결과 출력
for country, categories in results.items():
    print(f"\n=== {country.upper()} ===")
    for category, df in categories.items():
        print(f"\n{category.upper()} Category:")
        print(f"Total videos: {len(df)}")
        print("\nTop 5 videos:")
        print(df[['title', 'views', 'likes', 'channel']].head())