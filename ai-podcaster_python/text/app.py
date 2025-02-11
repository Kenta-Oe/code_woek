import os
import logging
import json
import datetime
import subprocess
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import requests
import openai
from bs4 import BeautifulSoup
from config import OPENAI_API_KEY, MODEL_NAME, OUTPUT_PATH, SECRET_KEY, DEBUG, LOG_FILE, MP3_SCRIPT_PATH

# OpenAI API キー設定
openai.api_key = OPENAI_API_KEY

# ログ設定
log_dir = os.path.dirname(LOG_FILE)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["DEBUG"] = DEBUG