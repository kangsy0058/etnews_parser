# etnews_parser
---
etnews rss 피드를 파싱하는 파서입니다.

# How to use
---
* install python library : feedparser, BeautifulSoup4, requests
* run main.py

# File Structure

>- main.py : main code file
>- error_log.txt : error log file 
>- json_data : parsing data folder
>   - date.json : news data
>- category_parser : parsing by category

## main.py
- 실행파일 입니다.

## json_data
- json 파일을 보관하는 폴더입니다.

## date.json 
- 파일이름은 날짜 "year-month-date.json" 형식으로 저장됩니다. 
- 하루에 파일 하나씩을 생성합니다.

## error_log.txt
- 파싱과정중 일어난 로그들을 저장하는 파일입니다. 
- 전체 로그들을 파일하나에 합쳐서 보관합니다.

## category_parser
- 카테고리별로 파싱을 해줍니다.
- 일자별로 새롭게 파일이 생성되는 방식이아닌 실행시킬때마다 파일이 갱신되는 방식입니다.
- Category : broadcast, economy, electronics, industry, matarial, software, today, today_recommanded