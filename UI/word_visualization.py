import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
import glob
import os


def generate_Title_WC(country = "korea", category = "all"):
    CATEGORY_TYPE = {
        'all': 'all',
        'entertainment': 'entertainment',
        'news': 'popular',
        'people_blogs': 'vlog',
        'music': 'music',
        'comedy': 'comedy',
        'sports': 'sports',
    }
    COUNTRY_TYPE = {
        "korea": "KR",
        "usa": "US",
    }

    csv_path = find_latest_csv(f"./../csvCollection/{COUNTRY_TYPE[country]}_{CATEGORY_TYPE[category]}_data")

    try:
        df = pd.read_csv(csv_path)

        if "title" not in df.columns or "viewCount" not in df.columns:
            print("CSV에 'title'과 'viewCount' 열이 필요합니다.")
            return

        # 한글/영어 불용어 통합
        korean_stopwords = set([
            "더보기", "보기", "입니다", "하는", "있습니다", "합니다", "라는", "하는",
            "영상", "노래", "제목", "공식", "티저", "쇼케이스", "기자회견", "있다", "이다", "자막"
        ])

        english_stopwords = set([
            "a", "an", "the", "on", "in", "at", "by", "for", "to", "of", "with", "about", "against", "between", "into", "through", "during",
            "before", "after", "above", "below", "from", "up", "down", "over", "under", "again", "further", "then", "once", "out", "off",
            "onto", "upon", "and", "but", "or", "so", "yet", "nor", "as", "because", "while", "although", "though", "if", "unless", "until",
            "since", "when", "where", "whether", "is", "are", "was", "were", "be", "been", "being", "do", "does", "did", "have", "has", "had",
            "can", "will", "shall", "would", "could", "should", "may", "might", "must", "let", "also"
        ])

        stopwords = korean_stopwords.union(english_stopwords)

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
            font_path="./Font/LGEITextTTF-Bold.ttf",  # 한글 폰트
            width=800,
            height=400,
            background_color="white",
            colormap="coolwarm",
            contour_width=2,
            contour_color='black',
            max_words=200
        ).generate_from_frequencies(word_freq)

        plt.figure(figsize=(12, 6))
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"에러 발생: {e}")


def find_latest_csv(prefix, folder="."):
    pattern = os.path.join(folder, f"{prefix}*.csv")
    matched_files = glob.glob(pattern)

    if not matched_files:
        print("해당 접두사에 맞는 CSV 파일이 없습니다.")
        return None

    # 수정 시간 기준으로 가장 최근 파일 선택
    latest_file = max(matched_files, key=os.path.getmtime)
    return latest_file



if __name__ == '__main__':
    #title_csv_path = "./../csvCollection/KR_sports_data_20250421_1017.csv"
    comment_csv_path = "./../csvCollection\KR_all_comments_20250421_1017.csv"
    generate_Title_WC()
    #generate_Comments_WC(comment_csv_path)