from django.shortcuts import get_object_or_404, render,redirect
from django.db.models import Sum
from .models import Material,HomeProject,HomeMaterial,LaborCost
from .forms import HomeProjectForm, HomeMaterialForm, LaborCostForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q

def search_materials(request):
    query = request.GET.get('q') # User type panna word-a vangurom
    results = []
    
    if query:
        # Material name OR Company name-la antha word irukka nu thedurom
        results = Material.objects.filter(
            Q(name__icontains=query) | Q(company_name__icontains=query)
        )
        
    return render(request, 'search_results.html', {'results': results, 'query': query})

def register_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Register aanathum automatic login
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')


def home_page(request):
    return render(request, 'home.html')

def materials_page(request):
    materials = Material.objects.all()
    
    materials_data = []
    for m in materials:
        img_url = m.image.url if m.image else ""
        materials_data.append({
            'id': m.id,
            'profession': m.profession_category, # Pudhusa add panna field
            'name': m.name,
            'company': m.company_name,
            'price': float(m.price),
            'image': img_url
        })

    # First dropdown-kaga unique professions-a mattum edukkurom
    unique_professions = list(set([m.profession_category for m in materials]))

    context = {
        'unique_professions': unique_professions,
        'materials_json': materials_data 
    }
    return render(request, 'materials_list.html', context)

@login_required(login_url='login')
def add_home(request):
    if request.method == 'POST':
        form = HomeProjectForm(request.POST)
        if form.is_valid():
            form.save() # Data-va database-la save panrom
            return redirect('home') # Save aanathum Home page-ku anuppidrom
    else:
        form = HomeProjectForm() # Puthu blank form
        
    return render(request, 'add_home.html', {'form': form})

@login_required(login_url='login')
def view_homes(request):
    # 1. Mudiyatha (Active) projects mattum edukurom
    active_homes = HomeProject.objects.filter(user=request.user, is_finished=False)
    
    # 2. Mudinja (Finished) projects mattum edukurom
    finished_homes = HomeProject.objects.filter(user=request.user, is_finished=True)
    
    # Rendaum HTML-ku anupurom
    context = {
        'active_homes': active_homes,
        'finished_homes': finished_homes
    }
    return render(request, 'view_homes.html', context)
    
@login_required(login_url='login')
def mark_as_finished(request, id):
    # Antha specific project-a edukurom
    project = get_object_or_404(HomeProject, id=id, user=request.user)
    
    # Status-a True nu mathurom (Finished aakidrom)
    project.is_finished = True
    project.save()
    
    # Thirumba My Projects page-ke anupudrom
    return redirect('view_homes')  

def update_home(request, id):
    home = HomeProject.objects.get(id=id) # Entha home-a click panrangalo atha edukkurom
    
    if request.method == 'POST':
        # Palaya data mela pudhu data-va overwrite panrom (instance=home)
        form = HomeProjectForm(request.POST, instance=home) 
        if form.is_valid():
            form.save()
            return redirect('view_homes') # Save aana piragu list page-ku anuppudrom
    else:
        # Palaya data-va form-la pre-fill panni kaaturom
        form = HomeProjectForm(instance=home)
        
    return render(request, 'update_home.html', {'form': form})

# Oru specific home-ku materials add panrathuku
def add_material_to_home(request, id):
    home = HomeProject.objects.get(id=id)
    
    if request.method == 'POST':
        # Custom HTML form-la irunthu data-va edukkurom
        material_id = request.POST.get('material_id')
        quantity = request.POST.get('quantity')
        
        if material_id and quantity:
            selected_material = Material.objects.get(id=material_id)
            total = selected_material.price * int(quantity)
            
            # Database-la save panrom
            HomeMaterial.objects.create(
                home=home,
                material=selected_material,
                quantity=quantity,
                total_price=total
            )
            return redirect('add_material', id=home.id)

    # JavaScript-ku data anuppa JSON format mathurom
    materials = Material.objects.all()
    materials_data = []
    for m in materials:
        materials_data.append({
            'id': m.id,
            'profession': m.profession_category,
            'name': m.name,
            'company': m.company_name,
            'price': float(m.price)
        })

    unique_professions = list(set([m.profession_category for m in materials]))
    added_materials = HomeMaterial.objects.filter(home=home)
    
    context = {
        'home': home,
        'added_materials': added_materials,
        'unique_professions': unique_professions,
        'materials_json': materials_data
    }
    return render(request, 'add_home_material.html', context)

    # JavaScript-ku data anuppa JSON format mathurom
    materials = Material.objects.all()
    materials_data = []
    for m in materials:
        materials_data.append({
            'id': m.id,
            'profession': m.profession_category,
            'name': m.name,
            'company': m.company_name,
            'price': float(m.price)
        })

    unique_professions = list(set([m.profession_category for m in materials]))
    added_materials = HomeMaterial.objects.filter(home=home)
    
    context = {
        'home': home,
        'added_materials': added_materials,
        'unique_professions': unique_professions,
        'materials_json': materials_data
    }
    return render(request, 'add_home_material.html', context)

def generate_bill(request, id):
    home = HomeProject.objects.get(id=id)
    materials = HomeMaterial.objects.filter(home=home)
    
    # Material Total Cost-a database-la irunthe sum panni edukkurom
    total_material_cost = materials.aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Intha home-ku already LaborCost iruntha edukkurom, illana pudhusa create panrom
    labor_cost, created = LaborCost.objects.get_or_create(home=home)
    
    profit = 0
    grand_total = 0
    show_bill = False

    if request.method == 'POST':
        form = LaborCostForm(request.POST, instance=labor_cost)
        profit_input = request.POST.get('profit', 0) # HTML-la irunthu profit amount vangurom
        
        if form.is_valid():
            form.save()
            profit = float(profit_input) if profit_input else 0
            
            # Model-la iruka function use panni labor total edukkurom
            total_labor = labor_cost.total_labor_cost() 
            
            # Final Grand Total calculation
            grand_total = float(total_material_cost) + float(total_labor) + profit
            show_bill = True # Bill-a show panna flag
    else:
        form = LaborCostForm(instance=labor_cost)

    context = {
        'home': home,
        'materials': materials,
        'total_material_cost': total_material_cost,
        'form': form,
        'profit': profit,
        'grand_total': grand_total,
        'show_bill': show_bill,
        'labor_cost': labor_cost
    }
    return render(request, 'generate_bill.html', context)