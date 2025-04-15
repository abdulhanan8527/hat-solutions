from django.contrib import admin
from .models import Contact, PortfolioItem, PortfolioImage

# Register your models here.


# Register your models here.
# class PortfolioItemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'category', 'created_at')
#     list_filter = ('category',)
#     search_fields = ('title', 'description')

admin.site.register(Contact)
# admin.site.register(PortfolioItem, PortfolioItemAdmin)

class PortfolioImageInline(admin.TabularInline):
    model = PortfolioImage
    extra = 1  # Number of empty forms to display

@admin.register(PortfolioItem)
class PortfolioItemAdmin(admin.ModelAdmin):
    inlines = [PortfolioImageInline]
    list_display = ('title', 'category', 'project_date')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(PortfolioImage)