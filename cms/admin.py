from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article

# Editorial Desk Branding
admin.site.site_header = "Nexus CMS Editorial Desk"
admin.site.site_title = "Nexus CMS Editorial Desk"
admin.site.index_title = "Editorial & Content Operations"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'published_article_count', 'total_article_count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    @admin.display(description="Published Articles")
    def published_article_count(self, obj):
        count = obj.article_count
        return format_html(
            '<span style="background-color: #EBF3EE; color: #365B45; padding: 3px 8px; border-radius: 12px; font-weight: 600; font-size: 0.82rem;">{} published</span>',
            count
        )

    @admin.display(description="Total Articles")
    def total_article_count(self, obj):
        return obj.total_articles


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'author',
        'status_badge',
        'reading_time_display',
        'created_at',
        'updated_at'
    )
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'author__username', 'author__email')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_select_related = ('author', 'category')
    list_per_page = 20

    fieldsets = (
        ('Article Content', {
            'fields': ('title', 'slug', 'category', 'content')
        }),
        ('Publication Status & Ownership', {
            'fields': ('author', 'status', 'reading_time')
        }),
    )

    @admin.display(description="Status")
    def status_badge(self, obj):
        if obj.status == 'published':
            return format_html(
                '<span style="background-color: #E8F0EC; color: #2B573D; border: 1px solid #6B8E7B; padding: 2px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Published</span>'
            )
        return format_html(
            '<span style="background-color: #FAF0EC; color: #9C3D1A; border: 1px solid #D96B43; padding: 2px 10px; border-radius: 9999px; font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em;">Draft</span>'
        )

    @admin.display(description="Read Time")
    def reading_time_display(self, obj):
        return f"{obj.reading_time} min"
