import io
import base64
import pandas as pd
from wordcloud import WordCloud
import re
from collections import Counter
import glob
import os

def generate_Title_WC(country="KR", category="all", image_Size = (800, 400), Max_words = 200):
    CATEGORY_TYPE = {
        'all': 'all',
        'entertainment': 'entertainment',
        'news': 'popular',
        'people_blogs': 'vlog',
        'music': 'music',
        'comedy': 'comedy',
        'sports': 'sports',
    }
    # 현재 스크립트의 디렉토리 경로를 기준으로 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)  # 프로젝트 루트 디렉토리
    csv_dir = os.path.join(project_root, "csvCollection")
    font_path = os.path.join(current_dir, "Font", "LGEITextTTF-Bold.ttf")
    
    print(f"현재 디렉토리: {current_dir}")
    print(f"프로젝트 루트: {project_root}")
    print(f"CSV 디렉토리: {csv_dir}")
    print(f"폰트 경로: {font_path}")
    
    csv_path = f"./../csvCollection/{country}_{CATEGORY_TYPE[category]}_video.csv"
    print(f"선택된 CSV 파일: {csv_path}")

    try:
        df = pd.read_csv(csv_path,
                    engine='python',
                    encoding='utf-8',
                    on_bad_lines='skip'
                    )

        if "title" not in df.columns or "viewCount" not in df.columns:
            print("CSV에 'title'과 'viewCount' 열이 필요합니다.")
            return None

        korean_stopwords = set([
            "더보기", "보기", "입니다", "하는", "있습니다", "합니다", "라는",
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


def find_latest_csv(prefix, folder="."):
    print(f"검색 패턴: {prefix}")
    print(f"검색 디렉토리: {folder}")
    
    pattern = os.path.join(folder, f"{prefix}_*.csv")
    print(f"전체 패턴: {pattern}")
    
    matched_files = glob.glob(pattern)
    print(f"찾은 파일들: {matched_files}")

    if not matched_files:
        print("해당 국가, 카테고리에 맞는 CSV 파일이 없습니다.")
        return None
    return max(matched_files, key=os.path.getmtime)

if __name__ == '__main__':
    from PIL import Image
    import matplotlib.pyplot as plt
    
    # 현재 스크립트의 디렉토리 경로를 기준으로 csvCollection 디렉토리 경로 설정
    current_dir = os.path.dirname(os.path.abspath(__file__))
    comment_csv_path = os.path.join(current_dir, "..", "csvCollection", "KR_all_comments_20250421_1017.csv")
    img_base64 = generate_Title_WC(country="KR", category="all", image_Size = (1200, 600), Max_words = 100)
    if img_base64 and img_base64.startswith("data:image"):
        img_base64_data = img_base64.split(",")[1]

        # 2. base64 디코딩 → 이미지 바이트
        image_data = base64.b64decode(img_base64_data)

        # 3. BytesIO → PIL 이미지로 변환
        image = Image.open(io.BytesIO(image_data))

        # 4. matplotlib으로 출력
        plt.imshow(image)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
    else:
        print("이미지 생성에 실패했습니다.")



if __name__ == '__main__':
    from PIL import Image
    import matplotlib.pyplot as plt
    comment_csv_path = "./../csvCollection\KR_all_comments_20250421_1017.csv"
    img_base64 = generate_Title_WC(country="KR", category="all", image_Size = (1200, 600), Max_words = 100)
    if img_base64 and img_base64.startswith("data:image"):
        img_base64_data = img_base64.split(",")[1]

        # 2. base64 디코딩 → 이미지 바이트
        image_data = base64.b64decode(img_base64_data)

        # 3. BytesIO → PIL 이미지로 변환
        image = Image.open(io.BytesIO(image_data))

        # 4. matplotlib으로 출력
        plt.imshow(image)
        plt.axis("off")
        plt.tight_layout()
        plt.show()
    else:
        print("이미지 생성에 실패했습니다.")