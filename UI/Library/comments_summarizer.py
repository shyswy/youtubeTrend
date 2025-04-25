import pandas as pd
import openai
import re
try:
    from Library.word_visualization import read_file 
except ImportError:
    from word_visualization import read_file

def load_api_key(path="./../../../LG_bootcamp_openai_api_key.txt"):
    try:
        path = "./../../../LG_bootcamp_openai_api_key.txt"
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        path = "./../../../LG_bootcamp_openai_api_key.txt"
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip()



def summarize_youtube_comments_by_id(video_id, country = "KR", category = "all"):
    """
    특정 YouTube video_id에 대한 댓글 요약 및 감정 점수 추정 함수

    Parameters:
        csv_path (str): 댓글이 저장된 CSV 파일 경로
        target_video_id (str): 요약할 YouTube 영상의 video_id

    Returns:
        Tuple[str, int, int]: 요약 텍스트, 긍정 점수, 부정 점수
    """
    try:
        openai.api_key = load_api_key()
    except Exception as e:
        print(f"api key가 없는거 같습니다 :{e}")
        return ["gpt api Key가 없습니다", -1, -1]

    csv_path, _ = read_file(country, category, type = "comments")
    try:
        df = pd.read_csv(csv_path,
            engine='python',
            encoding='utf-8',
            on_bad_lines='skip'
            )

        if "comment_text" not in df.columns or "video_id" not in df.columns:
            print("CSV에 'comment_text', 'video_id' 열이 필요합니다.")
            return None

        df = df[['video_id', 'comment_text']].dropna()

    except Exception as e:
        return [f"- CSV 파일 로딩 실패: {str(e)}", -1, -1]

    filtered_df = df[df['video_id'] == video_id]

    if filtered_df.empty:
        return ["- 해당 video_id에 대한 댓글이 없습니다.", 0, 0]

    comments = [c.strip() for c in filtered_df['comment_text'].values if isinstance(c, str) and len(c.strip()) > 10][:10]

    if not comments:
        return ["- 요약할 충분한 댓글이 없습니다.", 0, 0]

    comment_block = "\n".join(comments)

    prompt = f"""
아래는 YouTube 영상 하나에 달린 여러 댓글입니다. 이 댓글들을 참고하여 시청자들의 반응을 3줄 이내로 요약해 주세요.

또한 전체 댓글의 분위기를 감안하여 긍정/부정 점수를 100점 만점 기준으로 추산해 주세요.
예시 형식: (긍정: 75 / 부정: 25)

[Video ID: {video_id}]
댓글 목록:
{comment_block}

요약:
-
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response['choices'][0]['message']['ceontnt'].strip()

        # 정규식으로 점수 추출
        match = re.search(r'긍정\s*[:：]\s*(\d+)\s*/\s*부정\s*[:：]\s*(\d+)', content)
        if match:
            pos_score, neg_score = int(match.group(1)), int(match.group(2))
        else:
            pos_score, neg_score = -1, -1  # 점수 추출 실패

        return [content, pos_score, neg_score]

    except Exception as e:
        return [f"- 요약 실패: {str(e)}", -1, -1]

if __name__ == '__main__':
    result = summarize_youtube_comments_by_id("Qhz2L8WzgIw", country = "KR", category = "all")
    print(result)