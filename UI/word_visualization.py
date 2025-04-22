import io
import base64
import pandas as pd
from wordcloud import WordCloud
import re
from collections import Counter
import glob
import os
from Library.profanity_filter import clean_abusive_words

KOREAN_STOPWORDS = set([
    "더보기", "보기", "입니다", "하는", "있습니다", "합니다", "라는",
    "영상", "노래", "제목", "공식", "티저", "쇼케이스", "기자회견", "있다", "이다", "자막",
    "정말", "너무", "진짜", "그냥", "근데", "ㅋㅋ", "ㅎㅎ", "와", "음", "아", "앗",
    "요", "죠", "네", "아니", "이건", "저는", "제가", "우와", "대박", "하", "헐",
    "그", "이", "저", "것", "걸", "때", "분", "사람", "지금", "좀", "거", "건", "게", "되게", "되서"
])

ENGLISH_STOPWORDS = set([
    "a", "an", "the", "on", "in", "at", "by", "for", "to", "of", "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "from", "up", "down", "over", "under", "again", "further", "then", "once", "out", "off",
    "onto", "upon", "and", "but", "or", "so", "yet", "nor", "as", "because", "while", "although", "though", "if", "unless", "until",
    "since", "when", "where", "whether", "is", "are", "was", "were", "be", "been", "being", "do", "does", "did", "have", "has", "had",
    "can", "will", "shall", "would", "could", "should", "may", "might", "must", "let", "also",
    "omg", "lol", "wow", "yes", "no", "okay", "ok", "uh", "oh", "hi", "hey", "haha", "hahaha", "wa", "yea", "yeah", "yup", "huh", "eh"
])

def generate_Title_WC(country="KR", category="all", image_Size = (800, 400), Max_words = 200):

    csv_path, font_path = read_file(country, category, type = "video")
    try:
        df = pd.read_csv(csv_path,
                    engine='python',
                    encoding='utf-8',
                    on_bad_lines='skip'
                    )

        if "title" not in df.columns or "viewCount" not in df.columns:
            print("CSV에 'title'과 'viewCount' 열이 필요합니다.")
            return None

        stopwords = KOREAN_STOPWORDS.union(ENGLISH_STOPWORDS)

        word_freq = Counter()

        for _, row in df.iterrows():
            title = str(row["title"])
            try:
                view = int(row["viewCount"])
            except ValueError:
                continue

            cleaned = re.sub(r"[^가-힣a-zA-Z\s]", " ", title).lower()
            tokens = cleaned.split()

            for token in tokens:
                if token not in stopwords and len(token) > 1:
                    word_freq[token] += int(view * 0.001)

        wc = WordCloud(
            font_path=font_path,
            width=image_Size[0],
            height=image_Size[1],
            background_color="white",
            colormap="coolwarm",
            contour_width=2,
            contour_color='black',
            max_words=Max_words
        ).generate_from_frequencies(word_freq)

        # 메모리에 이미지 저장
        img_io = io.BytesIO()
        wc.to_image().save(img_io, format='PNG')
        img_io.seek(0)

        # base64 인코딩
        img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        print(f"에러 발생: {e}")
        return None

def generate_Comments_WC(video_ID, country="KR", category="all", image_Size = (800, 800), Max_words = 200):
    
    csv_path, font_path = read_file(country, category, type = "comments")

    try:
        df = pd.read_csv(csv_path,
                    engine='python',
                    encoding='utf-8',
                    on_bad_lines='skip'
                    )

        if "comment_text" not in df.columns or "comment_likes" not in df.columns or "video_id" not in df.columns:
            print("CSV에 'comment_text','comment_likes', 'video_id' 열이 필요합니다.")
            return None

        stopwords = KOREAN_STOPWORDS.union(ENGLISH_STOPWORDS)
        word_freq = Counter()

        for _, row in df.iterrows():
            if str(row["video_id"]) != video_ID:
                continue
            text = clean_abusive_words(str(row["comment_text"]))
            if len(text) == 0:
                continue
            try:
                like = int(row["comment_likes"])
            except ValueError:
                continue
            cleaned = re.sub(r"[^가-힣a-zA-Z\s]", " ", text).lower()
            tokens = cleaned.split()

            for token in tokens:
                if token not in stopwords and len(token) > 1:
                    word_freq[token] += int(1+ like * 0.01)

        wc = WordCloud(
            font_path=font_path,
            width=image_Size[0],
            height=image_Size[1],
            background_color="white",
            colormap="coolwarm",
            contour_width=2,
            contour_color='black',
            max_words=Max_words
        ).generate_from_frequencies(word_freq)

        # 메모리에 이미지 저장
        img_io = io.BytesIO()
        wc.to_image().save(img_io, format='PNG')
        img_io.seek(0)
        # base64 인코딩
        img_base64 = base64.b64encode(img_io.read()).decode('utf-8')
        return f"data:image/png;base64,{img_base64}"

    except Exception as e:
        print(f"에러 발생: {e}")
        return None

def read_file(country, category, type = "video"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_dir = os.path.join(current_dir, "youtube_data")
    font_path = os.path.join(current_dir, "Font", "LGEITextTTF-Bold.ttf")
    
    print(f"현재 디렉토리: {current_dir}")
    print(f"CSV 디렉토리: {csv_dir}")
    print(f"폰트 경로: {font_path}")

    # 파일명 패턴 수정
    if type == "video":
        pattern = os.path.join(csv_dir, f"{country}_{category}_video.csv")
    else:
        pattern = os.path.join(csv_dir, f"{country}_{category}_comments.csv")
    
    print(f"검색 패턴: {pattern}")
    matched_files = glob.glob(pattern)

    if not matched_files:
        print(f"해당 국가({country}), 카테고리({category})에 맞는 CSV 파일이 없습니다.")
        return None, None

    csv_path = matched_files[0]  # 첫 번째 매칭된 파일 사용
    print(f"선택된 CSV 파일: {csv_path}")

    return csv_path, font_path




if __name__ == '__main__':
    from PIL import Image
    import matplotlib.pyplot as plt
    import time
    import math
    start = time.time()
    math.factorial(100000)
    #img_base64 = generate_Title_WC(country="KR", category="all", image_Size = (1200, 600), Max_words = 100)
    img_base64 = generate_Comments_WC("dtJ9j8grYHk", country="KR", category="all", image_Size = (400, 800), Max_words = 100)
    
    if img_base64 and img_base64.startswith("data:image"):
        img_base64_data = img_base64.split(",")[1]
        image_data = base64.b64decode(img_base64_data)
        image = Image.open(io.BytesIO(image_data))
        end = time.time()
        print(f"{end - start:.5f} sec")
        plt.imshow(image)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
    else:
        print("이미지 생성에 실패했습니다.")
