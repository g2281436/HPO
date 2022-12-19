# 配布データと応募用ファイル作成方法の説明

本コンペティションで配布されるデータと応募用ファイルの作成方法について説明する.

1. [配布データ](#配布データ)
1. [応募用ファイルの作成方法](#応募用ファイルの作成方法)

## 配布データ

配布されるデータは以下の通り.

- [Readme](#readme)
- [動作確認用のプログラム](#動作確認用のプログラム)
- [応募用サンプルファイル](#応募用サンプルファイル)

### Readme

本ファイル(readme.md)で, 配布用データの説明と応募用ファイルの作成方法を説明したドキュメント. マークダウン形式で, プレビューモードで見ることを推奨する.

### 動作確認用のプログラム

最適化アルゴリズムを開発するための動作確認用プログラム. "run_test.zip"が本体で, 解凍すると, 以下のようなディレクトリ構造のデータが作成される.

```bash
run_test
├── submit                        : 応募用ファイルのベースとなるディレクトリ
│   ├── model
│   └── src
├── config.yaml                   : 最適化実行のための設定ファイル
├── Dockerfile                    : 環境構築に必要なDockerfile
├── example.py                    : 最適化の対象となる関数の実装例
├── requirements.txt              : 環境構築に必要なPythonライブラリ一覧
└── start_example.py              : 最適化を実行するスクリプト
```

使用方法の詳細については[応募用ファイルの作成方法](#応募用ファイルの作成方法)を参照すること.

### 応募用サンプルファイル

応募用のサンプルファイル. 実体は"sample_submit.zip"で, 解凍すると以下のようなディレクトリ構造のデータが作成される.

```bash
sample_submit
├── model
│   └── ...
├── src
│   └── optimizer.py
└── requirements.txt
```

詳細や作成方法については[応募用ファイルの作成方法](#応募用ファイルの作成方法)を参照すること.

## 応募用ファイルの作成方法

パラメータなどを含めた, 最適化を実行するためのソースコード一式をzipファイルでまとめたものとする.

### ディレクトリ構造

以下のようなディレクトリ構造となっていることを想定している.

```bash
.
├── model              必須: 最適化アルゴリズムに渡すパラメータなどを置くディレクトリ
│   └── ...
├── src                必須: Pythonのプログラムを置くディレクトリ
│   ├── optimizer.py   必須: 最初のプログラムが呼び出すファイル
│   └── ...            その他のファイル (ディレクトリ作成可能)
└── requirements.txt   任意: 追加で必要なライブラリ一覧
```

- 最適化アルゴリズムに渡すパラメータの格納場所は"model"ディレクトリを想定している.
  - 使用しない場合でも空のディレクトリを作成する必要がある.
  - 名前は必ず"model"とすること.
- Pythonのプログラムの格納場所は"src"ディレクトリを想定している.
  - 最適化アルゴリズムが実装されたソースコードは"optimizer.py"を想定している.
    - ファイル名は必ず"optimizer.py"とすること.
  - その他予測を実行するために必要なファイルがあれば作成可能である.
  - ディレクトリ名は必ず"src"とすること.
- 実行するために追加で必要なライブラリがあれば, その一覧を"requirements.txt"に記載することで, 評価システム上でも実行可能となる.
  - インストール可能で実行可能かどうか予めローカル環境で試しておくこと.

### optimizer.pyの実装方法

以下のクラスとメソッドを実装すること.

#### MyOptimizer

最適化アルゴリズムが実装されたクラス. 以下のメソッドを実装すること.

##### __init__

インスタンス化する際に最初に呼ばれるメソッド. "config.yaml"で定義される設定に関する情報が渡される. "config.yaml"の('generic', 'params_path')で"model"のパスが定義されているので, そこに格納してあるファイルなどを読み込むことができる. 例えばmodel/test.jsonを読み込みたいときは以下のようにすればよい.

```Python
params_path = self.config.config.get('generic', 'params_path')
with open(os.path.join(params_path, 'test.json')) as f:
  test = json.load(f)
```

##### generate_parameter

次の調整パラメータを返すメソッド. 以下のフォーマットで, *list型*で返す.

```json
[
    {
        "parameter_name": parameter_name,
        "type": type,
        "value": value
    },
    {
        "parameter_name": parameter_name,
        "type": type,
        "value": value
    },
    ...
]
```

"parameter_name"は設定で定義されたパラメータ名, "type"はパラメータの型, "value"は値.

設定されたパラメータに対する目的関数値は以下のようにして得ることができる.

```Python
objective = self.storage.result.get_any_trial_objective(trial_id)
```

`storage`が属性として更新されるので, その`result`に対して`get_any_trial_objective`メソッドに試行ID`trial_id`を渡すことで可能. 対応する試行IDの目的関数値が存在しない場合は`None`を返す.

以下は実装例. 正規分布に従ってサンプリングして, クリッピング処理を行った値を返すものである.

```Python
import json
import numpy as np
from aiaccel.optimizer.abstract_optimizer import AbstractOptimizer


class MyOptimizer(AbstractOptimizer):
    """An optimizer class.

    """
    def __init__(self, options: dict) -> None:
        super().__init__(options)
        param_path = self.config.config.get('generic', 'params_path')
        with open(os.path.join(param_path, 'test.json')) as f:
            test = json.load(f)


    def generate_parameter(self) -> None:
        """Generate parameters.

        Args:
            number (Optional[int]): A number of generating parameters.

        Returns:
            List[Dict[str, Union[str, float, List[float]]]]: A created
            list of parameters.
        """

        new_params = []
        hp_list = self.params.get_parameter_list()

        for hp in hp_list:
            value = np.random.normal(3, 0.1)
            value = min(max(value, hp.lower), hp.upper)
            new_param = {
                'parameter_name': hp.name,
                'type': hp.type,
                'value': value
            }
            new_params.append(new_param)

        return new_params
```

`MyOptimizer`クラスが継承している`AbstractOptimizer`やその派生クラスの実装については, [ここ](https://github.com/aistairc/aiaccel/blob/main/aiaccel/optimizer)を参照すること. また, 実装方法の詳細については[aiaccelの公式ドキュメント](https://aiaccel.readthedocs.io/ja/latest/developer_guide/custom_optimizer.html#)や応募用サンプルファイル"sample_submit.zip"も参照すること.

### 動作テスト

最適化を行うプログラムが実装できたら, 正常に動作するか確認する.

#### 環境構築

まず、自分のOS環境に応じてDockerを導入する. 導入方法については, [こちら](https://docs.docker.com/get-docker/)を参照. Dockerの導入ができたら, run_test.zipを解凍してDockerfileが存在するディレクトリ(そのまま解凍したなら run_test)に移動して, 以下のコマンドを実行する.

```bash
docker build .
...
```

コンテナの立ち上げには時間がかかることに注意. コンテナ環境の中に入ることができたら環境構築は成功である.

```bash
docker run -it IMAGEID
...
```

#### 最適化の実行

最適化アルゴリズムを実装して(run_test/以下で作業してることが前提)最適化を実行し, スコアを確認する. 最初にsubmit/srcのパスを通しておく.

```bash
export PYTHONPATH=$(pwd)/submit/src
python start_example.py  --submit-dir /path/to/submit/ --trial-number trial_number --time-out time_out
...
```

- 引数"--submit-dir"には実装した最適化プログラム("src/optimizer.py")が存在するパス名を指定する.
- 引数"--trial-number"には最適化の試行回数を設定する. デフォルトは2.
- 引数"--time-out"には実行に対するタイムアウト時間を秒で設定する. 指定された時間を過ぎた場合は`TimeOutError`を返す. デフォルトは180秒.

実行中は作業ディレクトリ直下でstdout.txtやstderr.txtが生成され, stdout.txtで標準出力(各試行に対する目的関数値などを含む)が, stderr.txtで実行ログやエラーログが確認できるので, 適宜参照すること. 実行に成功すると, 以下のように最終的に最もよかった目的関数値(best objective)とスコア(score)が表示される. スコアは全試行のうち後半半分の目的関数値の合計である(例えば100回試行した場合は後半50回分の目的関数値の合計). 今回は最小化を目指すため, これらの値は小さいほどよい.

```bash
results/yyyymmdd_hhmmss/results.csv
best objective: 1.636304418956428
score:          209.23429247037726
...
```

`yyyymmdd_hhmmss`は実行した時間帯を表す.

投稿する前にエラーが出ずに実行が成功することを確認すること.

### 応募用ファイルの作成

上記の[ディレクトリ構造](#ディレクトリ構造)となっていることを確認して, zipファイルとして圧縮する.
