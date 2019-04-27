import datetime
import json

from flask import Flask, jsonify, request, render_template
from flask_weasyprint import render_pdf, HTML
from jsonschema import validate

app = Flask(__name__)


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


with open('static/schema.json') as fp:
    JSON_SCHEMA = json.load(fp)


@app.route('/report.pdf', methods=['POST'])
def report():
    try:
        validate(instance=request.json, schema=JSON_SCHEMA)
        variables = request.json['values']
    except Exception as e:
        return jsonify({'error': e.message}), 400
    else:
        html = render_template(
            'report.html', now=datetime.datetime.now(), **variables)
        return render_pdf(HTML(string=html))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
