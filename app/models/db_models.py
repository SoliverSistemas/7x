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
