from genericpath import isfile
import json
import random
from django.core.management.base import BaseCommand, CommandError
from products.models import  Product , Brand , Category
from products.dataset import DATA
import re , requests , os


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        ...

    def parse_dataset(self):
        def parse_integer(data_as_json):
            match = re.search(r'[\d,]+', data_as_json['price'])
            if match:
                data_as_json['price'] =  int(match.group().replace(',', ''))
            else :
                data_as_json['price'] = 0
            
            path = f"./media/dataset/{data_as_json['image_1'].split('/')[-1]}"
            if not os.path.isfile(path):
                with open(path,"wb") as file :
                    file.write(requests.get(data_as_json['image_1']).content)
                    file.close()
            data_as_json['image_1'] = path
            return data_as_json
        return list(map(parse_integer,DATA[:10]))


    def handle(self, *args, **options):
        brands = Brand.objects.all()
        categories = Category.objects.all()
        objs = self.parse_dataset()
        for obj in objs:
            prod = Product(
                name = obj['name'],
                description = obj['name'],
                price = obj['price'] ,
                image_1 = obj['image_1'],
                image_2 = obj['image_1'],
                image_3 = obj['image_1'],
                count=random.randint(0,10),
                brand=random.choice(brands)
                )
            prod.save()
            prod.categories.set(random.choices(categories,k=random.randint(0,2))) if categories.count() > 1 else None
        self.stdout.write(
            self.style.SUCCESS("Added Virtual Products")
        )
