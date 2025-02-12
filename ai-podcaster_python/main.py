import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
import random
from dataclasses import dataclass
import os
from dotenv import load_dotenv
from openai import OpenAI
import ffmpeg

# 型定義
def get_random_bgm(bgm_dir: str) -> Optional[str]:
    """BGMフォルダからランダムにBGMファイルを選択
    
    Args:
        bgm_dir (str): BGMフォルダのパス
        
    Returns:
        Optional[str]: 選択されたBGMファイルのパス。BGMが見つからない場合はNone
        
    Raises:
        PermissionError: フォルダへのアクセス権限がない場合
        OSError: ファイルシステム関連のエラーが発生した場合
    """
    try:
        """BGMフォルダからランダムにBGMファイルを選択"""
        bgm_dir = Path(bgm_dir).resolve()  # 絶対パスに変換
        if not bgm_dir.exists():
            bgm_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created BGM directory: {bgm_dir}")
            return None
        
        # 安全なファイル拡張子チェック
        allowed_extensions = {'.mp3', '.wav', '.m4a'}
        bgm_files = [
            f for f in bgm_dir.glob('*.*')
            if f.suffix.lower() in allowed_extensions
            and f.is_file()
            and os.access(f, os.R_OK)  # 読み取り権限チェック
        ]
        
        if not bgm_files:
            print(f"No MP3 files found in BGM directory: {bgm_dir}")
            return None
        
        selected_bgm = random.choice(bgm_files)
        # ファイルサイズチェック（100MB以上は除外）
        if selected_bgm.stat().st_size > 100 * 1024 * 1024:  # 100MB
            print(f"Warning: Selected BGM file is too large: {selected_bgm}")
            return None
            
        print(f"Selected BGM: {selected_bgm}")
        return str(selected_bgm)
        
    except PermissionError as e:
        print(f"Permission error accessing BGM directory: {e}")
        return None
    except OSError as e:
        print(f"OS error handling BGM files: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error in get_random_bgm: {e}")
        return None

@dataclass
class ScriptElement:
    text: str
    speaker: str
    speed: float = 1.0
    filename: Optional[str] = None

@dataclass
class PodcastScript:
    title: str
    description: str
    reference: str
    script: List[ScriptElement]
    filename: Optional[str] = None
    speed: float = 1.0

async def generate_speech(text: str, output_path: str, api_key: str) -> None:
    """OpenAI APIを使用して音声を生成"""
    client = OpenAI(api_key=api_key)
    
    try:
        print(f"Generating speech for text: {text[:50]}...")
        response = client.audio.speech.create(
            model="tts-1",
            voice="shimmer",
            input=text
        )
        
        # 音声ファイルを保存
        output_path = Path(output_path).resolve()  # 絶対パスに変換
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            print(f"Writing response to file: {output_path}")
            f.write(response.content)
        print(f"Generated: {output_path}")
        print(f"File exists: {output_path.exists()}")  # ファイルの存在確認
        print(f"File size: {output_path.stat().st_size} bytes")
        
    except Exception as e:
        print(f"Error generating speech: {e}")
        print(f"Error type: {type(e)}")
        raise

