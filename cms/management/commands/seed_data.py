from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from cms.models import Category, Article

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds database with superuser, standard categories, and high-quality articles."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Beginning Nexus CMS database seeding..."))

        # 1. Create or update superuser
        admin_username = "admin"
        admin_email = "admin@nexus.local"
        admin_password = "adminpassword123"

        superuser, created = User.objects.get_or_create(
            username=admin_username,
            defaults={"email": admin_email, "first_name": "Editorial", "last_name": "Director"}
        )
        superuser.email = admin_email
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.set_password(admin_password)
        superuser.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_username}' created."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{admin_username}' credentials verified and updated."))

        # 2. Create the 3 canonical categories
        categories_data = [
            {
                "name": "Engineering",
                "slug": "engineering",
                "description": "Deep dives into robust runtime patterns, high-concurrency protocols, and maintainable software craft."
            },
            {
                "name": "Design Philosophy",
                "slug": "design-philosophy",
                "description": "Explorations into tactile digital typography, warm materiality, and humane editorial interfaces."
            },
            {
                "name": "Systems Architecture",
                "slug": "systems-architecture",
                "description": "Strategies for resilient distributed systems, decoupled headless topologies, and event-driven data flow."
            }
        ]

        categories_map = {}
        for cat_item in categories_data:
            cat_obj, _ = Category.objects.update_or_create(
                slug=cat_item["slug"],
                defaults={
                    "name": cat_item["name"],
                    "description": cat_item["description"]
                }
            )
            categories_map[cat_item["name"]] = cat_obj
            self.stdout.write(self.style.SUCCESS(f"Category verified: {cat_obj.name}"))

        # 3. Create 4 high-quality articles (3 published, 1 draft)
        articles_data = [
            {
                "title": "The Resurgence of Tactile Web Aesthetics",
                "slug": "the-resurgence-of-tactile-web-aesthetics",
                "category": categories_map["Design Philosophy"],
                "status": "published",
                "content": """The web of the early 2020s fell into an uninspired uniformity: harsh neon gradients, aggressively stark dark modes, and synthetic glassmorphic panels that felt detached from human experience.

Over the past two years, an intentional counter-movement has taken root. Designers and engineers are rediscovering the enduring qualities of **tactile, editorial interfaces**—surfaces with warm beige backgrounds, crisp paper cards, terracotta accents, and deliberate serif typography.

### Why Materiality Matters

When a reader interacts with an editorial piece, psychological grounding occurs through visual warmth:

> "Digital typography should not pretend to be invisible; it should carry the dignity, weight, and cadence of a printed folio without sacrificing interactive fluidity."

Consider how contrast is modulated:
- **Espresso over pure black**: Using `#2C2825` instead of `#000000` softens visual harshness during prolonged reading.
- **Warm cream surfaces**: Cream (`#F9F6F0`) creates an inviting substrate that reduces eye strain.
- **Terracotta as intentional punctuation**: Highlighting primary interactions with `#C85A32` signals purpose without sensory overload.

```css
/* Tactile Paper Elevation */
.reading-surface {
  background-color: #FFFFFF;
  border: 1px solid #E6E0D4;
  box-shadow: 0 4px 12px rgba(44, 40, 37, 0.05);
}
```

As we build the next generation of publishing platforms, balancing technological agility with human-scale beauty is no longer a luxury—it is the signature of enduring craft."""
            },
            {
                "title": "Designing Resilient Headless Architectures in 2026",
                "slug": "designing-resilient-headless-architectures-in-2026",
                "category": categories_map["Systems Architecture"],
                "status": "published",
                "content": """Decoupling the content store from presentation layers has evolved from an experimental pattern into the bedrock of modern enterprise publishing.

When architectural boundaries are clearly separated, backend teams focus on deterministic schemas, transactional integrity, and granular authorization, while frontend surfaces iterate freely across mobile apps, e-readers, and web applications.

### Core Architectural Pillars

1. **Explicit API Contracts**: JSON representations must treat backward compatibility as non-negotiable.
2. **Selective Invalidation**: Content modifications at the editorial desk emit targeted cache invalidation webhooks.
3. **Stateless Scalability**: Presentation consumers treat the API as a resilient source of truth.

```python
# Headless Content Serialization Pipeline
class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSummarySerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    rendered_content = serializers.CharField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'rendered_content', 'status']
```

### Navigating the Trade-Offs

While headless architectures offer unprecedented versatility, teams must guard against over-engineering:

> "The measure of an architecture's strength is not how many microservices it spans, but how effortlessly a single editor can publish words to the world without friction."

By standardizing on clean RESTful primitives backed by relational safety, organizations achieve durability without operational fatigue."""
            },
            {
                "title": "Deterministic Memory and High-Throughput Engines",
                "slug": "deterministic-memory-and-high-throughput-engines",
                "category": categories_map["Engineering"],
                "status": "published",
                "content": """Building high-throughput content ingestion and query layers requires deep discipline around memory allocation and query plan execution.

Even in interpreted runtime environments, understanding object lifecycles, database query profiling, and eager-loading prevents latency degradation under load.

### Mitigating N+1 Cascades

The most frequent culprit behind sluggish API endpoints is recursive foreign key evaluation in serialization loops:

```python
# Performant Query Construction with Eager Joins
queryset = Article.objects.filter(
    status='published'
).select_related(
    'author', 'category'
).order_by('-created_at')
```

### Operational Checklists for Scale

- **Connection Pool Tuning**: Match database worker limits to expected concurrency ceilings.
- **Index Alignment**: Ensure composite indexes exist on `(status, created_at)` and `slug`.
- **Query Caching**: Keep hot category lookups cached in memory.

When these engineering practices converge, throughput remains stable even through massive reader surges."""
            },
            {
                "title": "Draft: The Future of Offline-First Synchronization",
                "slug": "draft-the-future-of-offline-first-synchronization",
                "category": categories_map["Systems Architecture"],
                "status": "draft",
                "content": """*Editor's Note: This is an internal working draft. Not yet approved for publication.*

Investigating peer-to-peer conflict-free replicated data types (CRDTs) for editorial collaboration:

### Unresolved Hypotheses
- Can state synchronization work over unreliable field networks without split-brain anomalies?
- Performance benchmarks on SQLite local vector clocks vs remote reconciliation.

### Next Steps
1. Prototype WebSocket diff listener in local testbed.
2. Verify tombstone garbage collection for deleted revisions.
3. Align with lead infrastructure team prior to editorial sign-off."""
            }
        ]

        for item in articles_data:
            article_obj, _ = Article.objects.update_or_create(
                slug=item["slug"],
                defaults={
                    "title": item["title"],
                    "category": item["category"],
                    "author": superuser,
                    "content": item["content"],
                    "status": item["status"],
                }
            )
            # Re-save to calculate reading time
            article_obj.save()
            self.stdout.write(self.style.SUCCESS(
                f"Article verified: [{article_obj.status.upper()}] '{article_obj.title}' ({article_obj.reading_time} min read)"
            ))

        self.stdout.write(self.style.SUCCESS("\nDatabase seeding completed successfully!"))
        self.stdout.write(self.style.SUCCESS("Superuser: admin / adminpassword123"))
        self.stdout.write(self.style.SUCCESS(f"Total categories: {Category.objects.count()}"))
        self.stdout.write(self.style.SUCCESS(f"Total articles: {Article.objects.count()} (Published: {Article.objects.filter(status='published').count()}, Draft: {Article.objects.filter(status='draft').count()})"))
