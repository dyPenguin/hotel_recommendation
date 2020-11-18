# Hotel Recommendation Project

## 프로젝트 목표
호텔 선택 시, 중요한 참고 자료가 되는 리뷰 데이터를 통해 유의미한 단어들을 추출하고, 연관 관계를 분석하여 비슷한 호텔을 추천해주는 어플리케이션 개발

## 작업 환경
- Anaconda Python 3.7
- Pycharm
- Jupyter Notebook

## 사용 패키지
Selenium, PyQt5, pandas, urllib, sklearn, gensim, konlpy ‥

## 프로젝트 진행 과정
### 1. 데이터 수집
- Selenium 을 사용하여 크롤링

  > **네이버 호텔 사이트**
  > - 서울 지역
  > - 평점 6점 이상
  > - 호텔, 호스텔, 게스트 하우스, 모텔
  > - 부킹 닷컴 이용 후기

### 2. 자연어 처리

- Okt를 사용하여 토큰화
- 불용어(stopword) 처리
- 처리 된 데이터들을 한 줄로 구성

### 3. 모델 생성 및 학습

- Gensim 패키지를 통한 Word2Vec
- Embedding Model 생성
- 단어들의 유사도 분석

### 4. GUI 구현

## 주요 기능


