from app import db
from datetime import datetime
import json


class Property(db.Model):
    __tablename__ = 'properties'

    # ID da API Tecimob (geralmente UUID), usaremos como primary_key ou um campo unique.
    # Mas no SQLite, usar uma string UUID como PK é tranquilo.
    id = db.Column(db.String(36), primary_key=True)
    
    reference = db.Column(db.String(50), index=True)
    title = db.Column(db.String(255))
    slug = db.Column(db.String(255), index=True)
    
    type = db.Column(db.String(100), index=True) # Ex: Apartamento, Casa
    subtype = db.Column(db.String(100)) # Ex: Apartamento Padrão
    purpose = db.Column(db.String(50), index=True) # Venda, Aluguel
    
    price = db.Column(db.Float, index=True)
    condo_fee = db.Column(db.Float)
    iptu = db.Column(db.Float)
    
    area = db.Column(db.Float, index=True)
    area_total = db.Column(db.Float)
    
    bedrooms = db.Column(db.Integer, index=True)
    suites = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    garage = db.Column(db.Integer)
    garage_type = db.Column(db.String(100))
    
    solar_position = db.Column(db.String(50))
    floor_number = db.Column(db.String(50))
    total_floors = db.Column(db.Integer)
    condominium_name = db.Column(db.String(255))
    profile = db.Column(db.String(50))  # Residencial, Comercial
    situation = db.Column(db.String(100))  # Pronto para morar, Em construção, etc.
    is_corner = db.Column(db.Boolean, default=False)  # imóvel de esquina
    is_deeded = db.Column(db.Boolean, default=False)  # escriturado
    is_titled = db.Column(db.Boolean, default=False)  # titulado
    total_monthly_cost = db.Column(db.Float)  # total_taxes_price da API
    iptu_type = db.Column(db.String(20))  # Mensal/Anual
    
    is_financeable = db.Column(db.Boolean, default=False)
    accepts_exchange = db.Column(db.Boolean, default=False)
    furnished = db.Column(db.String(100)) # Semi-mobiliado, Não mobiliado, etc.
    
    city = db.Column(db.String(100), index=True)
    state = db.Column(db.String(2))
    neighborhood = db.Column(db.String(100), index=True)
    address = db.Column(db.String(255))
    zip_code = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='Disponível')
    badge = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    # Store lists and dicts as JSON encoded text
    _amenities_property = db.Column('amenities_property', db.Text)
    _amenities_condo = db.Column('amenities_condo', db.Text)
    _amenities = db.Column('amenities', db.Text)
    _gallery = db.Column('gallery', db.Text)
    _agent = db.Column('agent', db.Text)
    _establishments = db.Column('establishments', db.Text)  # vizinhança: Banco, Escola...
    
    image = db.Column(db.String(500)) # Main image URL
    calculated_category = db.Column(db.String(50))
    is_exclusive = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Properties to handle JSON serialization transparently
    @property
    def amenities_property(self):
        return json.loads(self._amenities_property) if self._amenities_property else []

    @amenities_property.setter
    def amenities_property(self, value):
        self._amenities_property = json.dumps(value) if value else '[]'

    @property
    def amenities_condo(self):
        return json.loads(self._amenities_condo) if self._amenities_condo else []

    @amenities_condo.setter
    def amenities_condo(self, value):
        self._amenities_condo = json.dumps(value) if value else '[]'

    @property
    def amenities(self):
        return json.loads(self._amenities) if self._amenities else []

    @amenities.setter
    def amenities(self, value):
        self._amenities = json.dumps(value) if value else '[]'

    @property
    def gallery(self):
        return json.loads(self._gallery) if self._gallery else []

    @gallery.setter
    def gallery(self, value):
        self._gallery = json.dumps(value) if value else '[]'

    @property
    def agent(self):
        return json.loads(self._agent) if self._agent else {}

    @agent.setter
    def agent(self, value):
        self._agent = json.dumps(value) if value else '{}'

    @property
    def establishments(self):
        return json.loads(self._establishments) if self._establishments else []

    @establishments.setter
    def establishments(self, value):
        self._establishments = json.dumps(value, ensure_ascii=False) if value else '[]'

    def to_dict(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'title': self.title,
            'slug': self.slug,
            'type': self.type,
            'subtype': self.subtype,
            'purpose': self.purpose,
            'price': self.price,
            'condo_fee': self.condo_fee,
            'iptu': self.iptu,
            'total_monthly_cost': self.total_monthly_cost,
            'iptu_type': self.iptu_type,
            'area': self.area,
            'area_total': self.area_total,
            'bedrooms': self.bedrooms,
            'suites': self.suites,
            'bathrooms': self.bathrooms,
            'garage': self.garage,
            'garage_type': self.garage_type,
            'solar_position': self.solar_position,
            'floor_number': self.floor_number,
            'total_floors': self.total_floors,
            'condominium_name': self.condominium_name,
            'profile': self.profile,
            'situation': self.situation,
            'is_corner': self.is_corner,
            'is_deeded': self.is_deeded,
            'is_titled': self.is_titled,
            'is_financeable': self.is_financeable,
            'accepts_exchange': self.accepts_exchange,
            'furnished': self.furnished,
            'city': self.city,
            'state': self.state,
            'neighborhood': self.neighborhood,
            'address': self.address,
            'zip_code': self.zip_code,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'featured': self.featured,
            'status': self.status,
            'badge': self.badge,
            'description': self.description,
            'amenities_property': self.amenities_property,
            'amenities_condo': self.amenities_condo,
            'amenities': self.amenities,
            'establishments': self.establishments,
            'image': self.image,
            'gallery': self.gallery,
            'agent': self.agent,
            'calculated_category': self.calculated_category,
            'is_exclusive': self.is_exclusive,
        }


