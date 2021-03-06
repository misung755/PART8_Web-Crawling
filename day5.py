# 다음 영화 주간 목록 추출하기
from flask import Flask, render_template, request
import re
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta

app = Flask(__name__, template_folder='templates')
app.env = 'development'
app.dabug = True

@app.route('/')
def index():
    return "Welcome, class day 5"


@app.route('/movies', methods=['get', 'post'])
def movies():
    if request.method == "GET":
        return render_template('movies.html')

    def get_movies(week_date=''):
        url = 'https://movie.daum.net/boxoffice/weekly'
        query = {'startDate': week_date}
        res = requests.get(url, params=query)# 나는 클라이언트고 서버한테 ?뒤에 완성해서 보내기(params)
        #https://movie.daum.net/boxoffice/weekly?startDate=2014-02-04
        soup = BeautifulSoup(res.content, 'html.parser')

        movies = [dict(
            title=tag.strong.a.get_text(),
            rating=tag.em.get_text(),
            visitors=re.findall('주간관객 (\d+)명', tag.get_text()),
            opened=re.findall('([0-9\.]+) 개봉', tag.get_text()),
        ) for tag in soup.select('.desc_boxthumb')] # 검사에서 해당 문자열 찾기
        return movies
    
    weeks = request.form.get('weeks')
    weeks = [date.today() - timedelta(weeks=i+1)
        for i in range(int(weeks))]
    movies = [get_movies(w.strftime('%Y%m%d')) for w in weeks]
    #print(movies)
    return render_template('movies.html', soup=movies)


app.run(port=5000)