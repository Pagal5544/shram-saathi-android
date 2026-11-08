from app.core.database import SessionLocal
from scripts.seed_catalog import seed_catalog


def test_seed_catalog_is_bilingual_and_idempotent():
    with SessionLocal() as db:
        try:
            first = seed_catalog(db)
            second = seed_catalog(db)
            assert first == (12, 26)
            assert second == (0, 0)
        finally:
            db.rollback()
