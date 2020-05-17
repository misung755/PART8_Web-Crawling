# PART8_Web-Crawling by 이숙번 강사님

## Day4.크롤링의 시작 - 2020.05.13
  * 참고 파일(day4.py + templates html + day4_study.ipynb)
  * 학습 목표 : 웹 크롤링을 활용하여 한글 분석기 만들기
  * 학습 내용
    1. 문자열 마스터하기

    2. requests 라이브러리 : http 응답 status code, text, content
      requests 주요 메소드
      * get + query string
        * params : query string을 dic 형태로 넣음
      * json 메소드
      ```
      # 설치
      pip install requests
      ```
      ```
      # 활용
      import requests
      res = requests.get("http://info.cern.ch/")
      res.text
      ```
    3. 정규식 활용하기

      re 주요 메소드
      * match : 문자열 전체가 정규식과 매치되는지 확인
      * search : 정규식과 매치되는 문자열이 있는지 확인
      * findall : 정규식과 매치되는 모든 문자열을 리스트로 반환
      * sub : 패턴을 찾아서 교체함.
      ```
      # 활용
      import re

      regex = re.compile('<a href=\"(.+)\">')
      regex.findall(text)
      ```

        쉬운 예제 : https://regexone.com/

        추천 사이트 : https://regexr.com/

        정규표현식
        ```
        \d	Any Digit
        \D	Any Non-digit character
        .	Any Character
        [abc]	Only a, b, or c
        [^abc]	Not a, b, nor c
        [a-z]	Characters a to z
        [0-9]	Numbers 0 to 9
        \w	Any Alphanumeric character
        \W	Any Non-alphanumeric character
        {m}	m Repetitions
        {m,n}	m to n Repetitions
        *	Zero or more repetitions
        +	One or more repetitions
        ?	Optional character
        \s	Any Whitespace
        \S	Any Non-whitespace character
        ^…$	Starts and ends
        (…)	Capture Group
        (a(bc))	Capture Sub-group
        (abc|def)	Matches abc or def
        ```
    4. 한글 분석기 만들기

        konlpy 알고리즘 : https://konlpy-ko.readthedocs.io/ko/v0.4.3/morph/

        konlpy 주요 메소드
          * sentences : 문장 분리
          * nouns : 단어 분리
          * pos : 품사 분석
        ```
        # 활용
        from konlpy.tag import Kkma
        kkma = Kkma()

        words = kkma.pos(words)
        ```
    5. JSON
      웹에서 주고받는 데이터의 표준

      검사 - copy as cURL -'convert curl to python requests' 툴로 변환

----------------------------------------------------------------------
## Day4. 과제
  * 기본 틀(day4.py + index.html, word_count.html, requests.html)
    ```
    # day4.py
    from flask import Flask, render_template

    app = Flask(__name__, template_folder='templates')
    app.env = "development"
    app.debug = True

    @app.route('/')
    def index():
        #return "welcome, class day 4, yeah"
        return render_template('index.html', message ="my message") #render_template은 html 불러오는 Flask의 함수

    app.run()
    ```
    ```
    # index.html
    <h1>Welcome class day 4</h1>
    <div>with template</div>
    <div>
        {{message}}
    </div>
    ```
    ```
    # word_count.html
    <h1>word count - {{ lang }}</h1>
    <form action="/wordcount/{{ lang }}" method="post">
        <p><textarea name="lyrics" cols="100" rows="10"></textarea></p>
        <p><input type="submit"></p>
    </form>

    <hr>

    <h2>result</h2>
    <ul>
    {% for k, v in words %}
        <li>{{ k }}: {{ v }}</li>
    {% endfor %}
    </ul>
    ```
    ```
    # requests.html
    <h1>link 추출기</h1>
    <form action="/requests" method="post">
        <p><input type="text" name="url" placeholder="url"></p>
        <p><input type="submit"></p>
    </form>

    <hr>

    <ol>
        {% for link in links %}
        <li>{{ link }}</li>
        {% endfor %}
    </ol>
    ```
  * 실전 과제

    미션1. 영문 문장에서 사용된 단어 개수 세기
    미션2. 한글 문장에서 사용된 단어 개수 세기
    미션3. 정규식 활용해서 URL 추출하기
    ```
    #day4.py
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

    ```

