from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

def crawl_tour_api_hub():
    # 1. 웹드라이버 설정 (Chrome 기준)
    options = webdriver.ChromeOptions()
    # 필요 시 헤드리스 모드 활성화: options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    url = "https://api.visitkorea.or.kr/#/hubTourSearch"
    driver.get(url)
    
    scraped_data = []

    try:
        # 2. 페이지 로딩 대기
        time.sleep(3) # 초기 렌더링 대기
        
        # 3. 필터 설정 (데이터 유형, 언어, 카테고리 등)
        # 주의: 아래 XPath는 예시이며, 실제 웹사이트의 DOM 구조를 확인하여 반드시 수정해야 합니다.
        
        # 예시: '관광정보' 탭 클릭
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '관광정보')]"))).click()
        
        # 예시: 언어 '한국어' 선택
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), '한국어')]"))).click()
        
        # 예시: 검색 버튼 클릭
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '검색')]"))).click()
        
        time.sleep(3) # 검색 결과 로딩 대기

        # 4. 데이터 크롤링 루프 (페이지네이션 처리 포함)
        page_num = 1
        max_pages = 5 # 테스트를 위해 제한 (필요 시 수정)
        
        while page_num <= max_pages:
            print(f"--- {page_num} 페이지 크롤링 중 ---")
            
            # 현재 페이지의 리스트 아이템 추출
            # 주의: 실제 리스트 컨테이너와 아이템의 식별자로 변경해야 합니다.
            items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result-list > li")))
            
            for i in range(len(items)):
                try:
                    # DOM이 갱신될 수 있으므로 요소를 다시 찾음
                    items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".search-result-list > li")))
                    item = items[i]
                    
                    # 제목 및 카테고리 추출
                    title = item.find_element(By.CSS_SELECTOR, ".title-class").text
                    category = item.find_element(By.CSS_SELECTOR, ".category-class").text
                    
                    # 상세 보기 클릭 (개요 정보 추출을 위해)
                    item.click()
                    
                    # 상세 페이지/모달 로딩 대기 및 개요 추출
                    overview_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".overview-class")))
                    overview = overview_element.text
                    
                    scraped_data.append({
                        "제목": title,
                        "카테고리": category,
                        "개요": overview
                    })
                    
                    # 뒤로 가기 또는 모달 닫기
                    # driver.back() 또는 닫기 버튼 클릭
                    close_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-close")))
                    close_btn.click()
                    
                    time.sleep(1) # 복귀 후 DOM 안정화 대기
                    
                except Exception as e:
                    print(f"항목 추출 중 오류 발생: {e}")
                    continue
            
            # 다음 페이지 이동
            try:
                # 다음 페이지 버튼 식별자 지정
                next_button = driver.find_element(By.CSS_SELECTOR, ".pagination .next")
                if "disabled" in next_button.get_attribute("class"):
                    break # 마지막 페이지인 경우 루프 종료
                next_button.click()
                time.sleep(2)
                page_num += 1
            except NoSuchElementException:
                break # 다음 페이지 버튼이 없으면 종료

    except Exception as e:
        print(f"크롤링 중 치명적 오류 발생: {e}")
        
    finally:
        driver.quit()

    # 5. CSV 파일로 저장
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        file_name = "tour_info_crawled.csv"
        df.to_csv(file_name, index=False, encoding='utf-8-sig')
        print(f"크롤링 완료. 데이터가 {file_name}로 저장되었습니다.")
    else:
        print("수집된 데이터가 없습니다.")

if __name__ == "__main__":
    crawl_tour_api_hub()