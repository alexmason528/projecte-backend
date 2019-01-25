import json
import csv

from django.core.management.base import BaseCommand
from api.models import Category


class Command(BaseCommand):
    help = 'Populate categories'

    def handle(self, *args, **options):
        with open('csv/categories.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Category.objects.create(
                        id=row.get('id').strip(),
                        name=row.get('name').strip(),
                        slug=row.get('slug').strip(),
                        path=row.get('path').strip(),
                        parent_id=row.get('parent_id').strip(),
                        translation=json.loads(row.get('translation').strip()),
                    )
                except Exception as e:
                    print(str(e))
