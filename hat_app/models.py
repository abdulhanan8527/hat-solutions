from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class PortfolioItem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    main_image = models.ImageField(upload_to='portfolio/main/')  # Main image for listings
    category = models.CharField(max_length=50, choices=[
        ('app', 'App'),
        ('product', 'Product'),
        ('branding', 'Branding')
    ])
    client = models.CharField(max_length=200, blank=True)
    # project_date = models.DateField()
    project_date = models.DateField(default=timezone.now)  # Or another default
    # project_date = models.DateField(null=True, blank=True)
    project_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug is unique
            counter = 1
            while PortfolioItem.objects.filter(slug=self.slug).exists():
                self.slug = f"{slugify(self.title)}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

class PortfolioImage(models.Model):
    portfolio_item = models.ForeignKey(PortfolioItem, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='portfolio/additional/')
    alt_text = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.portfolio_item.title}"