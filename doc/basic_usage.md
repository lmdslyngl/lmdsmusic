
# 使い方

## 1. ダウンロードして適当な場所に展開する
展開すると以下のようなフォルダ構成になっている．

```
- lmdsmusic_distribute
    - data
        - site_template
            - (ファイルが色々入っている)
        - sources
            - (何も入ってない)
        - siteconfig.toml
    - python-3.8.2-embed-amd64
        - (ファイルがいろいろ入ってる)
    - src
        - (ファイルがいろいろ入ってる)
    - generate_site.bat
    - preview_site.bat
```

## 2. ffmpegをダウンロードして配置する
[https://ffmpeg.zeranoe.com/builds/](https://ffmpeg.zeranoe.com/builds/)
からffmpegをダウンロードして，ffmpeg.exeを以下のフォルダにコピーする．

```
- lmdsmusic_distribute
    - src
        - ffmpeg.exe
        ↑このフォルダにffmpeg.exeを配置する
```

## 3. 曲を所定の場所にコピーする
以下のフォルダに，公開したい曲をコピーする．

```
- lmdsmusic_distribute
    - data
        - sources
            - (このフォルダに曲をコピー)
```

## 4. サイトを生成する
以下のバッチファイルを動かす．

```
- lmdsmusic_distribute
    - generate_site.bat
```

## 5. 生成されたサイトのプレビュー
以下のバッチファイルを動かす．

```
- lmdsmusic_distribute
    - preview_site.bat
```

## 6. サイトの公開
生成されたサイトは以下のフォルダに配置される．

```
- lmdsmusic_distribute
    - data
        - site_generated
```

このフォルダ内のファイルをサーバ等にアップロードすることでサイトの公開が可能．
