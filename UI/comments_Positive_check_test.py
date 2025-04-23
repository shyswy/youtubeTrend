import pandas as pd
import openai
import time

# OpenAI API 키 설정
openai.api_key = 'your-api-key'  # 여기에 실제 키 입력

# CSV 파일 경로
csv_path = 'KR_all_comments.csv'
df = pd.read_csv(csv_path)

# 필수 컬럼 필터링
df = df[['video_id', 'comment_text']].dropna()

# video_id별로 그룹핑
grouped = df.groupby('video_id')['comment_text'].apply(list)

# 결과 저장용 딕셔너리
summaries = {}

# 각 video_id에 대해 요약 요청
for video_id, comments in grouped.items():
    # 최대 50개 댓글 추출 및 정제
    filtered = [c.strip() for c in comments if isinstance(c, str) and len(c.strip()) > 10][:50]
    if not filtered:
        summaries[video_id] = "- 요약할 댓글이 부족합니다."
        continue

    comment_block = "\n".join(filtered)

    # 프롬프트 구성
    prompt = f"""
아래는 YouTube 영상 하나에 달린 여러 댓글입니다. 이 댓글들을 참고하여 영상에 대한 시청자들의 반응을 3줄 이내로 요약해 주세요. 요약은 해당 영상의 댓글만을 기반으로 하며, 다른 영상의 댓글과 혼동하지 마세요.

[Video ID: {video_id}]
댓글 목록:
{comment_block}

요약:
- 
"""

    try:
        # OpenAI GPT 호출
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        summary = response['choices'][0]['message']['content'].strip()
        summaries[video_id] = summary
    except Exception as e:
        summaries[video_id] = f"- 요약 실패: {str(e)}"
    
    time.sleep(1)  # 과금/속도 제한 완화

# 결과 출력
for vid, summ in summaries.items():
    print(f"({vid}) 요약:\n{summ}\n")