-----------------------------------------------------------------------
## Day4. 참고
### konlpy 등 pip 설치 내역 확인하기
```
user@DESKTOP-14530KF MINGW64 ~/Python_test
$ pip list
Package            Version   
------------------ ----------
Flask              1.1.2
idna               2.9
ipykernel          5.2.1
ipython            7.14.0
jedi               0.17.0
Jinja2             2.11.2
jupyter            1.0.0
konlpy             0.5.2

user@DESKTOP-14530KF MINGW64 ~/Python_test
$ pip freeze >> requerements.txt

user@DESKTOP-14530KF MINGW64 ~/Python_test
$ cat requerements.txt    
Flask==1.1.2
...
konlpy==0.5.2

user@DESKTOP-14530KF MINGW64 ~/Python_test
$ pip install -r requerements.txt => 다른 폴더에 똑같이 설치하고 싶을 때
```
### 아나콘다 가상환경에서 VS code 실행시키기
```
(base) PS C:\windows\system32> cd C:\Users\user\Python_test
(base) PS C:\Users\user\Python_test> pwd

Path
----
C:\Users\user\Python_test

(base) PS C:\Users\user\Python_test> code .
```

================================================================
## Day5.크롤링을 좀 더 쉽게 - 2020.05.14
  * 참고 파일(day5.py + templates html + day5_study.ipynb/day5_ex.ipynb)
  * 학습 목표 : 다음 영화 주간 목록 추출하기
  * 학습 내용
    1. BeautifulSoup(bs4) 라이브러리
      BeautifulSoup Parser
      * html.parser : html문서 트리 형태로 구조화
      * parent, child : 원하는 정보에 쉽게 접근
      * css selector : 원하는 정보에 쉽게 접근
      ```
      # 활용
      from bs4 import BeautifulSoup

      soup = BeautifulSoup (response.text, 'html.parser')
      soup = BeautifulSoup(response.content, 'html.parser')

      # a 태그 추출하기
      print(soup.a)

      # a 태그의 text 부분 추출하기
      print(soup.a.get_text())

      # attribute 추출하기(dictionary로 생각하면 됨)
      print(soup.a['href'])
      ```
    2. datetime 라이브러리
    datetime 주요 함수
    * date.today() : 오늘
    * datetime.now() : 현재시간
    * create 함수
    * strftime() : 날짜의 문자열 포맷 출력(%y%m%d%H%M%S %ww%a%A)
    * timedelta() : 시간의 변화

    ```
    # 활용
    from datetime import date, datetime, timedelta
    today = date.today()
    now = datetime.now()
    yesterday = date(2020, 5, 17)
    prev_28 = date.today() - timedelta(days=7*4)
    print(prev_28.strftime('%Y%m%d'))
    ```

---------------------------------------------------------------------
## Day5. 과제
* 기본 틀(day5.py + movies.html)
  ```
  # day5.py
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

  app.run(port=5000)

  ```
  ```
  # movies.html
  <h1>다음 인기 영화 목록 추출</h1>
  <form action ="/movies" method="post">
      <input type="text" name="weeks" placeholder="weeks">
      <input type="submit">
  </form>

  {% for ss in soup %}
  <hr>

  <h3>{{ loop.index }} 주전</h3>
  <div>
      {% for s in ss %}
      <ul>
          <li><strong>{{ loop.index }}위</strong></li>
          <li>제목: {{ s['title'] }}</li>
          <li>평점: {{ s['rating'] }}</li>
          <li>관객수: {{ s['visitors'] }}</li>
          <li>개봉일: {{ s['opened'] }}</li>
      </ul>
      {% endfor %}
  </div>
  {% endfor %}

  ```
    * 실전 과제

    미션1. 다음 영화 주간 목록 추출하기
    ```
    #day5.py
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
    ```
==================================================================
