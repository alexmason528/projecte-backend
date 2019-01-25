import random
from slugify import slugify

from django.core.management.base import BaseCommand
from api.models import *


class Command(BaseCommand):
    help = 'Import branding theme IDs from Xero'

    def handle(self, *args, **options):
        estate_names = ['Ranch with lake', 'Row house', 'Wood house', 'Farm house']

        details = 'Versteckt am Rande einer kleinen Siedlung verbirgt sich dieses exklusive Anwesen und schützt Bewohner vor allzu neugierigen Blicken. Ca. 25 km von der Wiener Stadtgrenze entfernt erschließt sich die einzigartige Natur des Wienerwaldes - weit und breit stört kein Gebäude diesen herrlichen Blick in die wunderbare und sanft hügelige Umgebung.\
        In absolut einzigartiger und erhöhter Lage können sie ungestört ihr Familienleben genießen, ihrer Arbeit nachgehen und ihre Freizeit und Hobbies genießen.\
        Das Haupthaus empfängt Sie freundlich, eine Überraschung offenbart sich bei jedem Schritt durch das Haus! Ein Hochgenuss für jeden, der das Besondere zu schätzen mag. Da die Besitzerfamilie sehr viel Wert auf Privatsphäre legt, wohnen Gäste im unweit gelegenen Gästehaus.\
        Ganz besonders interessant ist diese Liegenschaft für ambitionierte Pferdesportler - die komplette Infrastruktur für Reiter und Pferd - Stallungen mit Paddockboxen, eine Pferdeführanlage und natürlich ein Reitplatz sind vorhanden.\
        Ganz besonders interessant ist diese Liegenschaft für ambitionierte Pferdesportler - die komplette Infrastruktur für Reiter und Pferd - Stallungen mit Paddockboxen, eine Pferdeführanlage und natürlich ein Reitplatz sind vorhanden.'

        comment = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum'

        facts = {
            'living_space': 2000,
            'years_of_cons': 1999,
            'building_area': 15,
            'condition': 'Ready to use'
        }

        for i in range(1, 51):
            item = Item.objects.create(name='{} {}'.format(estate_names[random.randrange(
                0, len(estate_names)-1)], i), facts=facts, details=details, category_id=random.randrange(10, 13), user_id=1)
            item.slug = slugify('{}-{}'.format(item.name, item.id))
            item.save()

        for i in range(1, 20):
            Image.objects.create(obj='items/images/{}.jpg'.format(i),
                                 description='Image description {}'.format(i), item_id=1)

        for i in range(1, 51):
            for j in range(0, random.randrange(5, 8)):
                id = random.randrange(1, 19)
                image = Image.objects.get(id=id)
                Image.objects.create(obj=image.obj, description=image.description, item_id=i)

        for i in range(1, 51):
            estimation = random.randrange(15000, 80000)
            Estimation.objects.create(value=estimation, item_id=i, user_id=1)

        for i in range(1, 51):
            for j in range(0, random.randrange(3, 8)):
                Comment.objects.create(content=comment, item_id=i, parent_id=None, user_id=1)
