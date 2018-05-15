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

### [Requests and Responses](http://www.django-rest-framework.org/tutorial/2-requests-and-responses/#tutorial-2-requests-and-responses)

`Status codes`

```markdown
Using numeric HTTP status codes in your views doesn't always make for obvious reading, and it's easy to not notice if you get an error code wrong. REST framework provides more explicit identifiers for each status code, such as HTTP_400_BAD_REQUEST in the status module. It's a good idea to use these throughout rather than using numeric identifiers.
```

change `JSONResponse, JSONParser -> Response`



---

### /hello : return {hello:world}

1. json 리턴

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

