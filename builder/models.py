from django.db import models
from django.contrib.auth.models import User

# 1. Home Details Table
class HomeProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    HOME_TYPES = (
        ('Individual', 'Individual House'),
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
    )
    owner_name = models.CharField(max_length=100)
    home_type = models.CharField(max_length=50, choices=HOME_TYPES)
    sqr_feet = models.IntegerField()
    contact_no = models.CharField(max_length=15)
    place = models.CharField(max_length=200)
    start_date = models.DateField()
    finish_date = models.DateField()
    is_finished = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.owner_name} - {self.place}"

# 2. Material Details Table (Like BuilderSmart)
class Material(models.Model):
    # Pudhusa add panra Profession Category
    PROFESSION_CHOICES = (
        ('Masonry', 'Masonry (Cement, Sand, Bricks, Steel)'),
        ('Electrical', 'Electrical (Wires, Switches, Pipes)'),
        ('Plumbing', 'Plumbing (Pipes, Taps, Motors)'),
        ('Carpentry', 'Carpentry (Wood, Doors, Locks)'),
        ('Painting', 'Painting (Paint, Primer, Brushes)'),
    )
    
    # default='Masonry' nu kuduthurukom, so palaya data crash aagathu
    profession_category = models.CharField(max_length=50, choices=PROFESSION_CHOICES, default='Masonry') 
    
    name = models.CharField(max_length=100) 
    company_name = models.CharField(max_length=100) 
    image = models.ImageField(upload_to='materials/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} ({self.company_name}) - {self.profession_category}"

# 3. Materials linked to a specific Home
class HomeMaterial(models.Model):
    home = models.ForeignKey(HomeProject, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.material.name} for {self.home.owner_name}"

# 4. Labor/Professionals Cost linked to a specific Home
class LaborCost(models.Model):
    home = models.OneToOneField(HomeProject, on_delete=models.CASCADE)
    electrician_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    plumber_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mason_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    painter_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    carpenter_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def total_labor_cost(self):
        return sum([self.electrician_cost, self.plumber_cost, self.mason_cost, self.painter_cost, self.carpenter_cost])

    def __str__(self):
        return f"Labor costs for {self.home.owner_name}"
    
