import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from werkzeug.utils import secure_filename
import git
from git import Repo
import pygments
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import HtmlFormatter
import datetime
import tempfile
import time
import markdown
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Markdownフィルターの追加
@app.template_filter('markdown')
def render_markdown(text):
    return markdown.markdown(text, extensions=['fenced_code', 'tables'])

# 保存先のベースディレクトリ設定
REPO_BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repositories')
if not os.path.exists(REPO_BASE_DIR):
    os.makedirs(REPO_BASE_DIR)

# ユーザー管理（簡易版）
USERS = {
    'admin': {'password': 'admin', 'email': 'admin@example.com'}
}

###################
# Helper Functions #
###################

def get_repo_list():
    """リポジトリの一覧を取得する"""
    repos = []
    if os.path.exists(REPO_BASE_DIR):
        for repo_name in os.listdir(REPO_BASE_DIR):
            repo_path = os.path.join(REPO_BASE_DIR, repo_name)
            if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
                try:
                    repo = Repo(repo_path)
                    last_commit = None
                    if len(list(repo.iter_commits())) > 0:
                        last_commit = next(repo.iter_commits())
                        commit_time = datetime.datetime.fromtimestamp(last_commit.committed_date)
                        last_update = commit_time.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        last_update = 'No commits yet'
                    
                    repos.append({
                        'name': repo_name,
                        'path': repo_path,
                        'last_update': last_update
                    })
                except Exception as e:
                    print(f"Error accessing repo {repo_name}: {e}")
    return repos

def get_file_content(repo_path, file_path, branch='master'):
    """ファイルの内容を取得する"""
    repo = Repo(repo_path)
    try:
        # 指定されたブランチの最新コミットからファイルを取得
        commit = repo.commit(branch)
        blob = commit.tree / file_path
        content = blob.data_stream.read().decode('utf-8')
        return content
    except Exception as e:
        return f"Error: {str(e)}"

def get_file_history(repo_path, file_path):
    """ファイルの変更履歴を取得する"""
    repo = Repo(repo_path)
    history = []
    for commit in repo.iter_commits(paths=file_path):
        history.append({
            'hash': commit.hexsha,
            'author': commit.author.name,
            'date': datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S'),
            'message': commit.message
        })
    return history

def get_repo_structure(repo_path, branch='master'):
    """リポジトリの構造（フォルダとファイル）を取得する"""
    repo = Repo(repo_path)
    commit = repo.commit(branch)
    
    def traverse_tree(tree, path=''):
        result = []
        for item in tree.traverse():
            if item.type == 'tree':  # ディレクトリ
                item_path = os.path.join(path, item.path) if path else item.path
                result.append({
                    'type': 'folder',
                    'name': item.path,
                    'path': item_path
                })
            elif item.type == 'blob':  # ファイル
                item_path = os.path.join(path, item.path) if path else item.path
                result.append({
                    'type': 'file',
                    'name': item.path,
                    'path': item_path
                })
        return result
    
    structure = traverse_tree(commit.tree)
    return structure

def highlight_code(filename, content):
    """コードをシンタックスハイライトする"""
    try:
        lexer = get_lexer_for_filename(filename)
    except:
        lexer = TextLexer()
    formatter = HtmlFormatter(linenos=True, cssclass="source")
    highlighted = highlight(content, lexer, formatter)
    css = HtmlFormatter().get_style_defs('.source')
    return highlighted, css

###################
# Routes          #
###################

@app.route('/')
def index():
    """ホームページ - リポジトリ一覧を表示"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repos = get_repo_list()
    return render_template('index.html', repos=repos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン処理"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            flash('ログインしました。', 'success')
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが間違っています。', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """ログアウト処理"""
    session.pop('username', None)
    flash('ログアウトしました。', 'success')
    return redirect(url_for('login'))

@app.route('/create_repo', methods=['GET', 'POST'])
def create_repo():
    """新しいリポジトリを作成"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        repo_name = request.form['repo_name']
        repo_desc = request.form['repo_description']
        init_readme = 'init_readme' in request.form
        
        # 基本的なバリデーション
        if not repo_name or '/' in repo_name or '\\' in repo_name:
            flash('無効なリポジトリ名です。特殊文字は使用できません。', 'danger')
            return redirect(url_for('create_repo'))
        
        repo_path = os.path.join(REPO_BASE_DIR, repo_name)
        
        if os.path.exists(repo_path):
            flash('同じ名前のリポジトリが既に存在します。', 'danger')
            return redirect(url_for('create_repo'))
        
        try:
            # リポジトリディレクトリ作成
            os.makedirs(repo_path)
            
            # Gitリポジトリ初期化
            repo = Repo.init(repo_path)
            
            if init_readme:
                # README.mdファイルを作成
                readme_path = os.path.join(repo_path, 'README.md')
                with open(readme_path, 'w') as f:
                    f.write(f"# {repo_name}\n\n{repo_desc}")
                
                # 最初のコミット
                repo.git.add('README.md')
                repo.git.commit('-m', 'Initial commit with README.md')
            
            flash(f'リポジトリ {repo_name} を作成しました。', 'success')
            return redirect(url_for('view_repo', repo_name=repo_name))
        
        except Exception as e:
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            flash(f'リポジトリの作成に失敗しました: {str(e)}', 'danger')
            return redirect(url_for('index'))
    
    return render_template('create_repo.html')

