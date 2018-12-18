import csv

from django.core.management.base import BaseCommand
from api.models import Category


class Command(BaseCommand):
    help = 'Import branding theme IDs from Xero'

    def handle(self, *args, **options):
        with open('csv/categories.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    Category.objects.create(
                        id=row.get('Id').strip(),
                        name=row.get('Name').strip(),
                        path=row.get('Path').strip(),
                        parent_id=row.get('ParentID_Fk').strip()
                    )
                except Exception as e:
                    print(str(e))
