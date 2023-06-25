# Kamakiri

## 概要

ShangriLa Anime APIからアニメ公式サイトのURLリストを取得し、サイトのメタ情報、keywordsやOGP(Open Graph protocol)をクロールしてくるツールです

デフォルトではCSVファイル(UFT-8)に情報を保存します。


## ローカルPyhon3での実行 (非Docker実行)

### 事前準備 [pipenvインストール]

パッケージ管理にpipenvを使用しています

```
pip3 install pipenv
```

### モジュールインストール

※VSCodeで開発する場合は予め下記を.zshrc等に記載

```
export PIPENV_VENV_IN_PROJECT=true
```

```
pipenv install
```

### DB(MySQL)を使用する場合

以下から「site_meta_data」「site_meta_data_histories」テーブルのDDLを実行してください

https://github.com/Project-ShangriLa/anime_master_db_ddl

接続先は環境変数で設定します

```
export ANIME_API_DB_HOST="localhost"
export ANIME_API_DB_USER="root"
export ANIME_API_DB_PASS=""
export ANIME_API_DB_DATABASE="anime_admin_development"
```

### 使い方

まず最初にpipenvでpyenv環境に入る

```
pipenv shell
```

2016年秋期(4期)のアニメサイトのメタ情報を取得

```
python3 kamakiri.py -y 2016 -c 4
```

※csv_outフォルダにCSV出力

2016年秋期(4期)のアニメサイトのメタ情報を取得 (og_image画像を保存)

```
python3 kamakiri.py -y 2016 -c 4 -s
```

※og_imageフォルダに画像出力

2016年秋期(4期)のアニメサイトのメタ情報を取得 (DB保存)

```
python3 kamakiri.py -y 2016 -c 4 -r
```

特定の作品IDのみ指定

```
python3 kamakiri.py -y 2023 -c 4 -i 1802 -s 
```

```
python3 kamakiri.py -y 2023 -c 4 -i 1802 -r 
```


## Dockerでの実行

### docker イメージ ビルド

```
docker build -t kamakiri .
```

### docker コンテナ実行 [CSV保存]

```
docker run --rm -v $(pwd)/csv_out:/usr/src/app/csv_out -i kamakiri python kamakiri.py -y 2021 -c 4
```

### docker コンテナ実行 [画像保存]

```
docker run --rm -v $(pwd)/og_image:/usr/src/app/og_image -i kamakiri python kamakiri.py -y 2021 -c 4 -s 
```

### docker コンテナ実行 [DB保存]

```
docker run --rm -e ANIME_API_DB_HOST="docker.for.mac.localhost" -e ANIME_API_DB_USER="root" -e ANIME_API_DB_PASS="" -i kamakiri python kamakiri.py -y 2021 -c 4 -r
```