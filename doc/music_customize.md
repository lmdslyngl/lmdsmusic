
# 各曲のカスタマイズ
各曲のサムネイルや曲名，アーティスト名などをカスタマイズできる．

## 1. 曲のサムネイルとして使用したい画像を所定のフォルダに配置する
以下のフォルダに，使用したい画像ファイルをコピーする．

```
- lmdsmusic_distribute
    - data
        - site_template
            - (このフォルダに画像ファイルをコピー)
```

## 2. 曲リストを編集する
以下の設定ファイルをメモ帳などで開く．

```
- lmdsmusic_distribute
    - data
        - musicinfo_list.toml
```

設定ファイルは以下のように記載されており，必要に応じて変更して保存する．

``` toml
[[musicinfo_list]]
id = "47d741ef1cb6c501f67101addac7bb49"
title = "200320"
artist = ""
album = ""
duration = 66.13820861678005
last_modified = 1584878686.164157
thumbnail = "music-thumbnail.jpg"

[[musicinfo_list]]
id = "bb67ea14bb14613af465599d14a711fa"
title = "BattleTheme7"
artist = ""
album = "OriginalMusic"
duration = 138.2278458049887
last_modified = 1578136555.851
thumbnail = "music-thumbnail.jpg"

# 以下同様なので省略
```

各曲の各項目の意味は以下の通り．

- title: 曲のタイトル
- artist: アーティスト名
- album: アルバム名（ページ内では未使用）
- thumbnail: 曲のサムネイル画像ファイル名

title, artist, albumは，音声ファイルにタグがあれば自動で設定されている．
また，thumbnailはページの設定ファイル内の「default_music_thumbnail」に指定した画像ファイル名が設定されている．

なお，上記に無い項目は手動で変更するとページが正常に動作しなくため，変更してはならない．

## 3. サイトを生成する
以下のバッチファイルを動かす．

```
- lmdsmusic_distribute
    - generate_site.bat
```
