#!/usr/bin/env python
#coding: utf-8

import os
import dotenv

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from flask import Flask
app = Flask(__name__)

import tinymdblog.routes
