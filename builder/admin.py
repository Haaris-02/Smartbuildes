from django.contrib import admin
from .models import HomeProject, Material, HomeMaterial, LaborCost

# Namma create panna tables-a admin panel-la add panrom
admin.site.register(HomeProject)
admin.site.register(Material)
admin.site.register(HomeMaterial)
admin.site.register(LaborCost)