@app.route('/repo/<repo_name>')
def view_repo(repo_name):
    """リポジトリの詳細を表示"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    try:
        repo = Repo(repo_path)
        
        # ブランチ情報
        branches = [b.name for b in repo.branches]
        current_branch = repo.active_branch.name
        
        # コミット履歴
        commits = []
        for commit in repo.iter_commits(max_count=10):
            commits.append({
                'hash': commit.hexsha,
                'short_hash': commit.hexsha[:7],
                'author': commit.author.name,
                'date': datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S'),
                'message': commit.message
            })
        
        # ファイル構造
        structure = get_repo_structure(repo_path, current_branch)
        
        # README.mdの内容を取得
        readme_content = None
        if os.path.exists(os.path.join(repo_path, 'README.md')):
            with open(os.path.join(repo_path, 'README.md'), 'r') as f:
                readme_content = f.read()
        
        return render_template('view_repo.html', 
                              repo_name=repo_name,
                              branches=branches,
                              current_branch=current_branch,
                              commits=commits,
                              structure=structure,
                              readme_content=readme_content)
    
    except Exception as e:
        flash(f'リポジトリ情報の取得に失敗しました: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/repo/<repo_name>/file/<path:file_path>')
def view_file(repo_name, file_path):
    """ファイルの内容を表示"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    try:
        branch = request.args.get('branch', 'master')
        content = get_file_content(repo_path, file_path, branch)
        
        # シンタックスハイライト
        highlighted_code, css = highlight_code(file_path, content)
        
        # ファイル履歴
        history = get_file_history(repo_path, file_path)
        
        return render_template('view_file.html',
                              repo_name=repo_name,
                              file_path=file_path,
                              content=content,
                              highlighted_code=highlighted_code,
                              css=css,
                              history=history,
                              branch=branch)
    
    except Exception as e:
        flash(f'ファイル内容の取得に失敗しました: {str(e)}', 'danger')
        return redirect(url_for('view_repo', repo_name=repo_name))

@app.route('/repo/<repo_name>/upload', methods=['GET', 'POST'])
def upload_file(repo_name):
    """ファイルをアップロード"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがアップロードされていません。', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('ファイルが選択されていません。', 'danger')
            return redirect(request.url)
        
        if file:
            try:
                repo = Repo(repo_path)
                filename = secure_filename(file.filename)
                
                # 保存先パス
                upload_path = request.form.get('path', '')
                full_path = os.path.join(repo_path, upload_path, filename)
                
                # ディレクトリが存在することを確認
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                # ファイル保存
                file.save(full_path)
                
                # コミット
                commit_message = request.form.get('commit_message', f'Upload {filename}')
                repo.git.add(os.path.join(upload_path, filename))
                repo.git.commit('-m', commit_message)
                
                flash(f'ファイル {filename} をアップロードしました。', 'success')
                
                # ファイルパスを生成（upload_pathが空の場合は考慮）
                file_path = os.path.join(upload_path, filename).replace('\\', '/')
                return redirect(url_for('view_file', repo_name=repo_name, file_path=file_path))
            
            except Exception as e:
                flash(f'ファイルのアップロードに失敗しました: {str(e)}', 'danger')
                return redirect(url_for('view_repo', repo_name=repo_name))
    
    # GETリクエストの場合、アップロードフォームを表示
    structure = get_repo_structure(repo_path)
    
    return render_template('upload_file.html', 
                          repo_name=repo_name,
                          structure=structure)

@app.route('/repo/<repo_name>/edit/<path:file_path>', methods=['GET', 'POST'])
def edit_file(repo_name, file_path):
    """ファイルを編集"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    file_full_path = os.path.join(repo_path, file_path)
    
    if request.method == 'POST':
        try:
            repo = Repo(repo_path)
            
            content = request.form['content']
            commit_message = request.form.get('commit_message', f'Update {file_path}')
            
            # ファイル更新
            with open(file_full_path, 'w') as f:
                f.write(content)
            
            # コミット
            repo.git.add(file_path)
            repo.git.commit('-m', commit_message)
            
            flash(f'ファイル {file_path} を更新しました。', 'success')
            return redirect(url_for('view_file', repo_name=repo_name, file_path=file_path))
        
        except Exception as e:
            flash(f'ファイルの更新に失敗しました: {str(e)}', 'danger')
            return redirect(url_for('view_file', repo_name=repo_name, file_path=file_path))
    
    # GETリクエストの場合、編集フォームを表示
    branch = request.args.get('branch', 'master')
    content = get_file_content(repo_path, file_path, branch)
    
    return render_template('edit_file.html',
                          repo_name=repo_name,
                          file_path=file_path,
                          content=content,
                          branch=branch)

