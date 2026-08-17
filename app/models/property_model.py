from app.models.db_models import Property
from app import db
import math

class PropertyRepository:
    """
    Repository pattern model for Property listings, using local SQLAlchemy Database.
    """

    @classmethod
    def get_all(cls):
        # Retorna todos os imóveis ativos
        properties = Property.query.filter_by(status='Disponível').all()
        return [p.to_dict() for p in properties]

    @classmethod
    def calculate_category(cls, prop):
        if prop.get('is_exclusive'):
            return "Exclusivo"
        if prop.get('price', 0) > 2000000:
            return "Alto Padrão"
        if prop.get('featured'):
            return "Destaque"
        return "Geral"

    @classmethod
    def toggle_exclusive(cls, property_id):
        prop = Property.query.get(str(property_id))
        if prop:
            prop.is_exclusive = not prop.is_exclusive
            prop.calculated_category = cls.calculate_category(prop.to_dict())
            db.session.commit()
            return prop.is_exclusive
        return None

    @classmethod
    def get_featured(cls):
        properties = Property.query.filter_by(featured=True, status='Disponível').limit(3).all()
        if not properties:
            properties = Property.query.filter_by(status='Disponível').limit(3).all()
        return [p.to_dict() for p in properties]

    @classmethod
    def get_by_id(cls, property_id):
        prop = Property.query.get(str(property_id))
        if prop:
            return prop.to_dict()
            
        # Fallback para string reference ou slug
        s_id = str(property_id).strip()
        prop = Property.query.filter((Property.reference == s_id) | (Property.slug == s_id)).first()
        if prop:
            return prop.to_dict()
        return None

    @classmethod
    def get_by_slug(cls, slug):
        prop = Property.query.filter_by(slug=slug).first()
        return prop.to_dict() if prop else None

    @classmethod
    def filter(cls, page=1, per_page=12, search_query="", prop_type="", purpose="", min_price=None, max_price=None,
               bedrooms=None, suites=None, bathrooms=None, garage=None,
               min_area=None, max_area=None,
               city="", neighborhood="",
               financeable=None, exchange=None, furnished=None,
               sort_by="recent", category=None):
        
        query = Property.query.filter_by(status='Disponível')

        if category and category.lower() != "todas":
            query = query.filter(db.func.lower(Property.calculated_category) == category.lower())

        if search_query:
            q = f"%{search_query.lower()}%"
            query = query.filter(
                (db.func.lower(Property.title).like(q)) |
                (db.func.lower(Property.reference).like(q)) |
                (db.func.lower(Property.neighborhood).like(q)) |
                (db.func.lower(Property.city).like(q)) |
                (db.func.lower(Property.type).like(q)) |
                (db.func.lower(Property.condominium_name).like(q))
            )

        if prop_type and prop_type.lower() != "todos":
            query = query.filter(db.func.lower(Property.type) == prop_type.lower())

        if purpose and purpose.lower() != "todos":
            query = query.filter(db.func.lower(Property.purpose) == purpose.lower())

        if city and city.lower() != "todas":
            query = query.filter(db.func.lower(Property.city) == city.lower())

        if neighborhood and neighborhood.lower() != "todos":
            query = query.filter(db.func.lower(Property.neighborhood) == neighborhood.lower())

        if min_price is not None and min_price != "":
            try:
                query = query.filter(Property.price >= float(min_price))
            except (ValueError, TypeError):
                pass

        if max_price is not None and max_price != "":
            try:
                query = query.filter(Property.price <= float(max_price))
            except (ValueError, TypeError):
                pass

        if bedrooms is not None and bedrooms != "":
            try:
                query = query.filter(Property.bedrooms >= int(bedrooms))
            except (ValueError, TypeError):
                pass

        if suites is not None and suites != "":
            try:
                query = query.filter(Property.suites >= int(suites))
            except (ValueError, TypeError):
                pass

        if bathrooms is not None and bathrooms != "":
            try:
                query = query.filter(Property.bathrooms >= int(bathrooms))
            except (ValueError, TypeError):
                pass

        if garage is not None and garage != "":
            try:
                query = query.filter(Property.garage >= int(garage))
            except (ValueError, TypeError):
                pass

        if min_area is not None and min_area != "":
            try:
                query = query.filter(Property.area >= float(min_area))
            except (ValueError, TypeError):
                pass

        if max_area is not None and max_area != "":
            try:
                query = query.filter(Property.area <= float(max_area))
            except (ValueError, TypeError):
                pass

        if financeable == '1':
            query = query.filter(Property.is_financeable == True)

        if exchange == '1':
            query = query.filter(Property.accepts_exchange == True)

        if furnished == '1':
            query = query.filter((Property.furnished.isnot(None)) & (Property.furnished != 'Não mobiliado'))

        # Sorting
        sort_key = sort_by.replace('-', '_') if sort_by else "recent"
        if sort_key == "price_asc":
            query = query.order_by(Property.price.asc())
        elif sort_key == "price_desc":
            query = query.order_by(Property.price.desc())
        elif sort_key == "area_desc":
            query = query.order_by(Property.area.desc())
        else:  # 'recent'
            query = query.order_by(Property.created_at.desc(), Property.id.desc())

        # Pagination
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'properties': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'current_page': pagination.page,
            'last_page': pagination.pages,
            'per_page': pagination.per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    @classmethod
    def get_cities(cls):
        cities = db.session.query(Property.city).filter(Property.city.isnot(None), Property.status == 'Disponível').distinct().all()
        return sorted([c[0] for c in cities if c[0]])

    @classmethod
    def get_types(cls):
        types = db.session.query(Property.type).filter(Property.type.isnot(None), Property.status == 'Disponível').distinct().all()
        return sorted([t[0] for t in types if t[0]])

    @classmethod
    def get_neighborhoods(cls):
        neighborhoods = db.session.query(Property.neighborhood).filter(Property.neighborhood.isnot(None), Property.status == 'Disponível').distinct().all()
        return sorted([n[0] for n in neighborhoods if n[0]])
