# django && djangorestframework

목표는 지금 데모 페이지를 flask -> django imigration

## official tutorial

### app: quickstart

 `./tutorial`

http://www.django-rest-framework.org/tutorial/quickstart/

----

### Serialization : snippets

#### <a href=http://whatisthenext.tistory.com/126> serialize를 하는 이유 </a>

직렬화를 왜 하냐고 물어본다면 다른 환경과 데이터를 주고 받으려면 동일한 데이터 구조를 가져야 하기 때문이다.
제각기 다른 언어를 사용한다면 데이터 송신이 이루어질 수 없다.

> 따라서, 파이썬만 직렬화를 하는 것이 아니다. C, Java, PHP, R 여러 언어들이 직렬화를 지원한다.

시리얼라이즈는 마치 줄줄이 소시지처럼 통일된 데이터를 전송가능한 형태로(`데이터 스트림`) 만드는 것이라고 생각하면 된다.

> 일련의 바이트로부터 데이터 구조를 추출하는 것이 `반직렬화(deserialization)`한다.

파이썬에서 직렬화를 담당하는 클래스가 바로 `Serializer`이다.

```bash
# We'll also need to create an initial migration for our snippet model, and sync the database for the first time.
python manage.py makemigrations snippets # db.sqlite3 생성
python manage.py migrate # 스키마 생성
```

#### using ModelSerializers :  `serializers.Serializer -> ModelSerializers`

app 안에서 urls 설정 -> project 단에서 urls wrapping 해줘야 함. => 여러 app을 한번에 커버하기 좋아보임.

#### serialize + quickstart : 일단 보류

----

### [Tutorial 2: Requests and Responses](http://www.django-rest-framework.org/tutorial/2-requests-and-responses/#tutorial-2-requests-and-responses)

`Status codes`

```markdown
Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if you get an error code wrong. REST framework provides more explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST in the status module. It's a good idea to use these throughout rather than using numeric identifiers.
```

change `JSONResponse, JSONParser -> Response`

----

### [Tutorial 3: Class-based Views](http://www.django-rest-framework.org/tutorial/3-class-based-views/#tutorial-3-class-based-views)

keep our code [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself). : 좋구나

class로 만들면서 코드 가독성도 높이고, 확장성도 가져옴

#### Using mixins  `basic building blocks for generic class based views`

어떤 백엔드 api든 CRUD는 공통적으로 쓰인다. 그래서 mixins 안에 정의되어있다.

`Response, status` 등의 객체를 모두 `mixins, generics` class로 대체함

근데 이건 너무 컨트롤하기 쉽지 않아보인다. 숨겨져 있는게 너무 많음.

내가 웹 프로토콜에 대한 이해가 부족해서 그런가?

#### Using generic class-based views

더 심해짐 아예 메소드가 사라짐

---

### [Tutorial 4: Authentication & Permissions](http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#tutorial-4-authentication-permissions)

여기서부터는 필요할 때 읽는 걸로 함

---

### /hello : return {hello:world}

1. 해보자으

mixins -> generics 점점 큰 wrapper를 쓸 수록 자유도가 떨어지는걸 체감

반드시 디비를 거쳐야 데이터를 만들 수 있음.

서비스단에서는 중요할 듯.

----

### demo imigration : flask to django

#### demo + db 그냥 쌓아만 보자

일단 naver.pozalabs.com 으로 public ip
일단 마구잡이로 기능만 하도록 짜보자
django get으로 들어오는 request가? object

#### start project and app via django

```bash
django-admin.py startproject demo
cd demo
python manage.py startapp musicus
```

#### cross domain error @준태

```
Failed to load resource: Cross-origin redirection to http://naver.pozalabs.com:5000/song/ denied by Cross-Origin Resource Sharing policy: Origin http://demo.pozalabs.com is not allowed by Access-Control-Allow-Origin.
```

#### 그럼 테스트는 demo.pozalabs.com 에서 하는걸루

중요한걸 하나 빼먹었는데..

```
# install konlpy
pip install konlpy
pip install jpype1
# install mecab
```

#### urlpatterns

로 들어오게 하는 건 알았다

그런데 이렇게 보니까 REST 에서는 뒤 url 패턴으로 보통 값을 넘기지 않는다? 아니지

(pk=pk) 이렇게 인자를 받잖아 ok 알았다. `?P`가 parameter 임을 알려줌 [예시 적힌 블로그](https://simpleisbetterthancomplex.com/references/2016/10/10/url-patterns.html) 

`keyword_input`->`slug` 표준이 있다면 표준을 따르자

돌리는 것 까지 짬. demo.pozalabs.com에서 확인해보기

---

## reference

####<a href=https://www.buzzvil.com/ko/2016/12/26/how-to-use-django-rest-framework-buzzvil/> buzzvill 개발기 </a>

--------



-------

#### <a href=http://lunadev.tistory.com/category/%EA%B0%9C%EB%B0%9C/Django%20Restful%20Framework%28drf%29>루나데브 drf</a>

-----

####<a href=https://wayhome25.github.io/django/2017/03/20/django-ep6-migrations/>장고 기본들</a>

----

# 번외 : 새로운 프레임웍을 배울 때

1. awesome-{} 를 찾아본다.
2. 

###