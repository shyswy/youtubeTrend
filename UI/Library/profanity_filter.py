from better_profanity import profanity
import re

# 영어 욕설 사전 초기화
profanity.load_censor_words()

# 추가적으로 삭제하고 싶은 특정 단어
BANWORD_SET = set([
    # 예: "일베", "틀딱" 등 사용자 정의 단어
])

# 한국어 욕설 우회 표현까지 커버하는 정규식 패턴
BADWORD_PATTERNS = [
    r"씨\s*[^가-힣a-zA-Z0-9]{0,2}?\s*발",
    r"시\s*[^가-힣a-zA-Z0-9]{0,2}?\s*발",
    r"ㅅ\s*[^가-힣a-zA-Z0-9]{0,2}?\s*ㅂ",
    r"ㅆ\s*[^가-힣a-zA-Z0-9]{0,2}?\s*ㅂ",
    r"ㅂ\s*[^가-힣a-zA-Z0-9]{0,2}?\s*ㅅ",
    r"좆", r"좇",
    r"ㅈ\s*[^가-힣a-zA-Z0-9]{0,2}?\s*같",
    r"병\s*[^가-힣a-zA-Z0-9]{0,2}?\s*신",
    r"개\s*[^가-힣a-zA-Z0-9]{0,3}?\s*새끼",
    r"c\s*8"
]

# 한글 욕설 탐지
def is_korean_profane(text: str) -> bool:
    lowered = text.lower()
    return any(re.search(pat, lowered) for pat in BADWORD_PATTERNS)

# 통합 욕설 필터 함수 (한글 + 영어 + 커스텀 단어)
def is_abusive_comment(text: str) -> bool:
    lowered = text.lower()
    return (
        profanity.contains_profanity(lowered) or
        is_korean_profane(lowered) or
        any(bad in lowered for bad in BANWORD_SET)
    )


# 욕설 제거용 Clean 함수
def clean_abusive_words(sentence: str) -> str:
    if not is_abusive_comment(sentence):  # 욕설이 없다면 그대로 반환
        return sentence
    words = sentence.split()
    cleaned = [word if not is_abusive_comment(word) else "" for word in words]
    return " ".join(cleaned).strip()



if __name__ =='__main__':
    test_english_abuse_variants = [
        "f*ck you",
        "f***ing idiot",
        "f.u.c.k you",
        "fucck off",
        "fuxking dumb",
        "bish please",
        "you little a$$hole",
        "sh!t happens",
        "daMn you",
        "you’re such a b@stard"
    ]
    test_english_abuse = [
        "fuck you",
        "you are a bitch",
        "what the hell",
        "damn this video",
        "you asshole",
        "shit happens",
        "go to hell",
        "he is such a bastard",
        "this is fucking stupid",
        "you're a piece of shit"
    ]
    test_clean_english = [
        "I really love this video",
        "Great content as always",
        "Can you explain more?",
        "This is so interesting!",
        "Keep up the good work"
    ]

    test_clean_korean = [
        "이 영상 진짜 좋네요",
        "감사합니다 잘 보고 갑니다",
        "재밌는 콘텐츠네요!",
        "좋아요 눌렀어요",
        "응원합니다~"
    ]
    test_korean_abuse_variants = [
        "씨1발 뭐야",       # 숫자
        "ㅅ.ㅂ 진심?",       # 특수문자
        "ㅆ-ㅂ 개웃기네",     # 하이픈
        "시ㅡ발 아니네",     # 모음 분리
        "ㅂ.ㅅ인가?",        # 병신 우회
        "좇같",              # 종성만
        "ㅈ같은 느낌",       # 자음 약어
        "c8 진짜 개웃김",    # 영어 대체
        "개!새끼",           # 특수기호
        "개ㅡㅡㅡ새끼"        # 늘이기
    ]
    test_korean_abuse = [
        "씨발 뭐야",
        "ㅅㅂ 진짜 어이없다",
        "병신 같네",
        "개새끼가 또 왔네",
        "좆같은 소리하지 마",
        "존나 웃기네",
        "미친놈 아냐?",
        "그냥 꺼져라",
        "죽어라 진짜",
        "저 새끼 말하는 꼬라지 봐"
    ]

    Total_set = test_english_abuse + test_english_abuse_variants + test_clean_english + test_korean_abuse + test_korean_abuse_variants + test_clean_korean

    def run_all_profanity_test():
        for sentence in Total_set:
            if is_abusive_comment(sentence):
                print("[욕설 탐지됨] →", sentence, "->", clean_abusive_words(sentence))
            else:
                print("[정상] →", sentence, "->", clean_abusive_words(sentence))

    run_all_profanity_test()