class ExclusiveCollection(db.Model):
    """
    Define os até 3 imóveis que aparecem na seção 'Coleção Exclusiva' do index.
    Cada item pode ter uma imagem de capa personalizada armazenada no Supabase Storage.
    """
    __tablename__ = 'exclusive_collection'

    id            = db.Column(db.Integer, primary_key=True)
    property_id   = db.Column(db.String(36), db.ForeignKey('properties.id', ondelete='CASCADE'), nullable=False, unique=True)
    cover_url     = db.Column(db.String(500))   # URL pública do Supabase Storage
    display_order = db.Column(db.Integer, default=0)  # 1, 2 ou 3
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento
    property = db.relationship('Property', backref=db.backref('exclusive_slot', uselist=False, lazy='joined'))

    def to_dict(self):
        p = self.property.to_dict() if self.property else {}
        p['exclusive_cover_url'] = self.cover_url  # override de capa
        return p


class Lancamento(db.Model):
    """
    Representa um lançamento imobiliário gerenciado pelo painel admin.
    Máximo de 10 registros ativos.
    """
    __tablename__ = 'lancamentos'

    id            = db.Column(db.Integer, primary_key=True)
    slug          = db.Column(db.String(255), unique=True, nullable=False, index=True)

    # ── Dados do card (exibidos no index e na listagem) ──────────────────
    name          = db.Column(db.String(255), nullable=False)
    tagline       = db.Column(db.String(500))
    location      = db.Column(db.String(255))   # Ex: "Ipanema · Rio de Janeiro"
    type          = db.Column(db.String(100))   # Ex: "Alto Padrão", "Cobertura"
    status        = db.Column(db.String(100))   # Ex: "Lançamento", "Pré-lançamento"
    units         = db.Column(db.String(100))   # Ex: "24 unidades"
    cover_url     = db.Column(db.String(500))   # URL pública Supabase Storage (3:5)

    # ── Dados da página de detalhe ───────────────────────────────────────
    description   = db.Column(db.Text)          # HTML ou texto livre
    _gallery      = db.Column('gallery', db.Text)  # JSON: lista de até 6 URLs

    # ── Controle ──────────────────────────────────────────────────────────
    display_order = db.Column(db.Integer, default=0)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at    = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ── Gallery property ──────────────────────────────────────────────────
    @property
    def gallery(self):
        """Retorna lista de dicts {url, text, title}. Compatível com formato legado."""
        raw = json.loads(self._gallery) if self._gallery else []
        result = []
        for item in raw:
            if isinstance(item, dict):
                result.append({
                    'url':   item.get('url', ''),
                    'text':  item.get('text', ''),
                    'title': item.get('title', ''),
                })
            else:  # legado: string pura
                result.append({'url': str(item), 'text': '', 'title': ''})
        return result

    @gallery.setter
    def gallery(self, value):
        """Aceita lista de dicts {url, text, title} ou strings (compatibilidade)."""
        if not value:
            self._gallery = '[]'
            return
        normalized = []
        for item in value:
            if isinstance(item, dict):
                normalized.append({
                    'url':   item.get('url', ''),
                    'text':  item.get('text', ''),
                    'title': item.get('title', ''),
                })
            else:
                normalized.append({'url': str(item), 'text': '', 'title': ''})
        self._gallery = json.dumps(normalized, ensure_ascii=False)

    def add_gallery_image(self, url: str, text: str = '', title: str = '') -> bool:
        """Adiciona imagem à galeria. Retorna False se já tiver 6."""
        imgs = self.gallery
        if len(imgs) >= 6:
            return False
        imgs.append({'url': url, 'text': text, 'title': title})
        self.gallery = imgs
        return True

    def remove_gallery_image(self, index: int) -> dict | None:
        """Remove imagem pelo índice. Retorna o dict removido ou None."""
        imgs = self.gallery
        removed = None
        if 0 <= index < len(imgs):
            removed = imgs.pop(index)
            self.gallery = imgs
        return removed

    def update_gallery_text(self, index: int, text: str, title: str = None) -> bool:
        """Atualiza texto/título de uma imagem. Retorna False se índice inválido."""
        imgs = self.gallery
        if 0 <= index < len(imgs):
            imgs[index]['text'] = text
            if title is not None:
                imgs[index]['title'] = title
            self.gallery = imgs
            return True
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'name': self.name,
            'tagline': self.tagline,
            'location': self.location,
            'type': self.type,
            'status': self.status,
            'units': self.units,
            'cover_url': self.cover_url,
            'cover': self.cover_url,   # compatibilidade com template legado
            'description': self.description,
            'gallery': self.gallery,
            'display_order': self.display_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class PropertyCategory(db.Model):
    """
    Categorias de imóveis configuráveis pelo admin.
    A lógica de calculate_category() lê desta tabela para classificar imóveis.
    """
    __tablename__ = 'property_categories'

    id               = db.Column(db.Integer, primary_key=True)
    name             = db.Column(db.String(100), nullable=False)          # Ex: "Alto Padrão"
    color            = db.Column(db.String(20), default='#c9ac77')        # Cor hex do badge
    min_price        = db.Column(db.Float, nullable=True)                 # Preço mínimo (None = sem limite inferior)
    max_price        = db.Column(db.Float, nullable=True)                 # Preço máximo (None = sem limite superior)
    priority         = db.Column(db.Integer, default=10, nullable=False)  # Menor número = maior prioridade
    is_exclusive_flag = db.Column(db.Boolean, default=False)              # Se True, aplica a imóveis com is_exclusive=True
    is_featured_flag  = db.Column(db.Boolean, default=False)              # Se True, aplica a imóveis com featured=True
    created_at       = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def matches(self, prop_dict: dict) -> bool:
        """Retorna True se esta categoria se aplica ao imóvel dado."""
        price = prop_dict.get('price') or 0

        # Flag exclusivo
        if self.is_exclusive_flag:
            return bool(prop_dict.get('is_exclusive'))

        # Flag destaque
        if self.is_featured_flag:
            return bool(prop_dict.get('featured'))

        # Faixa de preço
        if self.min_price is not None and price < self.min_price:
            return False
        if self.max_price is not None and price > self.max_price:
            return False
        # Se chegou aqui e tem pelo menos um limite definido, bateu
        if self.min_price is not None or self.max_price is not None:
            return True
        return False

    def to_dict(self) -> dict:
        return {
            'id':               self.id,
            'name':             self.name,
            'color':            self.color,
            'min_price':        self.min_price,
            'max_price':        self.max_price,
            'priority':         self.priority,
            'is_exclusive_flag': self.is_exclusive_flag,
            'is_featured_flag':  self.is_featured_flag,
        }

    def criteria_label(self) -> str:
        """Descrição textual dos critérios para exibição no admin."""
        if self.is_exclusive_flag:
            return 'Imóvel marcado como Exclusivo'
        if self.is_featured_flag:
            return 'Imóvel marcado como Destaque'
        parts = []
        if self.min_price is not None:
            parts.append(f'≥ R$ {self.min_price:,.0f}'.replace(',', '.'))
        if self.max_price is not None:
            parts.append(f'≤ R$ {self.max_price:,.0f}'.replace(',', '.'))
        return ' e '.join(parts) if parts else 'Sem critério de preço (fallback)'

    def __repr__(self):
        return f'<PropertyCategory {self.name}>'


class ChatLead(db.Model):
    """Lead capturado pelo chatbot — nome, telefone e intenção do visitante."""
    __tablename__ = 'chat_leads'

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120))
    phone      = db.Column(db.String(30))
    message    = db.Column(db.Text)           # resumo da conversa / intenção
    page       = db.Column(db.String(300))    # URL da página onde o chat foi iniciado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatLead {self.name} {self.phone}>'


class AgentProfile(db.Model):
    """
    Overrides para o perfil do corretor (nome, avatar, instagram, descrição).
    O campo 'name' atua como chave, combinando com o nome retornado pela Tecimob.
    """
    __tablename__ = 'agent_profiles'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(150), unique=True, nullable=False, index=True)
    avatar_url  = db.Column(db.String(500))
    instagram   = db.Column(db.String(150))
    description = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<AgentProfile {self.name}>'
