import json

def create_sample_script():
    script = {
        "title": "サンプルスクリプト",
        "description": "サンプルの説明",
        "reference": "参考資料",
        "script": [
            {
                "text": "サンプルテキスト",
                "speaker": "ナレーター",
                "speed": 1.0
            }
        ]
    }
    return script

def save_script(script, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    sample_script = create_sample_script()
    save_script(sample_script, "sample_output.json")