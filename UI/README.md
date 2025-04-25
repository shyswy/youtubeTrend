# YouTube 트렌드 분석 프로젝트

이 프로젝트는 YouTube의 인기 동영상과 유튜버 순위를 분석하고 시각화하는 웹 애플리케이션입니다.

## 프로젝트 구조

```
youtubeTrend/
├── UI/
│   ├── main.py         # Dash를 사용한 메인 웹 애플리케이션
│   ├── collect.py      # YouTube API를 사용한 데이터 수집
│   └── new_tab.py      # 동영상 상세 정보를 보여주는 새 탭
├── Library/
│   ├── web_crawl.py    # 웹 크롤링 모듈
│   └── word_visualization.py  # 워드클라우드 생성 모듈
└── youtube_data/       # 수집된 데이터 저장 디렉토리
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
   - **인기 동영상 순위 테이블**
     - 국가별, 카테고리별 필터링
     - 페이지네이션 지원
     - 클릭 시 동영상 새 탭으로 열기
   
   - **이중 축 콤보 차트 (Dual Axis Combo Chart)**
     - 카테고리별 평균 조회수 (막대 그래프)
     - 카테고리별 평균 좋아요 (선 그래프)
     - 두 개의 Y축을 사용한 데이터 비교
   
   - **산점도 (Scatter Plot)**
     - 조회수 vs 좋아요 상관관계 분석
     - 로그 스케일 적용
     - 카테고리별 색상 구분
   
   - **파이 차트 (Pie Chart)**
     - 카테고리별 동영상 수 비율
     - 퍼센트와 개수 표시
   
   - **시간대별 조회수 분석 그래프**
     - 시간대별 평균 조회수 추세
     - 선 그래프와 마커 사용
   
   - **워드클라우드 (Word Cloud)**
     - 동영상 제목 키워드 시각화
     - 빈도수 기반 크기 및 색상 차별화
   
   - **실시간 인기 유튜버 순위**
     - 자동 순환되는 유튜버 정보
     - 채널 이미지 및 링크 포함

3. **인터랙티브 기능**
   - 국가 및 카테고리 필터링
   - 동영상 미리보기
   - 자동 순환되는 유튜버 순위
   - 모든 차트의 실시간 업데이트

## 시각화 특징

1. **일관된 디자인 테마**
   - 어두운 테마 (Dark Theme) 적용
   - 일관된 색상 팔레트 사용
   - 반응형 디자인

2. **상호작용성**
   - 모든 차트에 호버 효과 적용
   - 필터링 기능 (국가, 카테고리)
   - 실시간 데이터 업데이트

3. **데이터 분석 관점**
   - 정량적 분석 (조회수, 좋아요)
   - 정성적 분석 (워드클라우드)
   - 시계열 분석 (시간대별 조회수)
   - 카테고리별 비교 분석

## 설치 및 실행 방법

1. 필요한 패키지 설치:
```bash
pip install dash pandas plotly google-api-python-client
```
2. 애플리케이션 실행:
```bash
python UI/main.py
```
! Data sample 이 없는 경우
YouTube API 키 설정:
- `collect.py` 파일에서 API_KEY 변수를 본인의 YouTube API 키로 변경



## 기술 스택

- **프론트엔드**
  - Dash (웹 프레임워크)
  - Plotly (시각화)
  - HTML/CSS

- **백엔드**
  - Python
  - YouTube Data API
  - Pandas (데이터 처리)
  - Web Crawling

## 주의사항

- YouTube API 키는 개인적으로 발급받아 사용해야 합니다.
- API 사용량 제한에 주의해야 합니다.
- 웹 크롤링 시 대상 사이트의 robots.txt를 준수해야 합니다. 