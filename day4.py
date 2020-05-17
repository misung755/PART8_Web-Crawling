from flask import Flask, render_template, request
from konlpy.tag import Kkma
import requests
import re

app = Flask(__name__, template_folder='templates')
app.env = "development"
app.debug = True
kkma = Kkma()


@app.route('/')
def index():
    # index.html 불러오는 Flask 함수
    return render_template('index.html', message = "my message")

# 영어/한글 단어 카운트하기
@app.route('/wordcount/<lang>', methods = ['get','post'])
def wordcount(lang):
    words = [] # 선언 안하면 입력값 없을 때 에러남
    if request.method == 'POST':
        if lang == 'en':
            # 영어 문자열 전처리
            words = request.form.get('lyrics').strip().lower()
            words = words.replace('\n', ' ')
            specials = set(words) - set('abcdefghijklmnopqrstuvwxyz ') # 특수문자들
            for s in specials:
                words = words.replace(s,'')

            # 영어 단어 카운트
            words = words.split(' ')
            words = [(w, words.count(w)) for w in set(words)]
            # 정렬하기(정렬은 리스트 형식만 가능)
            words = sorted(words, key= lambda x :x[1], reverse=True)
        else:
            # 한글 단어 카운트
            words = request.form.get('lyrics').strip()
            words = kkma.pos(words) # nouns는 중복 제거
            words = [w for w in words if w[1] in ['NNG', 'NNP']] # 명사만 추출

            words = [(w, words.count(w)) for w in set(words)]
            # 정렬하기(정렬하려면 리스트형식만 가능)
            words = sorted(words, key = lambda x: x[1], reverse=True)

    return render_template('word_count.html', words=words, lang=lang)

# 정규식 활용해서 URL 추출하기
@app.route('/requests', methods=['get', 'post'])
def req():
    links = []
    if request.method == 'POST':
        url = request.form.get('url')
        res = requests.get(url) #크롤링

        #url을 추출하세요.(http://info.cern.ch/)
        regex = re.compile('href=["\']([^"\']+)["\']')
        links = regex.findall(res.text)

    return render_template("requests.html", links=links)

app.run()