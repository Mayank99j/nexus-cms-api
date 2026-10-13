"""
Autonomous Verification Script for Nexus Headless CMS.
Runs exhaustive checks on:
1. Database contents (Categories, Articles, Superuser)
2. Django Client HTTP endpoints:
   - GET / (Homepage)
   - GET /?category=engineering
   - GET /article/the-resurgence-of-tactile-web-aesthetics/
   - GET /article/draft-the-future-of-offline-first-synchronization/ (404 expected for anonymous)
   - GET /api/categories/
   - GET /api/articles/
   - GET /api/articles/?category=systems-architecture
   - GET /api/articles/the-resurgence-of-tactile-web-aesthetics/
   - GET /api/articles/draft-the-future-of-offline-first-synchronization/ (404 expected)
   - Authenticated GET /api/articles/ (staff can see drafts)
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from cms.models import Category, Article

User = get_user_model()


def run_verification():
    print("=" * 65)
    print(" NEXUS HEADLESS CMS - COMPREHENSIVE VERIFICATION SUITE")
    print("=" * 65)

    all_passed = True
    checks_passed = 0
    total_checks = 0

    def assert_check(condition, description, detail=""):
        nonlocal checks_passed, total_checks, all_passed
        total_checks += 1
        if condition:
            checks_passed += 1
            print(f" [PASS] {description}")
            if detail:
                print(f"        -> {detail}")
        else:
            all_passed = False
            print(f" [FAIL] {description}")
            if detail:
                print(f"        -> ERROR: {detail}")

    # --- 1. Database Validation ---
    print("\n[Phase 1] Database & Seed State Checks")
    admin_user = User.objects.filter(username="admin").first()
    assert_check(
        admin_user is not None and admin_user.is_superuser,
        "Superuser 'admin' exists with superuser privileges",
        f"Email: {admin_user.email if admin_user else 'None'}"
    )

    categories = list(Category.objects.all().order_by('slug'))
    assert_check(
        len(categories) == 3,
        "3 Categories exist in SQLite database",
        f"Categories: {[c.name for c in categories]}"
    )

    published_articles = list(Article.objects.filter(status='published'))
    draft_articles = list(Article.objects.filter(status='draft'))
    assert_check(
        len(published_articles) == 3 and len(draft_articles) == 1,
        "4 Articles exist: 3 Published, 1 Draft",
        f"Published: {len(published_articles)}, Draft: {len(draft_articles)}"
    )

    # --- 2. REST API Endpoint Checks ---
    print("\n[Phase 2] REST API Verifications (DRF)")
    client = Client()

    # GET /api/categories/
    res_cats = client.get('/api/categories/')
    assert_check(
        res_cats.status_code == 200,
        "GET /api/categories/ returns HTTP 200",
        f"Items returned: {res_cats.json().get('count', len(res_cats.json()))}"
    )

    # GET /api/articles/
    res_articles = client.get('/api/articles/')
    assert_check(
        res_articles.status_code == 200,
        "GET /api/articles/ returns HTTP 200",
        f"Published count in response: {res_articles.json().get('count')}"
    )
    assert_check(
        res_articles.json().get('count') == 3,
        "GET /api/articles/ returns ONLY published articles (Count = 3)",
        f"Results count: {len(res_articles.json().get('results', []))}"
    )

    # Category Filter on API
    res_filt = client.get('/api/articles/?category=engineering')
    assert_check(
        res_filt.status_code == 200 and len(res_filt.json().get('results', [])) == 1,
        "GET /api/articles/?category=engineering filters accurately to 1 item",
        f"Matched: {[a['title'] for a in res_filt.json().get('results', [])]}"
    )

    # Published Article Detail
    res_pub_detail = client.get('/api/articles/the-resurgence-of-tactile-web-aesthetics/')
    assert_check(
        res_pub_detail.status_code == 200 and 'rendered_content' in res_pub_detail.json(),
        "GET /api/articles/<slug>/ returns 200 with rendered Markdown HTML",
        f"Title: {res_pub_detail.json().get('title')}"
    )

    # Draft Article Detail (Anonymous - MUST BE 404)
    res_draft_anon = client.get('/api/articles/draft-the-future-of-offline-first-synchronization/')
    assert_check(
        res_draft_anon.status_code == 404,
        "Draft article returns HTTP 404 for anonymous API requests (Draft Isolation)",
        f"Status: {res_draft_anon.status_code}"
    )

    # Draft Article Detail (Staff Authenticated - MUST BE 200)
    client.force_login(admin_user)
    res_draft_auth = client.get('/api/articles/draft-the-future-of-offline-first-synchronization/')
    assert_check(
        res_draft_auth.status_code == 200,
        "Draft article accessible (HTTP 200) for authenticated staff API requests",
        f"Status: {res_draft_auth.status_code}"
    )
    client.logout()

    # --- 3. Consumer-Facing Frontend Checks ---
    print("\n[Phase 3] Consumer-Facing Frontend Verifications")
    res_home = client.get('/')
    assert_check(
        res_home.status_code == 200,
        "GET / returns HTTP 200",
        "Home view loaded successfully"
    )
    assert_check(
        b"Nexus" in res_home.content and b"The Resurgence of Tactile Web Aesthetics" in res_home.content,
        "GET / contains publication branding, editorial tagline, and article cards",
        "HTML contains rendered article cards"
    )
    assert_check(
        b"Draft: The Future of Offline-First Synchronization" not in res_home.content,
        "GET / isolates draft articles from reader homepage",
        "Draft title absent from public view"
    )

    # Category Filter on Frontend
    res_cat_front = client.get('/?category=design-philosophy')
    assert_check(
        res_cat_front.status_code == 200,
        "GET /?category=design-philosophy returns HTTP 200",
        "Filtered view loaded"
    )

    # Dedicated Article Detail Page
    res_reader = client.get('/article/the-resurgence-of-tactile-web-aesthetics/')
    assert_check(
        res_reader.status_code == 200 and b"Why Materiality Matters" in res_reader.content,
        "GET /article/<slug>/ returns HTTP 200 with formatted markdown content",
        "Rendered HTML headings present"
    )

    # Draft Isolation on Frontend
    res_reader_draft = client.get('/article/draft-the-future-of-offline-first-synchronization/')
    assert_check(
        res_reader_draft.status_code == 404,
        "GET /article/<draft-slug>/ returns HTTP 404 for unauthenticated readers",
        f"Status: {res_reader_draft.status_code}"
    )

    # Editorial Admin Desk
    res_admin = client.get('/admin/login/')
    assert_check(
        res_admin.status_code == 200 and b"Nexus CMS Editorial Desk" in res_admin.content,
        "GET /admin/login/ returns HTTP 200 with custom 'Nexus CMS Editorial Desk' branding",
        "Admin branding verified"
    )

    # --- Summary ---
    print("\n" + "=" * 65)
    print(f" RESULTS: {checks_passed}/{total_checks} checks passed successfully.")
    print("=" * 65)

    if not all_passed:
        print("[!] Verification failed.")
        sys.exit(1)
    else:
        print("[OK] All verifications passed without error!")


if __name__ == '__main__':
    run_verification()
