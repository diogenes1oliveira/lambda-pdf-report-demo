import datetime
import json
import os
import traceback

from flask import Flask, flash, jsonify, request, redirect, render_template, url_for
from flask_weasyprint import render_pdf, HTML
from flask_wtf import FlaskForm
from jinja2 import Markup
import jsonschema
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()


def include_raw(filename):
    path = os.path.join(app.root_path, filename)
    with open(path) as fp:
        return fp.read()


app.jinja_env.globals['include_raw'] = include_raw


@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


with open('static/schema.json') as fp:
    JSON_SCHEMA = json.load(fp)


def validate_json_values(form, field):
    try:
        data = json.loads(field.data)
        jsonschema.validate(data, schema=JSON_SCHEMA)
    except Exception as e:
        traceback.print_exc()
        raise ValidationError('Malformed JSON') from e


class ReportForm(FlaskForm):
    json_values = StringField('json_values', validators=[validate_json_values])


@app.route('/report.pdf', methods=['POST'])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        variables = json.loads(form.json_values.data)
        html = render_template(
            'report.html', now=datetime.datetime.now(), **variables['values'])
        return render_pdf(HTML(string=html))
    else:
        flash('validation_error', 'error')
        return redirect(url_for('index'))


@app.route('/', methods=['GET'])
def index():
    form = ReportForm()
    return render_template('index.html', form=form)
