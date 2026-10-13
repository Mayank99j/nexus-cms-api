from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.db.models import Count, Q
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from .models import Category, Article
from .serializers import (
    CategorySerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleWriteSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Categories.
    Unauthenticated users can list and retrieve categories.
    Staff/Admin can create, update, and delete categories.
    """
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all().order_by('name')


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Articles.
    - GET /api/articles/: List published articles (supports pagination and ?category=slug).
    - GET /api/articles/<slug>/: Detailed article view.
    - Draft articles are strictly isolated from unauthenticated visitors.
    - Staff members have full CRUD permissions.
    """
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleWriteSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.select_related('author', 'category').all()

        # Unauthenticated users or non-staff only see published articles
        if not (user.is_authenticated and user.is_staff):
            queryset = queryset.filter(status='published')
        else:
            status_param = self.request.query_params.get('status')
            if status_param:
                queryset = queryset.filter(status=status_param)

        # Filtering by category (slug or id)
        category_param = self.request.query_params.get('category')
        if category_param:
            if category_param.isdigit():
                queryset = queryset.filter(category_id=int(category_param))
            else:
                queryset = queryset.filter(category__slug=category_param)

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def home_view(request):
    """
    Consumer-facing publication homepage.
    Displays hero branding, category pills filter, and article grid.
    """
    selected_category_slug = request.GET.get('category', '').strip()
    categories = Category.objects.all().order_by('name')

    articles = Article.objects.filter(status='published').select_related('author', 'category')
    selected_category = None
    if selected_category_slug:
        selected_category = categories.filter(slug=selected_category_slug).first()
        if selected_category:
            articles = articles.filter(category=selected_category)

    return render(request, 'index.html', {
        'categories': categories,
        'articles': articles,
        'selected_category_slug': selected_category_slug,
        'selected_category': selected_category,
        'total_published_count': Article.objects.filter(status='published').count(),
    })


def article_detail_view(request, slug):
    """
    Dedicated article reading view.
    Renders article with editorial typography, metadata, and related articles.
    Drafts are inaccessible to non-staff visitors.
    """
    article = get_object_or_404(Article.objects.select_related('author', 'category'), slug=slug)

    # Security check: Unauthenticated/non-staff cannot view drafts
    if article.status != 'published' and not (request.user.is_authenticated and request.user.is_staff):
        raise Http404("Article not found or not published.")

    recent_articles = Article.objects.filter(
        status='published'
    ).exclude(pk=article.pk).select_related('author', 'category')[:3]

    return render(request, 'article_detail.html', {
        'article': article,
        'recent_articles': recent_articles,
    })
