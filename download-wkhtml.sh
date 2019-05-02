#!/bin/bash

set -eo pipefail


mkdir -p var/wkhtmltopdf/bin
cd var/wkhtmltopdf/bin
wget https://github.com/h4cc/wkhtmltopdf-amd64/blob/master/bin/wkhtmltopdf-amd64?raw=true -O wkhtmltopdf
chmod +x wkhtmltopdf
