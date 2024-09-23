# coding-interview

## dockerコンテナを起動
```
docker compose up -d
```

## マイグレーションを実行する
```
docker compose run --rm api python manage.py migrate
```

## 初期データを投入する
```
docker compose run --rm api python manage.py loaddata api_initial.json
```

## Webブラウザ上でapiを確認する
http://localhost:8000/api/

## テストを実行する
```
docker compose run --rm api python manage.py test
```
