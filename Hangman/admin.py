from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Game, Try

class TryInline(admin.TabularInline):
    model = Try
    extra = 0  

class GameAdmin(admin.ModelAdmin):
    list_display = ("user", "tries_count", "is_finished", "created_at")
    list_filter = ("user",)
    search_fields = ("user__username", "letter")
    inlines = [TryInline]
    date_hierarchy = "created_at"

    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("tries") 
# Реєстрація моделі Game у адмінці
admin.site.register(Game, GameAdmin)

# Вилучаємо модель Group з адмінки
admin.site.unregister(Group)
