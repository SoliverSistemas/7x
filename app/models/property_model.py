from app.services.tecimobi_service import TecimobService

class PropertyRepository:
    """
    Repository pattern model for Property listings, hybrid local storage & Tecimob API integration.
    """
    _properties = [
        {
            "id": 1,
            "reference": "7X-AP101",
            "title": "Apartamento de Luxo com Vista Panorâmica",
            "slug": "apartamento-de-luxo-com-vista-panoramica",
            "type": "Apartamento",
            "subtype": "Apartamento Padrão",
            "purpose": "Venda",
            "price": 2850000.00,
            "condo_fee": 2400.00,
            "iptu": 850.00,
            "area": 220,
            "area_total": 310,
            "bedrooms": 4,
            "suites": 3,
            "bathrooms": 4,
            "garage": 3,
            "garage_type": "Cobertas e demarcadas",
            "solar_position": "Face Norte",
            "floor_number": "18º Andar",
            "total_floors": 24,
            "condominium_name": "Edifício Horizon Itaim",
            "is_financeable": True,
            "accepts_exchange": True,
            "furnished": "Semi-mobiliado (Armários planejados Ornare)",
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Itaim Bibi",
            "address": "Rua Horácio Lafer, 450",
            "zip_code": "04538-133",
            "latitude": -23.5857,
            "longitude": -46.6785,
            "featured": True,
            "status": "Disponível",
            "badge": "Lançamento",
            "description": "Espetacular apartamento em andar alto com vista livre e panorâmica de 180° para a região mais nobre do Itaim Bibi. Projeto de interiores contemporâneo com acabamentos em mármore importado, sala com 3 ambientes integrados à varanda gourmet envidraçada com churrasqueira a carvão. A suíte master conta com closet duplo e banheira de imersão. Sistema de automação residencial de iluminação, climatização e cortinas já instalado.",
            "amenities_property": [
                "Varanda Gourmet com Churrasqueira",
                "Ar Condicionado Central VRF",
                "Automação Residencial Completa",
                "Piso em Mármore Travertino",
                "Suíte Master com Hidromassagem",
                "Closet Duplo",
                "Fechadura Biométrica",
                "Janelas com Isolamento Acústico",
                "Despensa & Área de Serviço Separada"
            ],
            "amenities_condo": [
                "Piscina Aquecida com Raia de 25m",
                "Academia High-Tech com Equipamentos Life Fitness",
                "Spa com Sauna Seca e Úmida",
                "Portaria 24h com Guarita Blindada",
                "Gerador Full para Todo o Edifício",
                "Salão de Festas com Espaço Gourmet",
                "Vagas para Carro Elétrico com Carregador",
                "Bicicletário Privativo"
            ],
            "amenities": [
                "Piscina Aquecida", "Academia High-Tech", "Spa & Sauna", "Portaria 24h",
                "Varanda Gourmet", "Automação", "Gerador Full", "Vaga Elétrica"
            ],
            "image": "img_prop_1.jpg",
            "gallery": ["img_prop_1.jpg", "img_prop_2.jpg", "img_prop_3.jpg", "img_prop_4.jpg"],
            "agent": {
                "name": "Ricardo Mendonça",
                "creci": "CRECI 184.920-F",
                "phone": "(11) 98765-4321",
                "email": "ricardo@7ximoveis.com.br",
                "avatar": "agent_1.jpg"
            }
        },
        {
            "id": 2,
            "reference": "7X-CA204",
            "title": "Casa de Condomínio Contemporânea",
            "slug": "casa-de-condominio-contemporanea",
            "type": "Casa",
            "subtype": "Casa em Condomínio Fechado",
            "purpose": "Venda",
            "price": 4900000.00,
            "condo_fee": 1800.00,
            "iptu": 1200.00,
            "area": 480,
            "area_total": 650,
            "bedrooms": 5,
            "suites": 5,
            "bathrooms": 6,
            "garage": 4,
            "garage_type": "4 Vagas cobertas + 2 descobertas",
            "solar_position": "Face Leste / Sol da manhã",
            "floor_number": "2 Pavimentos",
            "total_floors": 2,
            "condominium_name": "Residencial Alphaville 1",
            "is_financeable": True,
            "accepts_exchange": False,
            "furnished": "Totalmente Mobiliada & Decorada",
            "city": "Barueri",
            "state": "SP",
            "neighborhood": "Alphaville",
            "address": "Alameda dos Oitis, 120",
            "zip_code": "06454-000",
            "latitude": -23.4988,
            "longitude": -46.8522,
            "featured": True,
            "status": "Disponível",
            "badge": "Exclusivo",
            "description": "Residência contemporânea de alto padrão com projeto assinado por renomado escritório de arquitetura. Integração total entre os ambientes sociais, living com pé-direito duplo de 6 metros e amplos panos de vidro que valorizam a luz natural. Área externa cinematográfica com piscina aquecida de borda infinita, lounge com fire pit, espaço gourmet completo com chopeira embutida e paisagismo exuberante com irrigação automatizada.",
            "amenities_property": [
                "Piscina com Borda Infinita & Aquecimento",
                "Espaço Gourmet com Chopeira e Churrasqueira",
                "Home Theater Acústico com Projetor 4K",
                "Energia Solar Fotovoltaica com Baterias",
                "Adega Climatizada para 200 Garrafas",
                "Fire Pit & Lounge Externo",
                "Pé-direito Duplo de 6 Metros",
                "Irrigação Automatizada no Jardim",
                "Suíte Master com Terraço Privativo"
            ],
            "amenities_condo": [
                "Clube Privativo Exclusivo aos Moradores",
                "Quadra de Tênis de Saibro & Beach Tennis",
                "Campo de Futebol Society com Grama Sintética",
                "Segurança e Rondas 24h Armada",
                "Pista de Caminhada Arborizada",
                "Heliponto Homologado",
                "Lago Natural e Bosque Preservado"
            ],
            "amenities": [
                "Piscina Borda Infinita", "Espaço Gourmet", "Home Theater", "Energia Solar",
                "Quadra de Tênis", "Adega Climatizada", "Segurança Armada"
            ],
            "image": "img_prop_2.jpg",
            "gallery": ["img_prop_2.jpg", "img_prop_1.jpg", "img_prop_4.jpg", "img_prop_3.jpg"],
            "agent": {
                "name": "Fernanda Lima",
                "creci": "CRECI 195.430-F",
                "phone": "(11) 97654-3210",
                "email": "fernanda@7ximoveis.com.br",
                "avatar": "agent_2.jpg"
            }
        },
        {
            "id": 3,
            "reference": "7X-CB308",
            "title": "Penthouse Duplex em Pinheiros",
            "slug": "penthouse-duplex-em-pinheiros",
            "type": "Cobertura",
            "subtype": "Penthouse Duplex",
            "purpose": "Aluguel",
            "price": 18500.00,
            "condo_fee": 3100.00,
            "iptu": 950.00,
            "area": 310,
            "area_total": 420,
            "bedrooms": 3,
            "suites": 3,
            "bathrooms": 5,
            "garage": 3,
            "garage_type": "Cobertas com depósito privativo",
            "solar_position": "Face Norte / 360 Graus",
            "floor_number": "24º e 25º Andar (Duplex)",
            "total_floors": 25,
            "condominium_name": "Pinheiros Tower Penthouse",
            "is_financeable": False,
            "accepts_exchange": False,
            "furnished": "Porteira Fechada (Alto Padrão)",
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Pinheiros",
            "address": "Rua dos Pinheiros, 890",
            "zip_code": "05422-001",
            "latitude": -23.5673,
            "longitude": -46.6892,
            "featured": True,
            "status": "Disponível",
            "badge": "Pronto para Morar",
            "description": "Cobertura duplex espetacular no coração de Pinheiros, entregue pronta para morar na modalidade porteira fechada com mobiliário assinado e curadoria de arte. Pavimento superior com solarium aberto, deck de madeira nobre com hidromassagem Jacuzzi, churrasqueira gourmet e vista deslumbrante em 360° para o pôr do sol. Living integrado com adega envidraçada e lareira a gás.",
            "amenities_property": [
                "Jacuzzi Privativa no Terraço Superior",
                "Deck de Madeira com Vista 360º",
                "Totalmente Mobiliada (Design Assinado)",
                "Lareira a Gás no Living",
                "Ar Condicionado Central Inverter em Todos os Ambientes",
                "Fechaduras Eletrônicas com Senha e Cartão",
                "Adega Envidraçada Climatizada",
                "Depósito Privativo na Garagem"
            ],
            "amenities_condo": [
                "Coworking Equipado e Salas de Reunião",
                "Rooftop Lounge com Bar Integrado",
                "Piscina Semiolímpica Aquecida",
                "Academia com Personal Trainer Disponível",
                "Lavanderia Compartilhada OMO",
                "Serviço de Concierge e Valet",
                "Portaria 24h com Controle de Acesso Facial"
            ],
            "amenities": [
                "Jacuzzi Privativa", "Totalmente Mobiliado", "Ar Condicionado",
                "Fechadura Eletrônica", "Varanda 360º", "Coworking", "Concierge"
            ],
            "image": "img_prop_3.jpg",
            "gallery": ["img_prop_3.jpg", "img_prop_4.jpg", "img_prop_1.jpg", "img_prop_2.jpg"],
            "agent": {
                "name": "Ricardo Mendonça",
                "creci": "CRECI 184.920-F",
                "phone": "(11) 98765-4321",
                "email": "ricardo@7ximoveis.com.br",
                "avatar": "agent_1.jpg"
            }
        },
        {
            "id": 4,
            "reference": "7X-ST402",
            "title": "Studio Moderno & Tecnológico",
            "slug": "studio-moderno-tecnologico",
            "type": "Studio",
            "subtype": "Studio Residencial / Flat",
            "purpose": "Venda",
            "price": 680000.00,
            "condo_fee": 580.00,
            "iptu": 180.00,
            "area": 45,
            "area_total": 65,
            "bedrooms": 1,
            "suites": 1,
            "bathrooms": 1,
            "garage": 1,
            "garage_type": "1 Vaga coberta com manobrista",
            "solar_position": "Face Norte",
            "floor_number": "12º Andar",
            "total_floors": 18,
            "condominium_name": "Studio Design Vila Madalena",
            "is_financeable": True,
            "accepts_exchange": True,
            "furnished": "Mobiliado & Decorado para Renda",
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Vila Madalena",
            "address": "Rua Harmonia, 310",
            "zip_code": "05435-000",
            "latitude": -23.5539,
            "longitude": -46.6908,
            "featured": False,
            "status": "Disponível",
            "badge": "Investimento",
            "description": "Studio inteligente com planta otimizada e marcenaria funcional de altíssima qualidade na Vila Madalena. Excelente opção para moradia prática ou investimento em locações de curta e média temporada (Airbnb/Short Stay) com projeção de rentabilidade acima do CDI. Edifício conceito a poucos metros da estação de metrô e dos melhores cafés da região.",
            "amenities_property": [
                "Marcenaria Inteligente com Cama Rebatível",
                "Fechadura Digital Conectada via App",
                "Cozinha Equipada com Eletrodomésticos Embutidos",
                "Ar Condicionado Split Inverter Quente/Frio",
                "Varanda com Vista para a Copa das Árvores",
                "Isolamento Acústico nas Paredes e Janelas"
            ],
            "amenities_condo": [
                "Rooftop Lounge com Piscina de Borda Infinita",
                "Espaço Coworking 24h com Wi-Fi de Alta Velocidade",
                "Lavanderia Compartilhada Inteligente",
                "Pet Place com Área de Banho",
                "Academia Completa com Vista Panorâmica",
                "Bicicletário com Oficina de Reparos",
                "Mercadinho Autônomo 24h (Grab and Go)"
            ],
            "amenities": [
                "Rooftop Lounge", "Lavanderia Compartilhada", "Bicicletário",
                "Pet Place", "Academia", "Metrô Próximo"
            ],
            "image": "img_prop_4.jpg",
            "gallery": ["img_prop_4.jpg", "img_prop_3.jpg", "img_prop_2.jpg", "img_prop_1.jpg"],
            "agent": {
                "name": "Fernanda Lima",
                "creci": "CRECI 195.430-F",
                "phone": "(11) 97654-3210",
                "email": "fernanda@7ximoveis.com.br",
                "avatar": "agent_2.jpg"
            }
        },
        {
            "id": 5,
            "reference": "7X-CO505",
            "title": "Conjunto Comercial Corporate Faria Lima",
            "slug": "conjunto-comercial-corporate-faria-lima",
            "type": "Comercial",
            "subtype": "Laje Corporativa Triple A",
            "purpose": "Aluguel",
            "price": 25000.00,
            "condo_fee": 4200.00,
            "iptu": 1500.00,
            "area": 280,
            "area_total": 390,
            "bedrooms": 0,
            "suites": 0,
            "bathrooms": 4,
            "garage": 6,
            "garage_type": "6 Vagas no subsolo com valet",
            "solar_position": "Face Leste",
            "floor_number": "15º Andar",
            "total_floors": 28,
            "condominium_name": "Faria Lima Financial Center",
            "is_financeable": False,
            "accepts_exchange": False,
            "furnished": "Pronto para Ocupação (Plug & Play)",
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Itaim Bibi",
            "address": "Av. Brig. Faria Lima, 3400",
            "zip_code": "04538-133",
            "latitude": -23.5872,
            "longitude": -46.6811,
            "featured": False,
            "status": "Disponível",
            "badge": "Triple A",
            "description": "Laje corporativa de alto padrão pronta para ocupação imediata em edifício Triple A na Avenida Faria Lima. Layout versátil com salas de reunião privativas envidraçadas, open space para até 45 posições de trabalho, copa executiva e banheiros acessíveis. Infraestrutura tecnológica de ponta com piso elevado, cabeamento estruturado Cat6A e gerador de emergência para 100% da carga.",
            "amenities_property": [
                "Piso Elevado com Acabamento Vinílico Novo",
                "Forro Mineral com Iluminação em LED",
                "Sistema de Ar Condicionado VRF Central",
                "Copa Executiva Completa com Armários",
                "Salas de Reunião com Isolamento Acústico",
                "Cabeamento Estruturado e Rack de TI Dedicado"
            ],
            "amenities_condo": [
                "Edifício Corporativo Class AAA com Certificação LEED",
                "Heliponto Homologado para Grandes Aeronaves",
                "Auditório para 120 Pessoas com Foyer",
                "Segurança Biométrica e Catracas com QR Code",
                "Estacionamento Rotativo com Serviço de Valet",
                "Bicicletário com Vestiários Completos",
                "Restaurante Executivo e Café no Térreo"
            ],
            "amenities": [
                "Edifício Triple A", "Heliponto", "Certificação LEED",
                "Piso Elevado", "Segurança 24h", "Estacionamento Valet"
            ],
            "image": "img_prop_1.jpg",
            "gallery": ["img_prop_1.jpg", "img_prop_3.jpg", "img_prop_4.jpg"],
            "agent": {
                "name": "Carlos Eduardo",
                "creci": "CRECI 162.880-F",
                "phone": "(11) 96543-2109",
                "email": "carlos@7ximoveis.com.br",
                "avatar": "agent_3.jpg"
            }
        },
        {
            "id": 6,
            "reference": "7X-CA601",
            "title": "Residência Minimalista nos Jardins",
            "slug": "residencia-minimalista-nos-jardins",
            "type": "Casa",
            "subtype": "Casa Térrea / Residência Unifamiliar",
            "purpose": "Venda",
            "price": 6200000.00,
            "condo_fee": 0.00,
            "iptu": 2100.00,
            "area": 520,
            "area_total": 780,
            "bedrooms": 4,
            "suites": 4,
            "bathrooms": 6,
            "garage": 4,
            "garage_type": "4 Vagas cobertas",
            "solar_position": "Face Norte",
            "floor_number": "Térrea com Mezanino",
            "total_floors": 1,
            "condominium_name": "Rua Exclusiva Jardins",
            "is_financeable": True,
            "accepts_exchange": True,
            "furnished": "Mobiliário Fixo de Alto Padrão",
            "city": "São Paulo",
            "state": "SP",
            "neighborhood": "Jardins",
            "address": "Rua Colômbia, 155",
            "zip_code": "01438-000",
            "latitude": -23.5701,
            "longitude": -46.6718,
            "featured": True,
            "status": "Disponível",
            "badge": "Alto Padrão",
            "description": "Obra-prima da arquitetura contemporânea nos Jardins. Casa térrea com volumetria pura, concreto aparente e painéis ripados em madeira Cumaru. Pátio central arborizado que integra os setores íntimo e social ao redor de uma piscina aquecida revestida em pedra hijau. Cozinha gourmet equipada com eletros Viking, suíte master com jardim privativo, closet duplo e banheiro spa.",
            "amenities_property": [
                "Piscina Aquecida em Pedra Hijau Vulcânica",
                "Pátio Central com Jardim Japonês & Espelho d'Água",
                "Cozinha Gourmet Equipada com Eletros Viking",
                "Suíte Master com Banheiro Spa e Jardim Privativo",
                "Guarita de Segurança Blindada com CFTV",
                "Painéis Solares e Sistema de Captação de Água de Chuva",
                "Piso em Madeira Maciça de Demolição",
                "Lareira a Lenha Suspensa em Aço Corten"
            ],
            "amenities_condo": [
                "Rua Arborizada com Monitoramento Privado",
                "Próximo ao Clube Paulistano e Restaurantes Estrelados",
                "Vigilância 24 Horas com Ronda Motorizada"
            ],
            "amenities": [
                "Piscina Aquecida", "Jardim de Inverno", "Guarita Blindada",
                "Cozinha Viking", "Energia Solar", "Suíte Master Spa"
            ],
            "image": "img_prop_2.jpg",
            "gallery": ["img_prop_2.jpg", "img_prop_1.jpg", "img_prop_3.jpg", "img_prop_4.jpg"],
            "agent": {
                "name": "Fernanda Lima",
                "creci": "CRECI 195.430-F",
                "phone": "(11) 97654-3210",
                "email": "fernanda@7ximoveis.com.br",
                "avatar": "agent_2.jpg"
            }
        }
    ]

    @classmethod
    def calculate_category(cls, prop):
        if prop.get('is_exclusive', False):
            return "Exclusivo"
        
        try:
            price = float(prop.get('price', 0))
        except (ValueError, TypeError):
            price = 0
            
        try:
            area = float(prop.get('area', 0))
        except (ValueError, TypeError):
            area = 0
            
        try:
            suites = int(prop.get('suites', 0))
        except (ValueError, TypeError):
            suites = 0
            
        if price >= 3000000 or (area >= 200 and suites >= 3):
            return "Alto Padrão"
            
        if prop.get('featured', False):
            return "Destaque"
            
        return "Geral"

    @classmethod
    def get_all(cls):
        # Check if Tecimobi API returns items
        result = TecimobService.fetch_properties()
        if result:
            props = result.get('properties', [])
        else:
            props = cls._properties
            
        for p in props:
            p['calculated_category'] = cls.calculate_category(p)
            
        return props

    @classmethod
    def toggle_exclusive(cls, property_id):
        # Only works for local mock data for this demo
        try:
            pid = int(property_id)
            match = next((p for p in cls._properties if p['id'] == pid), None)
            if match:
                current = match.get('is_exclusive', False)
                match['is_exclusive'] = not current
                match['calculated_category'] = cls.calculate_category(match)
                return match['is_exclusive']
        except (ValueError, TypeError):
            pass
        return None

    @classmethod
    def get_featured(cls):
        all_props = cls.get_all()
        return [p for p in all_props if p.get('featured', False)] or all_props[:3]

    @classmethod
    def get_by_id(cls, property_id):
        # Try Tecimobi API first if active
        tecimobi_prop = TecimobService.fetch_property_by_id(str(property_id))
        if tecimobi_prop:
            tecimobi_prop['calculated_category'] = cls.calculate_category(tecimobi_prop)
            return tecimobi_prop

        # Search by int ID
        try:
            pid = int(property_id)
            match = next((p for p in cls._properties if p['id'] == pid), None)
            if match:
                match['calculated_category'] = cls.calculate_category(match)
                return match
        except (ValueError, TypeError):
            pass

        # Search by string UUID or reference or slug
        s_id = str(property_id).strip().lower()
        match = next((p for p in cls._properties if
                      str(p.get('id', '')).lower() == s_id or
                      str(p.get('reference', '')).lower() == s_id or
                      str(p.get('slug', '')).lower() == s_id), None)
        if match:
            match['calculated_category'] = cls.calculate_category(match)
        return match

    @classmethod
    def get_by_slug(cls, slug):
        all_props = cls.get_all()
        return next((p for p in all_props if p.get('slug') == slug), None)

    @classmethod
    def filter(cls, search_query="", prop_type="", purpose="", min_price=None, max_price=None,
               bedrooms=None, suites=None, bathrooms=None, garage=None,
               min_area=None, max_area=None,
               city="", neighborhood="",
               financeable=None, exchange=None, furnished=None,
               sort_by="recent", category=None):
        results = cls.get_all().copy()

        # Category
        if category and category.lower() != "todas":
            results = [p for p in results if p.get('calculated_category', '').lower() == category.lower()]

        # Text search
        if search_query:
            q = search_query.lower()
            results = [
                p for p in results if
                q in str(p.get('title', '')).lower() or
                q in str(p.get('reference', '')).lower() or
                q in str(p.get('neighborhood', '')).lower() or
                q in str(p.get('city', '')).lower() or
                q in str(p.get('description', '')).lower() or
                q in str(p.get('type', '')).lower() or
                q in str(p.get('condominium_name', '')).lower()
            ]

        # Property type
        if prop_type and prop_type.lower() != "todos":
            results = [p for p in results if p.get('type', '').lower() == prop_type.lower()]

        # Purpose
        if purpose and purpose.lower() != "todos":
            results = [p for p in results if p.get('purpose', '').lower() == purpose.lower()]

        # City
        if city and city.lower() != "todas":
            results = [p for p in results if p.get('city', '').lower() == city.lower()]

        # Neighborhood
        if neighborhood and neighborhood.lower() != "todos":
            results = [p for p in results if p.get('neighborhood', '').lower() == neighborhood.lower()]

        # Min Price
        if min_price is not None and min_price != "":
            try:
                results = [p for p in results if p.get('price', 0) >= float(min_price)]
            except (ValueError, TypeError):
                pass

        # Max Price
        if max_price is not None and max_price != "":
            try:
                results = [p for p in results if p.get('price', 0) <= float(max_price)]
            except (ValueError, TypeError):
                pass

        # Bedrooms
        if bedrooms is not None and bedrooms != "":
            try:
                results = [p for p in results if p.get('bedrooms', 0) >= int(bedrooms)]
            except (ValueError, TypeError):
                pass

        # Suites
        if suites is not None and suites != "":
            try:
                results = [p for p in results if p.get('suites', 0) >= int(suites)]
            except (ValueError, TypeError):
                pass

        # Bathrooms
        if bathrooms is not None and bathrooms != "":
            try:
                results = [p for p in results if p.get('bathrooms', 0) >= int(bathrooms)]
            except (ValueError, TypeError):
                pass

        # Garage / vagas
        if garage is not None and garage != "":
            try:
                results = [p for p in results if p.get('garage', 0) >= int(garage)]
            except (ValueError, TypeError):
                pass

        # Min Area
        if min_area is not None and min_area != "":
            try:
                results = [p for p in results if p.get('area', 0) >= float(min_area)]
            except (ValueError, TypeError):
                pass

        # Max Area
        if max_area is not None and max_area != "":
            try:
                results = [p for p in results if p.get('area', 0) <= float(max_area)]
            except (ValueError, TypeError):
                pass

        # Financeable
        if financeable == '1':
            results = [p for p in results if p.get('is_financeable', False)]

        # Accepts Exchange
        if exchange == '1':
            results = [p for p in results if p.get('accepts_exchange', False)]

        # Furnished
        if furnished == '1':
            results = [p for p in results if
                       p.get('furnished') and p.get('furnished') != 'Não mobiliado']

        # Sorting — accept both hyphen and underscore variants
        sort_key = sort_by.replace('-', '_')
        if sort_key == "price_asc":
            results.sort(key=lambda x: x.get('price', 0))
        elif sort_key == "price_desc":
            results.sort(key=lambda x: x.get('price', 0), reverse=True)
        elif sort_key == "area_desc":
            results.sort(key=lambda x: x.get('area', 0), reverse=True)
        else:  # 'recent'
            results.sort(key=lambda x: str(x.get('id', 0)), reverse=True)

        return results

    @classmethod
    def get_cities(cls):
        props = cls.get_all()
        return sorted(list(set(p.get('city', '') for p in props if p.get('city'))))

    @classmethod
    def get_types(cls):
        props = cls.get_all()
        return sorted(list(set(p.get('type', '') for p in props if p.get('type'))))

    @classmethod
    def get_neighborhoods(cls):
        props = cls.get_all()
        return sorted(list(set(p.get('neighborhood', '') for p in props if p.get('neighborhood'))))
