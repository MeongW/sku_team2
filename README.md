# sku_team2
sku_team2

### 미디어, 정적 파일 폴더 생성
Add Folder media, static, log


### 로그 기록용 파일 생성
Add File log/django.log


### secrets.json파일 생성
Add File secrets.json
{ "SECRET_KEY": "YOUR_SECRET_KEY" }


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
