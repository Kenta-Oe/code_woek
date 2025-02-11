from flask import Flask, render_template, request, flash, redirect, url_for
import subprocess
import os
import json
import logging
from datetime import datetime
import openai
from config import OUTPUT_DIR, JSON_OUTPUT_DIR, LOG_DIR, SECRET_KEY, DEBUG, OPENAI_API_KEY

# Flaskアプリケーションの設定
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG

# ロギングの設定
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'app.log'),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 以下、前回提供したapp.pyの全コンテンツ