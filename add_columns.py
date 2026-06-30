"""
visitkorea_tour_data.csv에 '지역명'과 '감정' 컬럼을 추가하는 스크립트
- 지역명: 주소(addr1) 앞부분에서 시/도 추출
- 감정: 제목 + 카테고리명 + 개요 키워드 기반 분류
"""

import csv
import re
import os

INPUT_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visitkorea_tour_data.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visitkorea_tour_data_v2.csv")

# ============================================================
# 1. 지역명 매핑 (주소 앞 키워드 -> 지역명)
# ============================================================
REGION_MAP = [
    # 특별시/광역시
    ("서울",   "서울"),
    ("부산",   "부산"),
    ("대구",   "대구"),
    ("인천",   "인천"),
    ("광주",   "광주"),
    ("대전",   "대전"),
    ("울산",   "울산"),
    ("세종",   "세종"),
    # 도
    ("경기",   "경기"),
    ("강원",   "강원"),
    ("충청북도", "충북"),
    ("충북",   "충북"),
    ("충청남도", "충남"),
    ("충남",   "충남"),
    ("전라북도", "전북"),
    ("전북",   "전북"),
    ("전라남도", "전남"),
    ("전남",   "전남"),
    ("경상북도", "경북"),
    ("경북",   "경북"),
    ("경상남도", "경남"),
    ("경남",   "경남"),
    ("제주",   "제주"),
]

def extract_region(addr: str) -> str:
    addr = addr.strip()
    for keyword, region in REGION_MAP:
        if addr.startswith(keyword):
            return region
    return "기타"

# ============================================================
# 2. 감정 분류 (키워드 기반)
# ============================================================
# 각 감정과 관련 키워드 목록 (우선순위 순)
EMOTION_RULES = [
    ("경건함",   ["사찰", "절", "성당", "교회", "불교", "천주교", "기독교", "기도",
                  "불상", "승려", "법당", "대웅전", "보살", "수도", "수행", "명상",
                  "신성", "신앙", "종교", "선원"]),

    ("추모·숙연", ["순국", "독립운동", "항일", "열사", "의병", "임시정부", "광복",
                   "호국", "전쟁", "희생", "추모", "현충", "만세", "애국", "순절"]),

    ("향수·그리움", ["고택", "민속", "전통마을", "옛날", "고향", "전통문화", "서민",
                     "장터", "재래시장", "골목", "옛 모습", "생가", "전통가옥",
                     "한옥", "마을", "정겨운", "과거"]),

    ("역사·경이", ["유네스코", "세계유산", "유적", "성곽", "왕릉", "왕궁", "궁궐",
                   "고분", "사적", "문화재", "보물", "국보", "역사", "조선", "고려",
                   "삼국", "백제", "신라", "가야", "고구려"]),

    ("낭만·설렘", ["일몰", "노을", "야경", "불꽃", "연인", "데이트", "해변", "해수욕장",
                   "낭만", "로맨틱", "사랑", "아름다운 해변", "섬", "등대",
                   "카페", "감성", "드라이브"]),

    ("활력·도전", ["등산", "트레킹", "클라이밍", "래프팅", "서핑", "스키",
                   "번지", "짚라인", "스카이", "모험", "레포츠", "스포츠",
                   "자전거", "마라톤", "아드레날린", "짜릿", "도전"]),

    ("즐거움·흥겨움", ["축제", "공연", "행사", "콘서트", "놀이", "체험", "이벤트",
                       "불꽃축제", "퍼레이드", "관람", "구경", "재미", "신나는",
                       "놀이공원", "워터파크", "테마파크", "게임"]),

    ("힐링·평화", ["자연", "숲", "계곡", "폭포", "온천", "스파", "휴양", "치유",
                   "조용한", "평화", "힐링", "쉼", "힐", "삼림욕", "산책",
                   "정원", "수목원", "습지", "청정", "바람", "여유"]),

    ("경이·신비", ["화산", "동굴", "협곡", "절벽", "주상절리", "용암", "기암괴석",
                   "천연기념물", "신비", "비경", "장관", "절경", "웅장", "광활",
                   "거대", "특이한"]),

    ("배움·호기심", ["박물관", "기념관", "전시관", "과학관", "천문대", "미술관",
                    "교육", "학습", "체험관", "학예", "전시", "연구", "도서관",
                    "기록", "역사관", "문학관"]),

    ("맛·풍요",   ["맛집", "음식", "식당", "카페", "먹거리", "요리", "식문화",
                   "향토음식", "특산물", "해산물", "정식", "한정식", "분식",
                   "막걸리", "전통주", "수산", "로컬푸드"]),

    ("쇼핑·활기", ["시장", "쇼핑", "백화점", "상가", "특산품", "기념품",
                   "공예품", "아울렛", "재래시장", "면세", "상점"]),
]

def classify_emotion(title: str, category: str, outl: str) -> str:
    text = f"{title} {category} {outl}"
    scores = {}
    for emotion, keywords in EMOTION_RULES:
        score = sum(text.count(kw) for kw in keywords)
        if score > 0:
            scores[emotion] = score

    if scores:
        return max(scores, key=scores.get)

    # 카테고리 기본 감정
    cat_defaults = {
        "관광지":    "힐링·평화",
        "문화시설":  "배움·호기심",
        "행사/공연/축제": "즐거움·흥겨움",
        "여행코스":  "설렘·낭만",
        "레포츠":    "활력·도전",
        "숙박":      "힐링·평화",
        "쇼핑":      "쇼핑·활기",
        "음식점":    "맛·풍요",
    }
    return cat_defaults.get(category, "힐링·평화")

# ============================================================
# 3. 메인
# ============================================================
def main():
    print("=" * 60)
    print("지역명 + 감정 컬럼 추가 작업 시작")
    print("=" * 60)

    with open(INPUT_PATH, "r", encoding="utf-8-sig", newline="") as fin, \
         open(OUTPUT_PATH, "w", encoding="utf-8-sig", newline="") as fout:

        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["지역명", "감정"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        total = 0
        region_stats = {}
        emotion_stats = {}

        for row in reader:
            addr     = row.get("주소", "")
            title    = row.get("제목", "")
            category = row.get("카테고리명", "")
            outl     = row.get("개요", "")

            region  = extract_region(addr)
            emotion = classify_emotion(title, category, outl)

            row["지역명"] = region
            row["감정"]   = emotion

            writer.writerow(row)
            total += 1

            region_stats[region]   = region_stats.get(region, 0) + 1
            emotion_stats[emotion] = emotion_stats.get(emotion, 0) + 1

            if total % 5000 == 0:
                print(f"  처리 중: {total:,}건 완료...")

    print(f"\n완료! 총 {total:,}건 처리")
    print(f"저장 파일: {OUTPUT_PATH}")

    print("\n[지역별 통계]")
    for k, v in sorted(region_stats.items(), key=lambda x: -x[1]):
        print(f"  {k:10s}: {v:6,}건")

    print("\n[감정별 통계]")
    for k, v in sorted(emotion_stats.items(), key=lambda x: -x[1]):
        print(f"  {k:15s}: {v:6,}건")


if __name__ == "__main__":
    main()
