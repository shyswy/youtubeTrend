# YouTube 트렌드 분석 프로젝트

이 프로젝트는 YouTube의 인기 동영상과 유튜버 순위를 분석하고 시각화하는 웹 애플리케이션입니다.

## 프로젝트 구조

```
youtubeTrend/
├── UI/
│   └── collect.py      # YouTube API를 사용한 데이터 수집
├── youtube_rank.py     # Dash를 사용한 웹 애플리케이션
└── web_crawl.py        # 웹 크롤링 모듈
```

## 데이터 구조

### YouTube 동영상 데이터
| 필드명 | 설명 | 데이터 타입 |
|--------|------|------------|
| video_id | 동영상 고유 ID | String |
| title | 동영상 제목 | String |
| channel | 채널명 | String |
| category_id | 카테고리 ID | String |
| category | 카테고리명 | String |
| views | 조회수 | Integer |
| likes | 좋아요 수 | Integer |
| description | 동영상 설명 | String |
| tags | 태그 | String |
| url | 동영상 URL | String |
| published_at | 업로드 날짜 | DateTime |
| comment_count | 댓글 수 | Integer |
| country | 국가 코드 | String |

### 카테고리 매핑
| 카테고리 ID | 카테고리명 |
|------------|------------|
| 0 | 전체 |
| 24 | 엔터테인먼트 |
| 25 | 뉴스 |
| 22 | People & Blogs |
| 10 | 음악 |
| 23 | 코미디 |
| 17 | 스포츠 |

### 국가 코드
| 국가명 | 국가 코드 |
|--------|------------|
| 한국 | KR |
| 미국 | US |

## 주요 기능

1. **데이터 수집**
   - YouTube API를 통한 인기 동영상 데이터 수집
   - 웹 크롤링을 통한 유튜버 순위 데이터 수집

2. **데이터 시각화**
   - 국가별, 카테고리별 동영상 순위 표시
   - 조회수 vs 좋아요 분석 그래프
   - 카테고리별 동영상 수 파이 차트
   - 실시간 인기 유튜버 순위 표시

3. **인터랙티브 기능**
   - 국가 및 카테고리 필터링
   - 동영상 미리보기
   - 자동 순환되는 유튜버 순위

## 설치 및 실행 방법

1. 필요한 패키지 설치:
```bash
pip install dash pandas plotly google-api-python-client
```

2. YouTube API 키 설정:
- `collect.py` 파일에서 API_KEY 변수를 본인의 YouTube API 키로 변경

3. 애플리케이션 실행:
```bash
python youtube_rank.py
```

## 기술 스택

- Python
- Dash (웹 프레임워크)
- YouTube Data API
- Pandas (데이터 처리)
- Plotly (시각화)
- Web Crawling

## 주의사항

- YouTube API 키는 개인적으로 발급받아 사용해야 합니다.
- API 사용량 제한에 주의해야 합니다.
- 웹 크롤링 시 대상 사이트의 robots.txt를 준수해야 합니다. 
