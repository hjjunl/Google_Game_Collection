from numpy import double
from openpyxl import load_workbook
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager  # 'webdriver_manager' 패키지모듈 다운로드 필요
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
import random,time,os,sys
import traceback
from datetime import datetime

# Get today's date
today_date = datetime.today().strftime('%Y-%m-%d')
WAIT_TIME = 60
def wait_element_ready(_driver: webdriver, xpath: str, wait: int = WAIT_TIME) -> WebElement:
    WebDriverWait(_driver, wait).until(
        expected_conditions.presence_of_all_elements_located(
            (By.XPATH, xpath)))
    web_element = _driver.find_element("xpath", xpath)
    return web_element


GMAIL = 'hyunjun960214'
PASSWORD = 'hjl960214'

chrome_options = uc.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--profile-directory=Default")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("user_agent=DN")
driver = uc.Chrome(options=chrome_options)
driver.delete_all_cookies()

try:
    driver.get("https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow")
    # id 입력
    wait_element_ready(driver,  "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(GMAIL)
    wait_element_ready(driver,  "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    # 비밀번호 입력
    time.sleep(10)
    wait_element_ready(driver, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input").send_keys(PASSWORD)

    wait_element_ready(driver,  "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    time.sleep(10)

    # 탭추가
    driver.execute_script('window.open("about:blank", "_blank");')
    # time.sleep(10)
    driver.switch_to.window(driver.window_handles[1])
    # 로그인후 플레이스토어 접근
    play_store_url= 'https://play.google.com/store/games?device=phone&hl=ko-KR'
    driver.get(play_store_url)
    # 전체 DF 생성
    columns = ["famous_games", "date", "game_nm", "game_intro", "realse_date", "developer", "contents_grade", "game_tag", "star_5", "star_4", "star_3", "star_2", "star_1", "star_avg", "review_count", "game_review_list"]
    df = pd.DataFrame(columns=columns)
    # 인기 앱/게임,최고매출, 인기 유료 탭 접근 4
    for tab in range(1, 4):
        time.sleep(10)
        print("3가지 탭접근: ", tab)
        try:
            wait_element_ready(driver,"/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div[1]/div/div/div[" + str(tab) + "]/div[2]/span[2]").click()
            famous_games = wait_element_ready(driver,"/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div[1]/div/div/div[" + str(tab) + "]/div[2]/span[2]").text

        except Exception:
            time.sleep(10)
            wait_element_ready(driver,"/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div[1]/div/div/div[" + str(tab) + "]/div[2]/span[2]").click()
            famous_games = wait_element_ready(driver,"/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div[1]/div/div/div[" + str(tab) + "]/div[2]/span[2]").text

        # 게임 접근 Top 46
        for fm in range(1, 16): # 컬럼이 15번 3번 반복

            time.sleep(10)
            # 게임 상세 클릭
            print("게임 46: ", fm)
            for col in range(1, 4):
                # 게임 row 정보
                game_list = []
                game_list.append(famous_games)
                # 오늘 날짜 수집
                game_list.append(today_date)
                # 게임 리뷰 리스트
                game_review_list = []
                time.sleep(10)
                try:
                    wait_element_ready(driver, "/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div[3]/div/div/div/div[1]/div[" + str(fm) + "]/div[" + str(col) + "]/div/a").click()
                except Exception:
                    print("check 뒤로 안가보기")
                    # driver.back()
                    time.sleep(20)
                    wait_element_ready(driver, "/html/body/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/c-wiz[2]/c-wiz/section/div/div[3]/div/div/div/div[1]/div[" + str(fm) + "]/div[" + str(col) + "]/div/a").click()

                # 게임명
                game_nm = wait_element_ready(driver,"//*[@id='yDmH0d']/c-wiz[3]/div/div/div[2]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1").text
                game_list.append(game_nm)
                print("game_nm: ", game_nm)
                # 게임 소개 상세 클릭
                try:
                    wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/header/div/div[2]/button").click()
                except Exception:
                    time.sleep(20)
                    wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/header/div/div[2]/button").click()
                # 게임 소개
                game_intro = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[1]").text
                print("game_info: ", game_intro[:20])
                game_list.append(game_intro)
                # 출시일
                try:
                    realse_date = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[9]/div[2]").text
                except Exception:
                    realse_date = wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[7]/div[2]").text
                except Exception:
                    realse_date = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[8]/div[2]").text

                game_list.append(realse_date)
                # 개발자
                try:
                    developer = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[8]/div[2]").text
                except Exception:
                    developer = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[9]/div[2]").text
                except Exception:
                    developer = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[10]/div[2]").text

                game_list.append(developer)
                # 콘텐츠 등급
                for trying in range(5,8):
                    try:
                        contents_grade = wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[" + str(trying) + "]/div[2]/div").text
                        break
                    except Exception:
                        print("trying: ", trying)
                        # contents_grade = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[6]/div[2]/div").text
                        pass
                # except Exception:
                #     print(wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[6]/div[2]/div").text)
                #     contents_grade = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[7]/div[2]/div").text
                # except Exception:
                #     contents_grade = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[3]/div[8]/div[2]/div").text

                game_list.append(contents_grade)
                # 게임 소개 나가기
                wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[1]/button").click()
                # 게임 태그
                game_tag = ''
                for tag in range(1, 6):
                    try:
                        game_tag = game_tag + " ," + wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[2]/div/section/div/div[3]/div[" + str(tag) + "]").text
                    except Exception:
                        print("tag 수집 종료")
                        break
                print("game_tag: ", game_tag)
                game_list.append(game_tag)
                # 평가
                star_5 = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[2]/div[1]/div[2]/div").get_attribute("title")
                star_4 = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div").get_attribute("title")
                star_3 = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/div").get_attribute("title")
                star_2 = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[2]/div[4]/div[2]/div").get_attribute("title")
                star_1 = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[2]/div[5]/div[2]/div").get_attribute("title")
                game_list.append(star_5)
                game_list.append(star_4)
                game_list.append(star_3)
                game_list.append(star_2)
                game_list.append(star_1)
                print("star5: ", star_5)
                # 평군 별점
                star_avg = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[1]/div[1]").text
                print("star_avg: ", star_avg)
                game_list.append(star_avg)
                # = wait_element_ready(driver,"").text
                # 리뷰 수
                try:
                    review_count = wait_element_ready(driver, "/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[1]/div[3]").text
                    print("review_count: ", review_count)
                except Exception:
                    review_count = wait_element_ready(driver,"/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/div/div[2]/div[1]/div/div/div[1]/div[3]/text()[2]").text
                    print("text는 text뒤에 필요없음")
                    pass
                    print("review_count: ", review_count)
                if "천개" in review_count[3:]:
                    print("천단위")
                    game_list.append(double(review_count[3:].replace("천개", ""))*1000)
                elif "만개" in review_count[3:]:
                    print("만단위")
                    if "," in review_count[3:].replace("만개", ""):
                        game_list.append(double(review_count[3:].replace("만개", "").replace(",", "")) * 10000)
                    else:
                        game_list.append(double(review_count[3:].replace("만개", ""))*10000)
                else:
                    game_list.append(int(review_count[3:].replace("개", "")))
                # 평가 및 리뷰 상세 클릭
                try:
                    print("기본 리뷰상세클릭")
                    wait_element_ready(driver, "/html/body/c-wiz[3]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/header/div/div[2]/button").click()
                except Exception:
                    print("바뀐 리뷰상세클릭")
                    wait_element_ready(driver, "/html/body/c-wiz[4]/div/div/div[2]/div[2]/div/div[1]/div[1]/c-wiz[4]/section/header/div/div[2]/button").click()

                # 리뷰 필터 클릭
                try:
                    print("기존 리뷰필터 클릭")
                    time.sleep(5)
                    wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div/div[2]/div[2]/i").click()
                except Exception:
                   print("기졸 리뷰필터와 다름")
                   wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/div/div/div/div[2]/div[2]/i").click()
                # 리뷰 필터 최신 클릭
                try:
                    wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[2]/div[2]/div[2]").click()
                except Exception:
                    time.sleep(10)
                    wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div[2]/div/div/span[2]/div[2]/div[2]").click()
                for i in range(1, 10+1): #int(review_count[3:].replace("개", ""))
                    review_list = []
                    try:
                        time.sleep(5)
                        # 리뷰 날짜
                        review_date = wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div/div[2]/div[" + str(i) + "]/header/div[2]/span").text
                        # 리뷰 별점
                        review_stars = wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[2]/div/div[2]/div[" + str(i) + "]/header/div[2]/div").text
                        # 리뷰 컨텐츠
                        review_contents = wait_element_ready(driver,"/html/body/div[5]/div[2]/div/div/div/div/div[2]/div/div[2]/div[" + str(i) + "]/div[1]").text
                        review_list.append([review_date, review_stars, review_contents])
                    except Exception as ex:
                        err_msg = traceback.format_exc()
                        print(err_msg)
                        pass
                    game_review_list.append(review_list)
                # print(game_review_list[:10])
                game_list.append(game_review_list)
                print(len(game_review_list))
                print("모아둔 game_list: ", game_list)
                # 평가 및 리뷰 상세 나가기
                wait_element_ready(driver, "/html/body/div[5]/div[2]/div/div/div/div/div[1]/button").click()

                print("game_list len: ", len(game_list))
                try:
                    df.loc[len(df)] = game_list
                except Exception:
                    df.loc[0] = game_list
                print("df: ", df)
                time.sleep(5)
                # 메인페이지로 가기
                driver.back()
                print("뒤로가기")
    df.to_excel(str(today_date) + "test.xlsx")
    driver.close()
except Exception as ex:
    print("드라이버 종료")
    err_msg = traceback.format_exc()
    print(err_msg)
    driver.close()
    df.to_excel(str(today_date) + "test.xlsx")