@app.route('/repo/<repo_name>/create_file', methods=['GET', 'POST'])
def create_file(repo_name):
    """新しいファイルを作成"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            repo = Repo(repo_path)
            
            file_path = request.form['file_path']
            content = request.form['content']
            commit_message = request.form.get('commit_message', f'Create {file_path}')
            
            # パス検証
            if not file_path or '..' in file_path:
                flash('無効なファイルパスです。', 'danger')
                return redirect(url_for('create_file', repo_name=repo_name))
            
            file_full_path = os.path.join(repo_path, file_path)
            
            # 既存ファイルのチェック
            if os.path.exists(file_full_path):
                flash('同じパスのファイルが既に存在します。', 'danger')
                return redirect(url_for('create_file', repo_name=repo_name))
            
            # ディレクトリが存在することを確認
            os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
            
            # ファイル作成
            with open(file_full_path, 'w') as f:
                f.write(content)
            
            # コミット
            repo.git.add(file_path)
            repo.git.commit('-m', commit_message)
            
            flash(f'ファイル {file_path} を作成しました。', 'success')
            return redirect(url_for('view_file', repo_name=repo_name, file_path=file_path))
        
        except Exception as e:
            flash(f'ファイルの作成に失敗しました: {str(e)}', 'danger')
            return redirect(url_for('view_repo', repo_name=repo_name))
    
    # GETリクエストの場合、作成フォームを表示
    parent_path = request.args.get('path', '')
    
    return render_template('create_file.html',
                          repo_name=repo_name,
                          parent_path=parent_path)

@app.route('/repo/<repo_name>/branches')
def view_branches(repo_name):
    """ブランチ一覧を表示"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    try:
        repo = Repo(repo_path)
        
        branches = []
        for branch in repo.branches:
            try:
                last_commit = next(repo.iter_commits(branch.name, max_count=1))
                branches.append({
                    'name': branch.name,
                    'last_commit': {
                        'hash': last_commit.hexsha[:7],
                        'message': last_commit.message,
                        'author': last_commit.author.name,
                        'date': datetime.datetime.fromtimestamp(last_commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
            except StopIteration:
                # コミットがない場合
                branches.append({
                    'name': branch.name,
                    'last_commit': None
                })
        
        return render_template('branches.html',
                              repo_name=repo_name,
                              branches=branches,
                              current_branch=repo.active_branch.name)
    
    except Exception as e:
        flash(f'ブランチ情報の取得に失敗しました: {str(e)}', 'danger')
        return redirect(url_for('view_repo', repo_name=repo_name))

@app.route('/repo/<repo_name>/create_branch', methods=['GET', 'POST'])
def create_branch(repo_name):
    """新しいブランチを作成"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        try:
            repo = Repo(repo_path)
            
            branch_name = request.form['branch_name']
            source_branch = request.form.get('source_branch', 'master')
            
            # ブランチ作成
            repo.git.checkout(source_branch)
            repo.git.branch(branch_name)
            
            flash(f'ブランチ {branch_name} を作成しました。', 'success')
            return redirect(url_for('view_branches', repo_name=repo_name))
        
        except Exception as e:
            flash(f'ブランチの作成に失敗しました: {str(e)}', 'danger')
            return redirect(url_for('view_branches', repo_name=repo_name))
    
    # GETリクエストの場合、作成フォームを表示
    try:
        repo = Repo(repo_path)
        branches = [b.name for b in repo.branches]
        
        return render_template('create_branch.html',
                              repo_name=repo_name,
                              branches=branches)
    
    except Exception as e:
        flash(f'リポジトリ情報の取得に失敗しました: {str(e)}', 'danger')
        return redirect(url_for('view_repo', repo_name=repo_name))

@app.route('/repo/<repo_name>/checkout/<branch_name>')
def checkout_branch(repo_name, branch_name):
    """ブランチをチェックアウト"""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repo_path = os.path.join(REPO_BASE_DIR, repo_name)
    
    if not os.path.exists(repo_path) or not os.path.isdir(repo_path):
        flash('指定されたリポジトリが見つかりません。', 'danger')
        return redirect(url_for('index'))
    
    try:
        repo = Repo(repo_path)
        
        # ブランチが存在するか確認
        if branch_name not in [b.name for b in repo.branches]:
            flash(f'ブランチ {branch_name} は存在しません。', 'danger')
            return redirect(url_for('view_branches', repo_name=repo_name))
        
        # チェックアウト
        repo.git.checkout(branch_name)
        
        flash(f'ブランチ {branch_name} にチェックアウトしました。', 'success')
        return redirect(url_for('view_repo', repo_name=repo_name))
    
    except Exception as e:
        flash(f'ブランチのチェックアウトに失敗しました: {str(e)}', 'danger')
        return redirect(url_for('view_branches', repo_name=repo_name))
