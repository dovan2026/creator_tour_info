"""
한국관광공사 콘텐츠랩(api.visitkorea.or.kr) 관광정보 크롤러
- 데이터 유형: 관광정보(DB)
- 언어: 한국어(KOR)
- 카테고리: 전체
- 지역: 전체
- 수집 항목: 제목(title), 카테고리(contentTypeId/카테고리명), 개요(outl)
"""

import requests
import csv
import time
import os
from datetime import datetime

# =============================================
# 설정
# =============================================
BASE_URL = "https://api.visitkorea.or.kr"
TOUR_INFO_URL = f"{BASE_URL}/hub/getTourDbInfo.do"
TOUR_CNT_URL  = f"{BASE_URL}/hub/getTourDbInfoTotalCnt.do"
TOUR_TYPE_URL = f"{BASE_URL}/hub/getTourType.do"

BATCH_SIZE = 100   # 한 번에 가져올 건수 (100이 안정적)
DELAY = 0.3        # 요청 간 딜레이(초)

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://api.visitkorea.or.kr",
    "Referer": "https://api.visitkorea.or.kr/#/hubTourSearch",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
}

OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "visitkorea_tour_data.csv")

# contentTypeId -> 카테고리명 기본 매핑
CONTENT_TYPE_MAP = {
    "12": "관광지",
    "14": "문화시설",
    "15": "행사/공연/축제",
    "25": "여행코스",
    "28": "레포츠",
    "32": "숙박",
    "38": "쇼핑",
    "39": "음식점",
}

# =============================================
# 카테고리명 API로 가져오기
# =============================================
def fetch_content_types():
    """API에서 콘텐츠 유형 목록을 가져옵니다."""
    try:
        payload = {"ctgrCd": "KOR_CONTENTTYPE"}
        resp = requests.post(TOUR_TYPE_URL, json=payload, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            mapping = {}
            for item in data:
                cid = str(item.get("ctgrCd", "")).replace("KOR_CONTENTTYPE_", "")
                cname = item.get("ctgrNm", "")
                if cid and cname:
                    mapping[cid] = cname
            if mapping:
                print(f"[INFO] 콘텐츠 유형 {len(mapping)}개 로드: {mapping}")
                return mapping
    except Exception as e:
        print(f"[WARN] 콘텐츠 유형 API 실패, 기본값 사용: {e}")
    return CONTENT_TYPE_MAP

# =============================================
# 전체 건수 조회
# =============================================
def fetch_total_count():
    payload = {
        "type": "all",
        "lang": "KOR",
        "cat1": [], "cat2": [], "cat3": [],
        "areaCd": [], "sigunguCd": [], "nuri": [],
        "title": "",
        "searchStart": 0,
        "searchCnt": BATCH_SIZE,
        "pageNo": 1,
        "pageCnt": 1,
        "mainYn": "N",
    }
    resp = requests.post(TOUR_CNT_URL, json=payload, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return int(resp.text.strip())

# =============================================
# 배치 조회
# =============================================
def fetch_batch(search_start: int, search_cnt: int = BATCH_SIZE):
    payload = {
        "type": "all",
        "lang": "KOR",
        "cat1": [], "cat2": [], "cat3": [],
        "areaCd": [], "sigunguCd": [], "nuri": [],
        "title": "",
        "searchStart": search_start,
        "searchCnt": search_cnt,
        "pageNo": 1,
        "pageCnt": 1,
        "mainYn": "N",
    }
    resp = requests.post(TOUR_INFO_URL, json=payload, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()

# =============================================
# 메인
# =============================================
def main():
    print("=" * 60)
    print("한국관광공사 콘텐츠랩 관광정보 크롤러")
    print(f"시작 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 콘텐츠 유형 로드
    content_type_map = fetch_content_types()

    # 전체 건수 확인
    print("\n[1단계] 전체 건수 확인 중...")
    total = fetch_total_count()
    print(f"  -> 전체 관광정보: {total:,}건")

    # CSV 파일 열기
    print(f"\n[2단계] 데이터 수집 시작 -> {OUTPUT_PATH}")

    success_count = 0
    error_count = 0

    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        # 헤더 작성
        writer.writerow(["번호", "contentId", "제목", "카테고리ID", "카테고리명", "개요", "주소"])

        start = 0
        batch_num = 0
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE

        while start < total:
            batch_num += 1
            retry = 0
            max_retry = 3

            while retry < max_retry:
                try:
                    items = fetch_batch(start, BATCH_SIZE)

                    if not items:
                        print(f"  [배치 {batch_num}/{total_batches}] 빈 응답 (start={start}), 종료")
                        start = total  # 루프 종료
                        break

                    for item in items:
                        success_count += 1
                        content_id  = item.get("contentId", "")
                        title       = item.get("title", "").strip()
                        type_id     = str(item.get("contentTypeId", ""))
                        category_nm = content_type_map.get(type_id, type_id)
                        outl        = (item.get("outl") or "").strip().replace("\n", " ").replace("\r", "")
                        addr        = (item.get("addr1", "") or "").strip()

                        writer.writerow([success_count, content_id, title, type_id, category_nm, outl, addr])

                    # 진행 상황 출력
                    percent = min(100.0, (start + len(items)) / total * 100)
                    print(f"  [배치 {batch_num:4d}/{total_batches}] {start+1:6d}~{start+len(items):6d}건 완료 | 누적: {success_count:,}건 | {percent:.1f}%")

                    start += len(items)
                    break  # 성공 시 retry 루프 탈출

                except requests.exceptions.RequestException as e:
                    retry += 1
                    print(f"  [배치 {batch_num}] 오류 (재시도 {retry}/{max_retry}): {e}")
                    if retry < max_retry:
                        time.sleep(2 ** retry)  # 지수 백오프
                    else:
                        print(f"  [배치 {batch_num}] 최대 재시도 초과, 건너뜀 (start={start})")
                        error_count += 1
                        start += BATCH_SIZE  # 다음 배치로

            time.sleep(DELAY)

    print("\n" + "=" * 60)
    print("크롤링 완료!")
    print(f"  수집 성공: {success_count:,}건")
    print(f"  오류 건수: {error_count}건")
    print(f"  저장 파일: {OUTPUT_PATH}")
    print(f"종료 시각:  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


if __name__ == "__main__":
    main()
