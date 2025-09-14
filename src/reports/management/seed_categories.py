from src.reports.models import Category


def seed_categories():
    categories = [
        "Saneamento",
        "Infraestrutura",
        "Segurança",
        "Energia",
        "Meio-ambiente",
        "Outros",
    ]
    categories_to_create = [Category(name=name) for name in categories]
    Category.objects.bulk_create(
        categories_to_create,
        ignore_conflicts=True,
    )
