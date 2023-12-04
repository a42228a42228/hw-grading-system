# Homework Grading System
プログラミング宿題採点用のCLIツール

### 目的
- 個々の宿題を手動コンパイル・テストの手間を減らす
- エラー表示とソースコード表示により柔軟な採点に対応する

### 機能
- Ｃプログラムの自動コンパイル
- Ｃプログラムの自動テスト
- エラー表示
- ソースコードの表示
- 採点記録・出力

## Pre-requisites
- Python >= 3.6
- GNU Compiler (Cプログラムコンパイル用)

## Getting Started

### Installation
リポジトリをクローンしてセットアップする
   ```sh
   git clone https://github.com/a42228a42228/hw-grading-system.git
   cd hw-grading-system
   python setup.py
   ```
   
## Usage
1. 採点したいファイルを `data/` に入れる
2. プログラム実行
   ```sh
   python ./hw-grading-system/hw_grading_system/main.py
   ```
