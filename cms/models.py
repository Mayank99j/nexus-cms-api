import re
import markdown
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def article_count(self):
        return self.articles.filter(status='published').count()

    @property
    def total_articles(self):
        return self.articles.count()


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    content = models.TextField(help_text="Article content in Markdown or HTML")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    reading_time = models.PositiveIntegerField(
        default=1,
        help_text="Estimated reading time in minutes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def calculate_reading_time(self):
        words = len(re.findall(r'\w+', self.content or ''))
        return max(1, round(words / 200))

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Calculate reading time if default or changed
        calculated = self.calculate_reading_time()
        if not self.reading_time or self.reading_time <= 1:
            self.reading_time = calculated

        super().save(*args, **kwargs)

    @property
    def rendered_content(self):
        """Converts Markdown content into safe, styled HTML."""
        return markdown.markdown(
            self.content or '',
            extensions=['fenced_code', 'tables', 'nl2br']
        )

    @property
    def excerpt(self):
        """Provides a clean plain-text excerpt for cards and previews."""
        plain_text = re.sub(r'#|\*|_|`|>|\[.*?\]\(.*?\)|\n+', ' ', self.content or '')
        plain_text = ' '.join(plain_text.split())
        if len(plain_text) > 175:
            return plain_text[:172].rstrip() + '...'
        return plain_text