async def combine_audio_files(input_files: List[str], output_file: str, bgm_file: str = None) -> None:
    """音声ファイルを結合してBGMを追加
    
    Args:
        input_files (List[str]): 入力音声ファイルのパスリスト
        output_file (str): 出力ファイルのパス
        bgm_file (str, optional): BGMファイルのパス
        
    Raises:
        FileNotFoundError: 入力ファイルが見つからない場合
        PermissionError: ファイルへのアクセス権限がない場合
        ffmpeg.Error: FFmpegによる処理でエラーが発生した場合
    """
    
    # 入力ファイルの検証
    for input_file in input_files:
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")
        if not os.access(input_file, os.R_OK):
            raise PermissionError(f"No read permission for file: {input_file}")
            
    # 出力ディレクトリの書き込み権限チェック
    output_dir = os.path.dirname(output_file)
    if not os.access(output_dir, os.W_OK):
        raise PermissionError(f"No write permission for directory: {output_dir}")
        
    # BGMファイルの検証
    if bgm_file:
        if not os.path.exists(bgm_file):
            raise FileNotFoundError(f"BGM file not found: {bgm_file}")
        if not os.access(bgm_file, os.R_OK):
            raise PermissionError(f"No read permission for BGM file: {bgm_file}")
    """音声ファイルを結合してBGMを追加"""
    try:
        print(f"Combining audio files: {input_files}")
        # すべての入力ファイルの存在を確認
        for input_file in input_files:
            path = Path(input_file).resolve()
            if not path.exists():
                raise FileNotFoundError(f"Input file not found: {path}")
            print(f"Confirmed input file exists: {path}")

        # 入力ファイルを連結
        concat_list = []
        for i, input_file in enumerate(input_files):
            input_path = Path(input_file).resolve()
            print(f"Processing file {i+1}/{len(input_files)}: {input_path}")
            # 音声ファイル
            stream = ffmpeg.input(str(input_path))
            # 0.5秒の無音を追加（最後のファイル以外）
            if i < len(input_files) - 1:
                silence = ffmpeg.input('anullsrc', f='lavfi', t=0.5)
                concat_list.extend([stream, silence])
            else:
                concat_list.append(stream)

        # 音声を連結
        concat = ffmpeg.concat(*concat_list, v=0, a=1)
        
        # 出力ファイルのパスを絶対パスに変換
        output_path = Path(output_file).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if bgm_file:
            print(f"Adding BGM from: {bgm_file}")
            bgm_path = Path(bgm_file).resolve()
            bgm = ffmpeg.input(str(bgm_path))
            mixed = ffmpeg.filter([concat, bgm], 'amix', inputs=2, duration='first', weights='1 0.2')
            command = ffmpeg.output(mixed, str(output_path)).overwrite_output()
            print(f"FFmpeg command: {' '.join(command.get_args())}")  # コマンドを表示
            command.run(capture_stdout=True, capture_stderr=True)
        else:
            print(f"Creating output without BGM: {output_path}")
            command = ffmpeg.output(concat, str(output_path)).overwrite_output()
            print(f"FFmpeg command: {' '.join(command.get_args())}")  # コマンドを表示
            command.run(capture_stdout=True, capture_stderr=True)
            
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in combine_audio_files: {str(e)}")
        print(f"Error type: {type(e)}")
        raise

def get_latest_json_script(script_dir):
    """指定されたディレクトリ内の最新のJSONスクリプトファイルを取得"""
    script_dir = Path(script_dir)
    json_files = list(script_dir.glob('*.json'))
    
    if not json_files:
        raise FileNotFoundError(f"No JSON script files found in {script_dir}")
    
    # 最新のファイルを更新日時で選択
    latest_script = max(json_files, key=os.path.getmtime)
    print(f"Selected script: {latest_script}")
    return latest_script

async def main():
    # カレントディレクトリをスクリプトのある場所に変更
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    print(f"Working directory: {os.getcwd()}")

    # 環境変数の読み込み
    load_dotenv(dotenv_path='.env')
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        return
    
    # 出力ディレクトリの作成（絶対パス）
    scratchpad_dir = script_dir / "scratchpad"
    output_dir = script_dir / "output"
    scratchpad_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    # 最新のJSONスクリプトを取得
    script_path = get_latest_json_script('json_script')
    script_data = json.loads(script_path.read_text(encoding='utf-8'))
    
    print(f"Loaded script data: {script_data}")
    
    # scriptの各要素をScriptElementに変換
    script_elements = [ScriptElement(**element) for element in script_data['script']]
    script_data['script'] = script_elements
    
    # PodcastScriptオブジェクトの作成
    script = PodcastScript(**script_data)
    script.filename = script_path.stem
    print(f"Created PodcastScript object with filename: {script.filename}")

    # 音声ファイルの生成
    audio_files = []
    for i, element in enumerate(script.script):
        # ここでfilename属性を設定
        element.filename = f"{script.filename}_{i}"
        output_path = scratchpad_dir / f"{element.filename}.mp3"
        
        try:
            await generate_speech(element.text, str(output_path), api_key)
            audio_files.append(str(output_path))
        except Exception as e:
            print(f"Error processing element {i}: {e}")
            return

    print(f"Generated audio files: {audio_files}")

    # 出力ファイル名の設定
    output_file = output_dir / f"{script.filename}_combined.mp3"

    # 音声ファイルの結合とBGMの追加
    try:
        # BGMフォルダからBGMを選択
        bgm_dir = script_dir / "bgm"
        bgm_file = get_random_bgm(str(bgm_dir))

        # 音声ファイルを結合（BGMがある場合は一緒に合成）
        await combine_audio_files(audio_files, str(output_file), bgm_file)
        print(f"Combined audio{' with BGM' if bgm_file else ''} saved to: {output_file}")

        # スクリプト情報の保存
        script_output = output_dir / f"{script.filename}.json"
        script_output.write_text(json.dumps(vars(script), default=vars, indent=2))
        print(f"Script information saved to: {script_output}")
        
    except Exception as e:
        print(f"Error in audio processing: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    asyncio.run(main())