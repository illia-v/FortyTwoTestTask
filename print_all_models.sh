#!/bin/bash
python manage.py print_all_models 2> "$(date +'%Y-%m-%d')".dat
