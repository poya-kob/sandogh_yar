# utils/dump_models.py

import sys
import os
import django

# تنظیم مسیر پروژه
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_DIR)

# تنظیم فایل تنظیمات Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sandogh_yar.settings')

# راه‌اندازی Django
django.setup()

from django.apps import apps

for model in apps.get_models():
    print(f"\n{model.__module__}.{model.__name__}")
    for field in model._meta.fields:
        print(f"  - {field.name}: {field.get_internal_type()}")
