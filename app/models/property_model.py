from app.services.tecimobi_service import TecimobService

class PropertyRepository:
    """
    Repository pattern model for Property listings, hybrid local storage & Tecimobi API integration.
    """
    _properties = [
        {
            "id": 1,
            "title": "Apartamento de Luxo com Vista Panorâmica",
            "slug": "apartamento-de-luxo-com-vista-panoramica",
            "type": "Apartamento",
            "purpose": "Venda",
            "price": 2850000.00,
            "condo_fee": 2400.00,
            "iptu": 850.00,
            "area": 220,
            "bedrooms": 4,
            "suites": 3,
            "bathrooms": 4,
            "garage": 3,
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Itaim Bibi",
            "address": "Rua Horácio Lafer, 450",
            "featured": True,
            "status": "Disponível",
            "badge": "Lançamento",
            "description": "Espetacular apartamento em andar alto com pé-direito duplo na sala de estar, varanda gourmet envidraçada com churrasqueira a carvão, acabamentos em mármore importado e automação residencial completa.",
            "amenities": ["Piscina Aquecida", "Academia High-Tech", "Spa & Sauna", "Portaria 24h", "Varanda Gourmet", "Piso Aquecido", "Gerador Full"],
            "image": "img_prop_1.jpg",
            "gallery": ["img_prop_1.jpg", "img_prop_2.jpg", "img_prop_3.jpg"],
            "agent": {
                "name": "Ricardo Mendonça",
                "phone": "(11) 98765-4321",
                "email": "ricardo@7ximoveis.com.br",
                "avatar": "agent_1.jpg"
            }
        },
        {
            "id": 2,
            "title": "Casa de Condomínio Contemporânea",
            "slug": "casa-de-condominio-contemporanea",
            "type": "Casa",
            "purpose": "Venda",
            "price": 4900000.00,
            "condo_fee": 1800.00,
            "iptu": 1200.00,
            "area": 480,
            "bedrooms": 5,
            "suites": 5,
            "bathrooms": 6,
            "garage": 4,
            "city": "Barueri",
            "state": "SP",
            "neighborhood": "Alphaville",
            "address": "Alameda dos Oitis, 120",
            "featured": True,
            "status": "Disponível",
            "badge": "Exclusivo",
            "description": "Residência contemporânea de alto padrão com projeto assinado por renomado arquiteto. Integração total entre os ambientes sociais, piscina com borda infinita, espaço gourmet e paisagismo exuberante.",
            "amenities": ["Piscina Borda Infinita", "Espaço Gourmet", "Home Theater", "Energia Solar", "Quadra de Tênis no Condomínio", "Adega Climatizada"],
            "image": "img_prop_2.jpg",
            "gallery": ["img_prop_2.jpg", "img_prop_1.jpg", "img_prop_4.jpg"],
            "agent": {
                "name": "Fernanda Lima",
                "phone": "(11) 97654-3210",
                "email": "fernanda@7ximoveis.com.br",
                "avatar": "agent_2.jpg"
            }
        },
        {
            "id": 3,
            "title": "Penthouse Duplex em Pinheiros",
            "slug": "penthouse-duplex-em-pinheiros",
            "type": "Cobertura",
            "purpose": "Aluguel",
            "price": 18500.00,
            "condo_fee": 3100.00,
            "iptu": 950.00,
            "area": 310,
            "bedrooms": 3,
            "suites": 3,
            "bathrooms": 5,
            "garage": 3,
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Pinheiros",
            "address": "Rua dos Pinheiros, 890",
            "featured": True,
            "status": "Disponível",
            "badge": "Pronto para Morar",
            "description": "Cobertura duplex espetacular totalmente mobilhada e decorada. Deck privativo com jacuzzi, churrasqueira, vista desimpedida de 360 graus para o pôr do sol de Pinheiros.",
            "amenities": ["Jacuzzi Privativa", "Totalmente Mobiliado", "Ar Condicionado Central", "Fechadura Eletrônica", "Varanda 360º", "Coworking"],
            "image": "img_prop_3.jpg",
            "gallery": ["img_prop_3.jpg", "img_prop_4.jpg", "img_prop_1.jpg"],
            "agent": {
                "name": "Ricardo Mendonça",
                "phone": "(11) 98765-4321",
                "email": "ricardo@7ximoveis.com.br",
                "avatar": "agent_1.jpg"
            }
        },
        {
            "id": 4,
            "title": "Studio Moderno & Tecnológico",
            "slug": "studio-moderno-tecnologico",
            "type": "Studio",
            "purpose": "Venda",
            "price": 680000.00,
            "condo_fee": 580.00,
            "iptu": 180.00,
            "area": 45,
            "bedrooms": 1,
            "suites": 1,
            "bathrooms": 1,
            "garage": 1,
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Vila Madalena",
            "address": "Rua Harmonia, 310",
            "featured": False,
            "status": "Disponível",
            "badge": "Investimento",
            "description": "Studio inteligente ideal para moradia ou investimento em rentabilidade via Airbnb/Short Stay. Prédio conceito com rooftop lounge, lavanderia compartilhada OMO e infraestrutura completa.",
            "amenities": ["Rooftop Lounge", "Lavanderia Compartilhada", "Bicicletário", "Pet Place", "Academia", "Solarium"],
            "image": "img_prop_4.jpg",
            "gallery": ["img_prop_4.jpg", "img_prop_3.jpg", "img_prop_2.jpg"],
            "agent": {
                "name": "Fernanda Lima",
                "phone": "(11) 97654-3210",
                "email": "fernanda@7ximoveis.com.br",
                "avatar": "agent_2.jpg"
            }
        },
        {
            "id": 5,
            "title": "Conjunto Comercial Corporate Faria Lima",
            "slug": "conjunto-comercial-corporate-faria-lima",
            "type": "Comercial",
            "purpose": "Aluguel",
            "price": 25000.00,
            "condo_fee": 4200.00,
            "iptu": 1500.00,
            "area": 280,
            "bedrooms": 0,
            "suites": 0,
            "bathrooms": 4,
            "garage": 6,
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Itaim Bibi",
            "address": "Av. Brig. Faria Lima, 3400",
            "featured": False,
            "status": "Disponível",
            "badge": "Triple A",
            "description": "Laje corporativa pronta em edifício Triple A na Faria Lima. Piso elevado com vinílico novo, forro acústico, ar condicionado VRF, auditório e heliponto homologado.",
            "amenities": ["Edifício Triple A", "Heliponto", "Certificação LEED", "Piso Elevado", "Segurança 24h Biométrica", "Estacionamento Valet"],
            "image": "img_prop_1.jpg",
            "gallery": ["img_prop_1.jpg", "img_prop_3.jpg"],
            "agent": {
                "name": "Carlos Eduardo",
                "phone": "(11) 96543-2109",
                "email": "carlos@7ximoveis.com.br",
                "avatar": "agent_3.jpg"
            }
        },
        {
            "id": 6,
            "title": "Residência Minimalista nos Jardins",
            "slug": "residencia-minimalista-nos-jardins",
            "type": "Casa",
            "purpose": "Venda",
            "price": 6200000.00,
            "condo_fee": 0.00,
            "iptu": 2100.00,
            "area": 520,
            "bedrooms": 4,
            "suites": 4,
            "bathrooms": 6,
            "garage": 4,
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Jardins",
            "address": "Rua Colômbia, 155",
            "featured": True,
            "status": "Disponível",
            "badge": "Alto Padrão",
            "description": "Casa térrea com arquitetura moderna e minimalista nos Jardins. Grandes panos de vidro proporcionam iluminação natural abundante. Jardim interno arborizado com piscina aquecida.",
            "amenities": ["Piscina Aquecida", "Jardim de Inverno", "Guarita Blindada", "Suíte Master com Closet Duplo", "Cozinha Gourmet Viking"],
            "image": "img_prop_2.jpg",
            "gallery": ["img_prop_2.jpg", "img_prop_1.jpg", "img_prop_3.jpg"],
            "agent": {
                "name": "Fernanda Lima",
                "phone": "(11) 97654-3210",
                "email": "fernanda@7ximoveis.com.br",
                "avatar": "agent_2.jpg"
            }
        }
    ]

    @classmethod
    def get_all(cls):
        # Check if Tecimobi API returns items
        result = TecimobService.fetch_properties()
        if result:
            return result.get('properties', [])
        return cls._properties

    @classmethod
    def get_featured(cls):
        all_props = cls.get_all()
        return [p for p in all_props if p.get('featured', False)] or all_props[:3]

    @classmethod
    def get_by_id(cls, property_id):
        # Try Tecimobi API first if active
        tecimobi_prop = TecimobService.fetch_property_by_id(str(property_id))
        if tecimobi_prop:
            return tecimobi_prop

        try:
            pid = int(property_id)
            return next((p for p in cls._properties if p['id'] == pid), None)
        except (ValueError, TypeError):
            return None

    @classmethod
    def get_by_slug(cls, slug):
        all_props = cls.get_all()
        return next((p for p in all_props if p.get('slug') == slug), None)

    @classmethod
    def filter(cls, search_query="", prop_type="", purpose="", min_price=None, max_price=None, bedrooms=None, city="", neighborhood="", sort_by="recent"):
        results = cls.get_all().copy()

        # Text search
        if search_query:
            q = search_query.lower()
            results = [
                p for p in results if
                q in str(p.get('title', '')).lower() or
                q in str(p.get('neighborhood', '')).lower() or
                q in str(p.get('city', '')).lower() or
                q in str(p.get('description', '')).lower() or
                q in str(p.get('type', '')).lower()
            ]

        # Property type
        if prop_type and prop_type.lower() != "todos":
            results = [p for p in results if str(p.get('type', '')).lower() == prop_type.lower()]

        # Purpose (Venda / Aluguel)
        if purpose and purpose.lower() != "todos":
            results = [p for p in results if str(p.get('purpose', '')).lower() == purpose.lower()]

        # City
        if city and city.lower() != "todas":
            results = [p for p in results if str(p.get('city', '')).lower() == city.lower()]

        # Neighborhood
        if neighborhood and neighborhood.lower() != "todos":
            results = [p for p in results if str(p.get('neighborhood', '')).lower() == neighborhood.lower()]

        # Price range
        if min_price is not None:
            try:
                min_p = float(min_price)
                results = [p for p in results if p.get('price', 0) >= min_p]
            except ValueError:
                pass

        if max_price is not None:
            try:
                max_p = float(max_price)
                if max_p > 0:
                    results = [p for p in results if p.get('price', 0) <= max_p]
            except ValueError:
                pass

        # Bedrooms
        if bedrooms is not None:
            try:
                beds = int(bedrooms)
                if beds > 0:
                    results = [p for p in results if p.get('bedrooms', 0) >= beds]
            except ValueError:
                pass

        # Sorting
        if sort_by == 'price-asc':
            results.sort(key=lambda x: x.get('price', 0))
        elif sort_by == 'price-desc':
            results.sort(key=lambda x: x.get('price', 0), reverse=True)
        elif sort_by == 'area-desc':
            results.sort(key=lambda x: x.get('area', 0), reverse=True)
        else: # 'recent'
            results.sort(key=lambda x: x.get('id', 0), reverse=True)

        return results

    @classmethod
    def get_cities(cls):
        return sorted(list(set(p.get('city', '') for p in cls.get_all() if p.get('city'))))

    @classmethod
    def get_neighborhoods(cls):
        return sorted(list(set(p.get('neighborhood', '') for p in cls.get_all() if p.get('neighborhood'))))

    @classmethod
    def get_types(cls):
        return sorted(list(set(p.get('type', '') for p in cls.get_all() if p.get('type'))))
