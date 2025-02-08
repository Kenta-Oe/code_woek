import os
import json
from pathlib import Path

def load_script(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_script(script):
    # サンプル処理ロジック
    print(f"Processing script: {script['title']}")
    for item in script['script']:
        print(f"- Text: {item['text']}")
        print(f"  Speed: {item['speed']}")

def main():
    script_path = Path('json_script/sample_script.json')
    if not script_path.exists():
        print(f"Error: Script file not found at {script_path}")
        return
    
    script = load_script(script_path)
    process_script(script)

if __name__ == "__main__":
    main()