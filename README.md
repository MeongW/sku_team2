# sku_team2
sku_team2

### 미디어, 정적 파일 폴더 생성
Add Folder media, static, log


### 로그 기록용 파일 생성
Add File log/django.log


### secrets.json파일 생성
Add File secrets.json
{ 
    "SECRET_KEY": "YOUR KEY",
    "KAKAO_REST_API_KEY": "YOUR KAKAO REST API KEY",
    "KAKAO_CLIENT_ID": "YOUR KAKAO CLIENT ID KEY",
    "KAKAO_CLIENT_SECRET": "YOUR KAKAO CLIENT SECRET KEY",
    "NAVER_CLIENT_ID": "YOUR NAVER CLIENT ID KEY",
    "NAVER_CLIENT_SECRET": "YOUR NAVER CLIENT SECRET KEY",
    "SMS_NAVER_ACCESS_KEY_ID": "YOUR SMS NAVER ACCESS KEY",
    "SMS_NAVER_SECRET_KEY": "YOUR SMS NAVER SECRET KEY",
    "SMS_NAVER_SERVICE_ID": "YOUR SMS NAVER SERVICE ID",
    "SEND_PHONE_NUMBER": "YOUR PHONE NUMBER",
    "EMAIL_HOST_USER": "YOUR EMAIL ADDRESS",
    "EMAIL_HOST_PASSWORD": "YOUR EMAIL ADDRESS PASSWORD"
}


### 익스텐션 추가 (해당 프로젝트 기준 3환경 모두 같은 내용)

- 로컬 환경
pip install -r .\requirements\local.txt

- 개발 환경
pip install -r .\requirements\development.txt

- 운영 환경
pip install -r .\requirements\production.txt


### 마이그레이션
python manage.py makemigrations

python manage.py migrate

### 서버 실행
- 로컬 환경
python manage.py runserver --settings=config.settings.local

- 개발 환경
python manage.py runserver --settings=config.settings.development

- 운영 환경
python manage.py runserver --settings=config.settings.production
