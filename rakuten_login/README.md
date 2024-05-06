# 日本語版README

## 概要
このPythonスクリプトは、特定のデータを既存のExcelファイルに追記します。スクリプトは`openpyxl`ライブラリを使用してExcelファイルを操作します。

## 前提条件
- Python 3.6以上がインストールされていること。
- `openpyxl` ライブラリがインストールされています。まだの場合は、以下のコマンドを実行してください。
```bash
  pip install openpyxl
```

## 使用方法
write_to_excel 関数に、書き込みたいデータとExcelファイルのパスを指定します。
スクリプトを実行すると、指定されたファイルにデータが追記されます。ファイルが存在しない場合は新しいファイルが作成されます。

## スクリプトの実行
スクリプトを実行するには、次のコマンドを使用します。
```bash
python your_script.py
```
your_script.py はこのPythonスクリプトのファイル名に置き換えてください。



# English Version README

## Overview
This Python script appends specific data to an existing Excel file using the openpyxl library to manipulate Excel files.

## Prerequisites
Python 3.6 or higher must be installed.
The openpyxl library must be installed. If it is not yet installed, run the following command:
```bash
pip install openpyxl
```

## How to Use
Specify the data you want to write and the path to the Excel file in the write_to_excel function.
Run the script, and the data will be appended to the specified file. If the file does not exist, a new file will be created.

## Running the Script
To run the script, use the following command:
```bash
python your_script.py
```
Replace your_script.py with the filename of this Python script.