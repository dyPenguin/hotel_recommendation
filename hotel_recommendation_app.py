import sys
from PyQt5 import uic
from PyQt5.QtCore import QStringListModel
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
from konlpy.tag import Okt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import urllib.request
from PyQt5.QtGui import *
import pandas as pd

form_window = uic.loadUiType('./mainwidget.ui')[0]


# 서브 창
class OptionWindow(QDialog):
    def __init__(self, parent):
        super(OptionWindow, self).__init__(parent)
        self.parent = parent
        # 데이터 LOAD
        self.data = pd.read_csv('./datasets/real_data.csv', index_col=0)
        option_ui = './window.ui'
        uic.loadUi(option_ui, self)
        self.initUI()
        self.exec_()  # MODAL 창으로 실행

    def initUI(self):
        self.setStyleSheet("background-color: #ffffff")
        self.lbl_title.setText(self.parent.name)
        self.lbl_title.adjustSize()

        hotel_title = self.lbl_title.text()
        self.setWindowTitle(hotel_title + ' 정보')

        df_hotel = self.data[self.data['hotel_title'] == hotel_title]
        df_hotel.reset_index(inplace=True, drop=True)

        # 호텔 정보 설정
        self.set_hotelInfo(df_hotel)

        # 호텔 url 설정
        self.set_urlLink(df_hotel)

        # 호텔 이미지 설정
        self.set_imageLoad(df_hotel)

        # 버튼 ok
        self.btn_ok.clicked.connect(self.btn_closeEvent)

    def set_hotelInfo(self, DataFrame):
        self.lbl_type.setText(DataFrame['hotel_type'][0])
        self.lbl_addr.setText(str(DataFrame['hotel_addr'][0]))
        self.lbl_info.setText(DataFrame['hotel_info'][0])

    def set_urlLink(self, DataFrame):
        str_url = str(DataFrame['hotel_url'][0])
        self.lbl_url.setText('<a href="' + str_url + '"target="_blank">' + str_url + '</a>')
        self.lbl_url.setOpenExternalLinks(True)

    def set_imageLoad(self, DataFrame):
        img_url = str(DataFrame['img_url'][0])
        imgFromWeb = urllib.request.urlopen(img_url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(imgFromWeb)
        pixmap = pixmap.scaled(500, 400)
        self.lbl_img.setPixmap(pixmap)

    def btn_closeEvent(self):
        self.close()


# 메인 창
class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()

        # 데이터 LOAD
        self.df_hotel = pd.read_csv('./datasets/real_data.csv', index_col=0)
        self.embedding_model = Word2Vec.load('./model/real_final.model')
        self.vocab = self.embedding_model.wv.vocab

        # 변수명 초기화
        self.type = ''
        self.Tfidf = TfidfVectorizer()
        self.Tfidf_matrix = self.Tfidf.fit_transform(self.df_hotel['good_review'])
        self.msg = QMessageBox()

        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('호텔 인도자')  # 팀명으로 제목 지정

        self.cmb_hotel_type.addItem('숙박 유형 전체')
        self.cmb_hotel_type.addItem('호스텔')
        self.cmb_hotel_type.addItem('호텔')
        self.cmb_hotel_type.addItem('게스트 하우스')
        self.cmb_hotel_type.addItem('모텔')
        self.type = self.cmb_hotel_type.currentText()
        print('타입', self.type)

        self.btn_exec.clicked.connect(self.btn_exec_clicked_slot)
        self.btn_hotel.clicked.connect(self.btn_hotel_clicked_slot)
        self.cmb_hotel_type.currentIndexChanged.connect(self.set_hotel_type)
        self.btn_1.clicked.connect(self.btn_1_clicked)
        self.btn_2.clicked.connect(self.btn_2_clicked)
        self.btn_3.clicked.connect(self.btn_3_clicked)

        # 자동 완성 기능
        title_list = list(self.df_hotel['hotel_title'])
        model = QStringListModel()
        model.setStringList(title_list)
        completer = QCompleter()
        completer.setModel(model)
        self.le_hotel.setCompleter(completer)

    # 호텔 타입 변경
    def set_hotel_type(self):
        self.type = self.cmb_hotel_type.currentText()

    # 호텔 자식 창 연결
    def btn_1_clicked(self):
        try:
            self.dialog_open(self.lbl_hotel_sim_1)
        except:
            return

    def btn_2_clicked(self):
        try:
            self.dialog_open(self.lbl_hotel_sim_2)
        except:
            return

    def btn_3_clicked(self):
        try:
            self.dialog_open(self.lbl_hotel_sim_3)
        except:
            return

    # 호텔명으로 찾는 함수
    def btn_exec_clicked_slot(self):
        title = self.le_hotel.text()
        try:
            hotel_idx = self.df_hotel[self.df_hotel['hotel_title'] == title].index[0]  # hotel명의 인덱스를 알려주는 모드
            # print(hotel_idx)
        except:
            if IndexError:
                self.le_hotel.setText('')
                self.msg.warning(self, '호텔명 입력 오류', '호텔명을 정확하게 입력해 주세요.')

                return

        cosine_sim = linear_kernel(self.Tfidf_matrix[hotel_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)[0:3]
        self.lbl_hotel_sim_1.setText('\n'.join(list(recommendation[0:1])))
        self.lbl_hotel_sim_2.setText('\n'.join(list(recommendation[1:2])))
        self.lbl_hotel_sim_3.setText('\n'.join(list(recommendation[2:3])))

    # 추천 서비스
    def getRecommendation(self, cosine_sim):
        simScores = list(enumerate(cosine_sim[-1]))
        simScores = sorted(simScores, key=lambda x: x[1], reverse=True)  # x: x[1]은 코사인 세타 값을 보겠다는 소리다.
        simScores = simScores[1:40]  # 0번은 자기자신이 나옴
        idx = [i[0] for i in simScores]
        RecMovielist = self.df_hotel.iloc[idx]

        if self.type == '숙박 유형 전체':
            typelist = RecMovielist
        else:
            typelist = RecMovielist[RecMovielist['hotel_type'] == self.type]

        return typelist.hotel_title

    # 단어로 찾는 서비스
    def btn_hotel_clicked_slot(self):
        str_word = self.le_word.text()
        print(str_word)
        hotel_list = []

        # '청결'
        if str_word in self.vocab:
            sim_words = self.embedding_model.wv.most_similar(str_word, topn=10)
            """
            입력값을 첫번째 띄어쓰기로 줌. 입력된 '겨울'과 유사한 '여름','가을'들이 나옴.
            비슷한 단어 (겨울,0.9999)
            """
            word_list = [str_word]
            for sim_word, _ in sim_words:
                word_list.append(sim_word)  # 입력단어, 유사단어를 리스트화 함. 가중치를 더함.

            keyword_list = []
            for i in range(0, 10):
                keyword_list = keyword_list + ([word_list[i]] * (10 - i))
        else:
            self.le_word.setText('')
            self.msg.warning(self, '단어 입력 오류', '다른 단어를 입력해 주세요.')

            return

        try:
            keyword_vec = self.Tfidf.transform(keyword_list)  # 겨울겨울겨울...가을가을가을......계절...
            # print(keyword_vec)
            cosine_sim = linear_kernel(keyword_vec, self.Tfidf_matrix)

            # 추천 숙박시설 목록 :  1순위 2순위 3순위
            recommendation = self.getRecommendation(cosine_sim)[0:3]
            self.lbl_first_hotel_list.setText('\n'.join(list(recommendation[0:1])))
            hotel_list.append(self.lbl_first_hotel_list.text())
            self.lbl_second_hotel_list.setText('\n'.join(list(recommendation[1:2])))
            hotel_list.append(self.lbl_second_hotel_list.text())
            self.lbl_third_hotel_list.setText('\n'.join(list(recommendation[2:3])))
            hotel_list.append(self.lbl_third_hotel_list.text())

            in_text = str(word_list[0]) + ', ' + str(word_list[1]) + ', ' + str(word_list[2])
            # print(in_text)
            self.lbl_key_word.setText(in_text)
        except Exception as e:
            print(e)
            print('키워드 추천 Error')

        # print(hotel_list, '확인')
        self.keyword_recommendation(hotel_list)
        print('검색 완료')

    # 키워드 추천
    def keyword_recommendation(self, hotel_list):
        good_list = []
        bad_list = []
        okt = Okt()

        try:
            for i in range(len(hotel_list)):
                if hotel_list[i] == '':
                    good_list.append('')
                    bad_list.append('')
                    continue

                idx = self.df_hotel[self.df_hotel['hotel_title'] == hotel_list[i]].index[0]
                good_token = okt.pos(self.df_hotel['good_review'][idx], norm=True, stem=True)
                good_token = pd.DataFrame(good_token, columns=['word', 'class'])
                cleaned_good_token = good_token[good_token['class'] == 'Noun']
                good = cleaned_good_token.word.value_counts()
                good = pd.DataFrame(good)
                good.reset_index(inplace=True)
                good = list(good['index'][0:4])
                vocabs = str(good[0]) + ', ' + str(good[1]) + ', ' + str(good[2])
                good_list.append(vocabs)
                # print('good_list', good_list)

                bad_token = okt.pos(self.df_hotel['bad_review'][idx], norm=True, stem=True)
                bad_token = pd.DataFrame(bad_token, columns=['word', 'class'])
                cleaned_bad_token = bad_token[bad_token['class'] == 'Noun']
                bad = cleaned_bad_token.word.value_counts()
                bad = pd.DataFrame(bad)
                bad.reset_index(inplace=True)
                bad = list(bad['index'][0:4])
                bad_vocabs = str(bad[0]) + ', ' + str(bad[1]) + ', ' + str(bad[2])
                bad_list.append(bad_vocabs)
                # print('bad_list', bad_list)

            self.lbl_first_good.setText(good_list[0])
            self.lbl_second_good.setText(good_list[1])
            self.lbl_third_good.setText(good_list[2])

            self.lbl_first_bad.setText(bad_list[0])
            self.lbl_second_bad.setText(bad_list[1])
            self.lbl_third_bad.setText(bad_list[2])

            # 추천 호텔이 없을 경우
            if hotel_list == ['', '', '']:
                self.msg.information(self, '', '추천 목록이 없습니다.')
        except Exception as e:
            print(e)

    def lbl_clean(self, *lblNames):
        for lblName in lblNames:
            lblName.setText('')
        # print('lbl_clean OK')

    # 자식창 여는 함수
    def dialog_open(self, lblName):
        self.name = lblName.text()
        OptionWindow(self)

    # 창 닫기
    def closeEvent(self, QCloseEvent):
        ans = QMessageBox.question(self, '종료하기', '종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.Yes)
        if ans == QMessageBox.Yes:
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()


app = QApplication(sys.argv)
mainWindow = Exam()
mainWindow.show()
sys.exit(app.exec_())
