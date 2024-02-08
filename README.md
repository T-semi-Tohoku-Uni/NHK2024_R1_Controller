# NHK2024_R1_Controller
R1のコントローラ用のプログラム

## 実行方法
リポジトリをcloneして, ディレクトリを移動
```
git clone git@github.com:T-semi-Tohoku-Uni/NHK2024_R1_Controller.git
cd NHK2024_R1_Controller
```

まずは`python`がインストールされているかを確認（`python3.`がインストールされていればOK）
```
$ python -V
Python 3.11.2
```

venvで仮想環境（ライブラリのバージョンがコンフリクトしないため）を立てる（ローカルに`pip install`するのは非推奨にいつの間にかなったらしい）
```
$ python3 -m venv env
```
仮想環境をactivateする
```
$ . env/bin/activate
```
指定されたライブラリ群をインストールする（すでに`requirements.txt`）で定義ずみ. 新しい環境をインストールした場合は後に説明する手順に従って, 更新された`requirements.txt`をgithubにあげる.
```
$ pip install -r requirements.txt
```

これで環境のセットアップが完成したので, プログラムを実行する
```
$ python3 main.py
```

仮想環境を閉じるときは, 次のコマンドを実行
```
$ deactivate
```

## 新しいパッケージをインストールした場合
`requirements.txt`を更新してgithubを更新する.
まず, `requirements.txt`を更新する
```
$ pip freeze > requirements.txt
```
あとはgithubにpushしてOK