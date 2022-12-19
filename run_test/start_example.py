import subprocess
import glob
import yaml
import os
import numpy as np
from typing import Dict, Any
from pathlib import Path
from argparse import ArgumentParser


def load_config(config_path: Path) -> Dict:
    with open(config_path, "r") as f:
        cfg: Dict = yaml.safe_load(f)
    return cfg


def save_config(cfg: Dict, config_path: Path) -> None:
    with open(config_path, "w") as f:
        yaml.safe_dump(cfg, f)


def main():
    parser = ArgumentParser()
    parser.add_argument("--submit-dir", default="./submit", type=str)
    parser.add_argument("--trial-number", default=2, type=int)
    parser.add_argument("--time-out", default=180, type=int)
    args = parser.parse_args()

    # load the configuration file
    master_cfg: Dict[str, Any] = load_config(Path("config.yaml"))

    # set the optimization algorithm
    # samples(implemented in aiaccel):
    # "aiaccel.optimizer.NelderMeadOptimizer"
    # "aiaccel.optimizer.RandomOptimizer"
    # "aiaccel.optimizer.SobolOptimizer"
    # "aiaccel.optimizer.GridOptimizer"
    # "aiaccel.optimizer.TpeOptimizer"
    # your optimizer:
    # "optimizer.MyOptimizer"
    master_cfg: Dict[str, Any] = load_config(Path("config.yaml"))
    master_cfg["optimize"]["search_algorithm"] = "optimizer.MyOptimizer" # set the optimizer
    master_cfg["generic"]["params_path"] = os.path.abspath(f"{args.submit_dir}/model") # user defined param path
 
    # set the number of trials
    master_cfg["optimize"]["trial_number"] = args.trial_number

    save_config(master_cfg, Path("config.yaml"))

    # run the optimization
    results_path = glob.glob("results/*/results.csv")
    num_file_exists = len(results_path)

    command = [
        'bash',
        '-c',
        'aiaccel-start --config config.yaml --clean 1> stdout.txt 2> stderr.txt'
    ]
    process = subprocess.Popen(command)
    try:
        process.wait(timeout=args.time_out)
    except subprocess.TimeoutExpired:
        raise TimeoutError  # タイムアウトエラー

    if process.returncode != 0:
        raise RuntimeError  # 異常終了エラー

    results_path = glob.glob("results/*/results.csv")
    if len(results_path) == num_file_exists:
        raise FileNotFoundError  # results.csvファイルが存在しないエラー

    # 正常の場合の処理

    # データの読み込み
    for result_path in results_path:
        results = np.loadtxt(result_path, skiprows=1, delimiter=",")

        # 最適値の追跡
        current_best = np.inf
        best = []
        for xi in results:
            current_best = min(xi[-1], current_best)
            best.append(current_best)
        best = np.array(best)

        # スコアの計算
        score = best[int(args.trial_number/2):].sum()

        # 結果の表示
        print('\n'+result_path)
        print(f"best objective: {best[-1]}")
        print(f"score:          {score}")


if __name__ == '__main__':
    main()