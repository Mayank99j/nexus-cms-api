from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from cms.models import Category, Article

User = get_user_model()


class NexusCMSTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@nexus.local',
            password='adminpassword123'
        )

        # Create categories
        self.cat_eng = Category.objects.create(
            name="Engineering",
            slug="engineering",
            description="Deep dives into engineering."
        )
        self.cat_design = Category.objects.create(
            name="Design Philosophy",
            slug="design-philosophy",
            description="Explorations of tactile design."
        )
        self.cat_arch = Category.objects.create(
            name="Systems Architecture",
            slug="systems-architecture",
            description="Distributed systems and headless setups."
        )

        # Create 3 published articles
        self.art_1 = Article.objects.create(
            title="The Resurgence of Tactile Web Aesthetics",
            slug="the-resurgence-of-tactile-web-aesthetics",
            author=self.admin_user,
            category=self.cat_design,
            status="published",
            content="Detailed discussion about warm beige `#F9F6F0` and terracotta `#C85A32`."
        )
        self.art_2 = Article.objects.create(
            title="Designing Resilient Headless Architectures in 2026",
            slug="designing-resilient-headless-architectures-in-2026",
            author=self.admin_user,
            category=self.cat_arch,
            status="published",
            content="Discussion regarding decoupled API contracts and event flows."
        )
        self.art_3 = Article.objects.create(
            title="Deterministic Memory and High-Throughput Engines",
            slug="deterministic-memory-and-high-throughput-engines",
            author=self.admin_user,
            category=self.cat_eng,
            status="published",
            content="Profiling memory allocations and SQL joins."
        )

        # Create 1 draft article
        self.art_draft = Article.objects.create(
            title="Draft: The Future of Offline-First Synchronization",
            slug="draft-the-future-of-offline-first-synchronization",
            author=self.admin_user,
            category=self.cat_arch,
            status="draft",
            content="Internal notes on vector clocks and synchronization."
        )

    # ---------------- API Tests ----------------
    def test_api_categories_list(self):
        """GET /api/categories/ returns 200 with all 3 categories."""
        response = self.api_client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        slugs = [c['slug'] for c in response.data['results']]
        self.assertIn('engineering', slugs)
        self.assertIn('design-philosophy', slugs)
        self.assertIn('systems-architecture', slugs)
        self.assertEqual(len(slugs), 3)

    def test_api_articles_list_published_only(self):
        """GET /api/articles/ returns 200 and only published articles (no drafts)."""
        response = self.api_client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(len(results), 3)

        returned_slugs = [a['slug'] for a in results]
        self.assertIn('the-resurgence-of-tactile-web-aesthetics', returned_slugs)
        self.assertNotIn('draft-the-future-of-offline-first-synchronization', returned_slugs)

    def test_api_articles_filter_by_category(self):
        """GET /api/articles/?category=engineering filters correctly."""
        response = self.api_client.get('/api/articles/?category=engineering')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['slug'], 'deterministic-memory-and-high-throughput-engines')

    def test_api_article_detail_published(self):
        """GET /api/articles/<slug>/ returns 200 for published article."""
        response = self.api_client.get('/api/articles/the-resurgence-of-tactile-web-aesthetics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Resurgence of Tactile Web Aesthetics')
        self.assertIn('rendered_content', response.data)

    def test_api_draft_isolation_unauthenticated(self):
        """GET /api/articles/<draft-slug>/ returns 404 for unauthenticated visitors."""
        response = self.api_client.get('/api/articles/draft-the-future-of-offline-first-synchronization/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_draft_accessible_to_staff(self):
        """Authenticated staff can view draft articles."""
        self.api_client.force_authenticate(user=self.admin_user)
        response = self.api_client.get('/api/articles/draft-the-future-of-offline-first-synchronization/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'draft')

    # ---------------- Frontend Tests ----------------
    def test_frontend_home_view(self):
        """GET / returns 200 and renders hero and published articles."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nexus")
        self.assertContains(response, "The Resurgence of Tactile Web Aesthetics")
        self.assertNotContains(response, "Draft: The Future of Offline-First Synchronization")

    def test_frontend_article_detail_view(self):
        """GET /article/<slug>/ returns 200 and renders article."""
        response = self.client.get('/article/the-resurgence-of-tactile-web-aesthetics/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Resurgence of Tactile Web Aesthetics")
        self.assertContains(response, "Design Philosophy")

    def test_frontend_draft_isolation(self):
        """GET /article/<draft-slug>/ returns 404 for anonymous users."""
        response = self.client.get('/article/draft-the-future-of-offline-first-synchronization/')
        self.assertEqual(response.status_code, 404)
