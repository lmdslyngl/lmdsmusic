
# ページのカスタマイズ
プロフィール文やプロフィール画像，背景を好きなものに変更できる．

## 1. プロフィール画像や背景画像を所定のフォルダに配置する
以下のフォルダに，ページで使用したい画像ファイルをコピーする．

```
- lmdsmusic_distribute
    - data
        - site_template
            - (このフォルダに画像ファイルをコピー)
```

## 2. ページの設定ファイルを編集する
以下の設定ファイルをメモ帳などで開く．

```
- lmdsmusic_distribute
    - data
        - siteconfig.toml
```

設定ファイルは以下のように記載されており，必要に応じて変更し保存する．

``` toml
# ページタイトル
title = "My awesome musics"

# プロフィールのサムネイル画像ファイル名
profile_thumbnail = "profile-thumbnail.png"

# プロフィールの背景画像ファイル名
profile_background = "profile-background.jpg"

# ユーザ名
username = "My name is ..."

# ユーザ説明
description = "This is description of site."

# ページ下部のコピーライト
copyright = "Copyright 2020 My name."

# デフォルトの曲サムネイル
default_music_thumbnail = "music-thumbnail.jpg"
```

なお，以下の画像ファイル名を記載する項目は，手順1にてフォルダにコピーした画像ファイル名を記入する．

- profile_thumbnail
- profile_background
- default_music_thumbnail

## 3. サイトを生成する
以下のバッチファイルを動かす．

```
- lmdsmusic_distribute
    - generate_site.bat
```

