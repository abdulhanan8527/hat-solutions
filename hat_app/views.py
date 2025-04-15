from django.shortcuts import get_object_or_404, render, redirect
from .forms import ContactForm
from .models import Contact, PortfolioItem
from django.http import JsonResponse

# Create your views here.

# def home(request):
#     return render(request, 'index.html')

def home(request):
    portfolio_items = PortfolioItem.objects.all()[:6]  # Show first 6 items on homepage
    return render(request, 'index.html', {'portfolio_items': portfolio_items})

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def team(request):
    return render(request, 'team.html')

def contact(request):
    return render(request, 'contact.html')

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Redirect to a success page
#     else:
#         form = ContactForm()
    
#     return render(request, 'index.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ContactForm()
    return render(request, 'index.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')

def portfolio_list(request):
    items = PortfolioItem.objects.all().order_by('-project_date')
    return render(request, 'portfolio/portfolio.html', {'portfolio_items': items})

# def portfolio_detail(request, pk):
#     item = get_object_or_404(PortfolioItem, pk=pk)
#     return render(request, 'portfolio/portfolio-details.html', {'portfolio_item': item})

def portfolio_detail(request, slug):
    item = get_object_or_404(PortfolioItem, slug=slug)
    return render(request, 'portfolio/portfolio-details.html', {'portfolio_item': item})