from app.models.db_models import Property, PropertyCategory, AgentProfile
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
        
        # Load agent profiles to override avatar, description, instagram, etc.
        try:
            profiles = AgentProfile.query.all()
            profile_map = {p.name: p for p in profiles}
        except Exception:
            profile_map = {}

        result = []
        for prop in properties:
            p_dict = prop.to_dict()
            agent = p_dict.get('agent', {})
            agent_name = agent.get('name')
            if agent_name and agent_name in profile_map:
                prof = profile_map[agent_name]
                if prof.avatar_url:
                    agent['avatar_url'] = prof.avatar_url
                if prof.instagram:
                    agent['instagram'] = prof.instagram
                if prof.description:
                    agent['description'] = prof.description
            result.append(p_dict)

        return result

    @classmethod
    def get_all_agents(cls):
        """Retorna uma lista única de agentes com a contagem de imóveis para cada."""
        properties = cls.get_all()
        agents_map = {}
        for p in properties:
            agent = p.get('agent', {})
            name = agent.get('name')
            if name:
                if name not in agents_map:
                    agents_map[name] = {
                        'name': name,
                        'email': agent.get('email', ''),
                        'phone': agent.get('phone', ''),
                        'creci': agent.get('creci', ''),
                        'avatar_url': agent.get('avatar_url', ''),
                        'instagram': agent.get('instagram', ''),
                        'description': agent.get('description', ''),
                        'property_count': 0
                    }
                agents_map[name]['property_count'] += 1
        
        # Sort by property count descending
        sorted_agents = sorted(agents_map.values(), key=lambda x: x['property_count'], reverse=True)
        return sorted_agents

    @classmethod
    def get_properties_by_agent(cls, agent_name):
        """Retorna os imóveis sob responsabilidade de um corretor específico."""
        properties = cls.get_all()
        # Normaliza o nome para busca insensível a maiúsculas/minúsculas
        search_name = agent_name.lower().strip()
        filtered = []
        for p in properties:
            agent = p.get('agent', {})
            name = agent.get('name', '')
            if name.lower().strip() == search_name:
                filtered.append(p)
        return filtered

    @classmethod
    def calculate_category(cls, prop: dict) -> str:
        """
        Classifica o imóvel lendo as categorias configuradas no banco,
        ordenadas por prioridade (menor número = verificada primeiro).
        Fallback para 'Geral' se nenhuma bater ou tabela vazia.
        """
        try:
            categories = PropertyCategory.query.order_by(
                PropertyCategory.priority.asc()
            ).all()
        except Exception:
            # Tabela ainda não existe (ex: primeiro boot) — usa lógica legada
            categories = []

        if not categories:
            # Lógica legada como segurança
            if prop.get('is_exclusive'):
                return 'Exclusivo'
            if prop.get('price', 0) > 2_000_000:
                return 'Alto Padrão'
            if prop.get('featured'):
                return 'Destaque'
            return 'Geral'

        for cat in categories:
            if cat.matches(prop):
                return cat.name

        return 'Geral'

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
    def get_featured(cls, limit=3):
        properties = Property.query.filter_by(featured=True, status='Disponível').limit(limit).all()
        if not properties:
            properties = Property.query.filter_by(status='Disponível').limit(limit).all()
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
            from sqlalchemy import func, cast, Integer
            query = query.order_by(
                cast(func.nullif(func.regexp_replace(Property.reference, r'\D', '', 'g'), ''), Integer).desc().nullslast(),
                Property.created_at.desc()
            )

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
