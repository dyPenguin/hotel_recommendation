# Hotel Recommendation Project

## 프로젝트 목표
호텔을 선택할 때 중요한 참고 자료가 되는 리뷰 데이터를 통해 유의미한 단어들을 추출하고, 연관 관계를 분석하여 비슷한 호텔을 추천해 주는 어플리케이션 개발

## 작업 환경
- **Anaconda Python 3.7**
- **Pycharm**
- **Jupyter Notebook**

## 사용 패키지
**Selenium, PyQt5, pandas, urllib, sklearn, gensim, konlpy ‥**

- KoNLPy: 한글 형태소 분석 패키지 설치 전,

1. JAVA 1.7 이상의 설치
2. JAVA_HOME PATH 설정
3. JPype1 (>=0.5.7) 설치
```
pip install konlpy
```
- 그 외 필요한 패키지 파일 설치
```
pip install 패키지명
```

## 주요 기능
<p align="center"><메인 UI>
<p align="center"><img src="/img/Screenshots/main.PNG" width="700px" height="450px"></>
<p align="center"><img src="/img/Screenshots/result.PNG" width="700px" height="450px"></>
  
-------------------------------
### [검색 기능 1 : 키워드로 검색]

- 숙박 유형 선택
- 검색할 키워드를 입력한 후 추천 버튼 클릭
- keyword 부분에는 검색한 키워드와 유사한 세 단어를 출력해주고, 이와 유사한 단어를 포함하는 숙박 시설 3곳을 추천 목록에 출력
- 추천 목록 아래 부분에는 가장 많이 포함하는 장점과 단점 키워드를 세 단어씩 출력

-------------------------------
### [검색 기능 2 : 숙박 시설 명으로 검색]

- 자동 완성 기능으로 정확한 숙박 시설 명을 입력한 후 추천 버튼 클릭
- 입력한 숙박 시설과 가장 비슷한 리뷰를 가진 3곳을 추천
- 각 호텔명 하단에 Click 버튼을 누르면 해당 호텔의 정보를 확인할 수 있는 창 출력
<p align="center"><img src="/img/Screenshots/info.PNG" width="600px" height="550px"></>

### [호텔 정보 출력 창 기능]

- 숙박 시설명, 숙박 유형, 주소, 이미지, 숙박 시설 정보 출력
- 하단에 url 을 클릭하면 해당 숙박 시설의 네이버 호텔 사이트로 이동
- 확인 버튼을 누르면 창 닫기


## 프로젝트 진행 과정
### 1. 데이터 수집
- **Selenium** 을 사용하여 **'네이버 호텔 사이트'** 크롤링

  > - 서울 지역
  > - 평점 6점 이상
  > - 호텔, 호스텔, 게스트 하우스, 모텔
  > - 부킹 닷컴 이용 후기

### 2. 자연어 처리

- **Okt** 를 사용하여 토큰화
- 불용어(stopword) 처리
- 처리 된 데이터들을 한 줄로 구성

### 3. 모델 생성 및 학습

- **Gensim** 패키지를 통한 Word2Vec
- Embedding Model 생성
- 단어들의 유사도 분석

### 4. GUI 구현

## 
