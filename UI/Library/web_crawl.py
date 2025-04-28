# import requests
# from bs4 import BeautifulSoup

# def get_youtuber_Ranking(category = 'all', country = 'korea', ranking = "인기",  duration = "일간"):
#     # 카테고리 맵핑
#     CATEGORY_TYPE = {
#         'all': 'all',
#         'entertainment': 'entertainment',
#         'news': 'news',
#         'people_blogs': 'vlog',
#         'music': 'music',
#         'comedy': 'comedy',
#         'sports': 'sports'
#     }
#     # 순위 방식 맵핑
#     RANKING_TYPE = {
#         "인기": "popular",
#         "구독자": "subscribed",
#         "슈퍼챗": "superchatted",
#         "라이브 시청자": "watched",
#         "조회수": "viewed",
#         "구독자 급상승": "growth",
#         "구독자 급하락": "decline"
#     }
#     # 국가 맵핑
#     COUNTRY_TYPE = {
#         "all": "worldwide",
#         "korea": "south-korea",
#         "usa": "united-states",
#         }
#     # 집계 기간 맵핑
#     DURACTION_TYPE = {
#         "일간": "daily",
#         "주간": "weekly",
#         "월간": "monthly",
#         "연말": "yearend",
#         "연간": "yearly",
#         "전체": "total"
#     }
#     # 기본값 설정
#     category_key = CATEGORY_TYPE.get(category, next(iter(CATEGORY_TYPE)))
#     ranking_key = RANKING_TYPE.get(ranking, next(iter(RANKING_TYPE)))
#     country_key = COUNTRY_TYPE.get(country, next(iter(COUNTRY_TYPE)))
#     duration_key = DURACTION_TYPE.get(duration, next(iter(DURACTION_TYPE)))
#     url = f'https://playboard.co/youtube-ranking/most-{ranking_key}-{category_key}-channels-in-{country_key}-{duration_key}'
#     return get_ranking_data(url)


# def get_ranking_data(url):
#     print(url)

#     def fetch_soup():
#         response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#         return BeautifulSoup(response.text, 'html.parser')

#     soup = fetch_soup()
#     chart_items = soup.find_all(class_='chart__row')
#     result = []

#     for idx, row in enumerate(chart_items):
#         try:
#             # 광고는 제외
#             if 'chart__row--ad' in row.get('class', []):
#                 continue

#             def parse_row(row):
#                 # 1. 순위
#                 rank_div = row.find('td', class_='rank')
#                 rank = rank_div.find('div', class_='current').get_text(strip=True) if rank_div else None

#                 # 2. 채널 링크
#                 logo_td = row.find('td', class_='logo')
#                 a_tag = logo_td.find('a') if logo_td else None
#                 channel_link = a_tag['href'] if a_tag and a_tag.has_attr('href') else None

#                 # 3. 채널 이름
#                 name_td = row.find('td', class_='name')
#                 name_tag = name_td.find('h3') if name_td else None
#                 channel_name = name_tag.get_text(strip=True) if name_tag else None

#                 # 4. 채널 이미지
#                 img_tag = logo_td.find('img') if logo_td else None
#                 image_url = img_tag.get('data-src') or img_tag.get('src') if img_tag else None

#                 # 5. 대표 영상
#                 video_section = row.find('td', class_='videos')
#                 video_item = video_section.find('a') if video_section else None
#                 video_link = video_item['href'] if video_item and video_item.has_attr('href') else None

#                 thumb_div = video_item.find('div', class_='thumb') if video_item else None
#                 thumbnail_url = thumb_div.get('data-background-image') if thumb_div else None
#                 if thumbnail_url and thumbnail_url.startswith('//'):
#                     thumbnail_url = 'https:' + thumbnail_url

#                 return {
#                     'rank': rank,
#                     'channel_name': channel_name,
#                     'channel_link': f"https://youtube.com{channel_link}" if channel_link else None,
#                     'channel_image': image_url,
#                     'video_link': f"https://youtube.com{video_link}" if video_link else None,
#                     'thumbnail_url': thumbnail_url
#                 }

#             # row 파싱
#             item = parse_row(row)

#             # 만약 중요한 항목들이 None이면 → 한 번 더 시도
#             if not item['channel_name'] or not item['channel_link']:
#                 print(f"[재시도] {idx}번 row의 데이터가 누락되어 재요청합니다.")
#                 soup_retry = fetch_soup()
#                 chart_items_retry = soup_retry.find_all(class_='chart__row')
#                 if idx < len(chart_items_retry):
#                     retry_row = chart_items_retry[idx]
#                     if 'chart__row--ad' not in retry_row.get('class', []):
#                         item = parse_row(retry_row)

#             result.append(item)

#         except Exception as e:
#             print(f"[예외 발생] row {idx}: {e}")
#             result.append({
#                 'rank': None,
#                 'channel_name': None,
#                 'channel_link': None,
#                 'channel_image': None,
#                 'video_link': None,
#                 'thumbnail_url': None
#             })

#     return result

# if __name__ == '__main__':    
#     import math
#     import time
#     start = time.time()
#     math.factorial(100000)
#     ranking_dict = get_youtuber_Ranking('music', 'korea')
#     end = time.time()
#     print("실행 시간 :" + f"{end - start:.5f} sec")
#     for contents in ranking_dict:
#         print(f"{contents} \n")

import pandas as pd
import os

def get_youtuber_Ranking(country, category):
    print("크롤링 체크", country, category)
    COUNTRY_TYPE = {
        "전체": "US",
        "한국": "KR",
        "미국": "US",
    }

    # 'all'이면 US 데이터를 기반으로 처리 (예시)
    csv_country = COUNTRY_TYPE[country]
    
    if category == 'lge':
        csv_category = 'all'
    else:
        csv_category = category

    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_dir = os.path.join(current_dir, "youtube_data")

    csv_path = os.path.join(csv_dir, f"{csv_country}_{category}_youtuber.csv")
    df = pd.read_csv(csv_path)

    # country가 'all'인 경우 전체 데이터를 반환하고,
    # 다른 특정 국가가 지정된 경우 country 컬럼이 있다면 필터링 (필요 시)
    # if country.lower() != 'all' and 'country' in df.columns:
    #     df = df[df['country'] == country]

    results = []

    for _, row in df.iterrows():
        item = {
            'rank': row['rank'],
            'channel_name': row['channelName'],
            'channel_link': row['channelLink'],
            'channel_image': row['channelImage'],
            'video_link': row['videoLink'],
            'thumbnail_url': row['thumbnailUrl']
        }
        results.append(item)

    return results


# 사용 예시
if __name__ == '__main__':    
    ranking_dict = get_youtuber_Ranking('KR', 'all')
    for contents in ranking_dict[:5]:  # 예시로 상위 5개만 출력
        print(contents)
