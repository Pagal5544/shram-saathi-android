"""Seed a starter Hindi/English skill catalogue.

Run from the backend directory:
    python -m scripts.seed_catalog
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Skill, SkillCategory


CATALOG = {
    "Masonry": ("राजमिस्त्री", [("Brick Mason", "ईंट मिस्त्री"), ("Concrete Worker", "कंक्रीट मजदूर"), ("Plaster Worker", "प्लास्टर मिस्त्री")]),
    "Construction": ("निर्माण कार्य", [("Construction Helper", "निर्माण सहायक"), ("Shuttering Carpenter", "शटरिंग कारीगर"), ("Bar Bender", "सरिया बांधने वाला")]),
    "Electrical": ("बिजली का काम", [("Electrician", "इलेक्ट्रीशियन"), ("Electrical Helper", "बिजली सहायक")]),
    "Plumbing": ("प्लंबिंग", [("Plumber", "प्लंबर"), ("Plumbing Helper", "प्लंबिंग सहायक")]),
    "Carpentry": ("बढ़ई का काम", [("Carpenter", "बढ़ई"), ("Furniture Carpenter", "फर्नीचर बढ़ई")]),
    "Painting": ("पेंटिंग", [("Painter", "पेंटर"), ("Spray Painter", "स्प्रे पेंटर")]),
    "Welding": ("वेल्डिंग", [("Welder", "वेल्डर"), ("Gas Cutter", "गैस कटर")]),
    "Tiling": ("टाइल लगाने का काम", [("Tile Mason", "टाइल मिस्त्री"), ("Marble Fitter", "मार्बल कारीगर")]),
    "Agriculture": ("कृषि कार्य", [("Farm Worker", "खेत मजदूर"), ("Tractor Operator", "ट्रैक्टर चालक")]),
    "Cleaning": ("सफाई कार्य", [("House Cleaner", "घर की सफाई"), ("Office Cleaner", "कार्यालय सफाई")]),
    "Driving": ("ड्राइविंग", [("Car Driver", "कार चालक"), ("Heavy Vehicle Driver", "भारी वाहन चालक")]),
    "Loading": ("लोडिंग और अनलोडिंग", [("Loader", "लोडर"), ("Warehouse Helper", "गोदाम सहायक")]),
}


def seed_catalog(db: Session) -> tuple[int, int]:
    categories_added = 0
    skills_added = 0

    for category_name, (category_name_hi, skills) in CATALOG.items():
        category = db.scalar(
            select(SkillCategory).where(SkillCategory.name == category_name)
        )
        if category is None:
            category = SkillCategory(
                name=category_name,
                name_hi=category_name_hi,
                is_active=True,
            )
            db.add(category)
            db.flush()
            categories_added += 1

        for skill_name, skill_name_hi in skills:
            existing = db.scalar(
                select(Skill.id).where(
                    Skill.category_id == category.id,
                    Skill.name == skill_name,
                )
            )
            if existing is None:
                db.add(
                    Skill(
                        category_id=category.id,
                        name=skill_name,
                        name_hi=skill_name_hi,
                        is_active=True,
                    )
                )
                skills_added += 1

    db.flush()
    return categories_added, skills_added


def main() -> None:
    with SessionLocal() as db:
        categories_added, skills_added = seed_catalog(db)
        db.commit()
    print(f"Added {categories_added} categories and {skills_added} skills.")


if __name__ == "__main__":
    main()
