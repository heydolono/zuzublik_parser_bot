from sqlalchemy.orm import Session
from database import Site, Price, SessionLocal
from sqlalchemy.sql import func

def add_site(title, url, xpath):
    session = SessionLocal()
    site = Site(title=title, url=url, xpath=xpath)
    session.add(site)
    session.commit()
    session.close()

def get_sites():
    session = SessionLocal()
    sites = session.query(Site.id, Site.url, Site.xpath).all()
    session.close()
    return sites

def save_price(site_id, price):
    session = SessionLocal()
    price_entry = Price(site_id=site_id, price=price)
    session.add(price_entry)
    update_average_price(session, site_id)
    session.commit()
    session.close()

def get_average_prices():
    session = SessionLocal()
    results = session.query(Site.title, func.avg(Price.price)).join(Price).group_by(Site.id).all()
    session.close()
    return results

def update_average_price(session: Session, site_id: int):
    avg_price = session.query(func.avg(Price.price)).filter(Price.site_id == site_id).scalar()
    site = session.query(Site).filter(Site.id == site_id).first()
    if site:
        site.average_price = avg_price
        session.commit()
