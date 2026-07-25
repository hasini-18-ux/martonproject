from importlib.resources import contents
from turtle import title
from typing import Any
from django.core.management.base import BaseCommand
from amazon.models import Category

class Command(BaseCommand):
    help="This command inserts data into the Category model"
    def handle(self,*args:Any,**options:Any):
        Category.objects.all().delete()
        categories=[
            'Electronics','Mobiles','laptops','Fashion','Furniture','Cameras','Home Appliances','Wearables','Gaming'
        ]
        for category_name in categories:
            Category.objects.create(name=category_name)
        
        self.stdout.write(self.style.SUCCESS("Data inserted successfully!"))

