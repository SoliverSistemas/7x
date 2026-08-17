import os
import json
import re
import urllib.request
import urllib.error
from flask import current_app

class TecimobService:
    """
    Serviço de integração com a API Pública do Tecimob.

    Documentação oficial (Swagger): https://swagger.tecimob.com.br
    URL base: https://api.tecimob.com.br/v1
    Autenticação: Bearer Token (Authorization: Bearer <token>)

    Endpoints usados:
      - GET /api/properties             -> Listagem paginada de imóveis
      - GET /api/properties/{uuid}      -> Detalhe completo de um imóvel
      - POST /api/leads/store-person    -> Envio de lead (visitante interessado)
    """

    BASE_URL = 'https://api.tecimob.com.br/v1'

    @classmethod
    def _get_token(cls):
        return (current_app.config.get('TECIMOB_API_TOKEN') or
                os.getenv('TECIMOB_API_TOKEN', ''))

    @classmethod
    def _is_active(cls):
        return bool(
            current_app.config.get('USE_TECIMOB_API', False) and
            cls._get_token()
        )

    @classmethod
    def _headers(cls):
        return {
            'Authorization': f'Bearer {cls._get_token()}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': '7XImoveis-Site/1.0'
        }

    @classmethod
    def _get(cls, path, params=None):
        """
        Realiza GET na API Tecimob e retorna o dict JSON parseado, ou None em caso de falha.
        """
        url = f"{cls.BASE_URL}{path}"
        if params:
            qs = '&'.join(f"{k}={v}" for k, v in params.items() if v is not None)
            if qs:
                url = f"{url}?{qs}"
        try:
            req = urllib.request.Request(url, headers=cls._headers())
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode('utf-8')
                return json.loads(body)
        except urllib.error.HTTPError as e:
            current_app.logger.warning(f"[Tecimob] HTTP {e.code} em {url}: {e.reason}")
            return None
        except Exception as e:
            current_app.logger.error(f"[Tecimob] Erro ao acessar {url}: {e}")
            return None

    @classmethod
    def _post(cls, path, payload):
        """Realiza POST na API Tecimob."""
        url = f"{cls.BASE_URL}{path}"
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=cls._headers(), method='POST')
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode('utf-8')
                return json.loads(body)
        except Exception as e:
            current_app.logger.error(f"[Tecimob] Erro ao POST {url}: {e}")
            return None

    # ─────────────────────────────────────────────
    # MÉTODO PÚBLICO: Listagem com filtros reais da API
    # ─────────────────────────────────────────────
    @classmethod
    def fetch_properties(cls, page=1, per_page=20, transaction=None, city=None,
                         neighborhood=None, price_gte=None, price_lte=None,
                         bedroom_qty=None, prop_type=None, status='disponivel',
                         min_area=None, max_area=None, reference=None):
        """
        Busca imóveis via GET /api/properties
        Filtros suportados pela API Tecimob:
          - filter[transaction]: 'venda' | 'aluguel' | 'temporada'
          - filter[neighborhood.city.name]: nome da cidade
          - filter[neighborhood.name]: nome do bairro
          - filter[price]: '>=' ou '<=' com valor inteiro
          - filter[by_room][bedroom][value]: número de quartos
          - filter[by_room][bedroom][filter]: 'greater_equals'
          - filter[subtype.type.title]: tipo do imóvel (ex: Residencial)
          - filter[status]: 'disponivel' | 'vendido' | 'alugado' | 'excluido'
          - filter[by_area][built_area][greater_equals]: min_area
          - filter[by_area][built_area][lower_equals]: max_area
          - filter[reference]: reference
        """
        if not cls._is_active():
            return None

        params = {'page': page, 'per_page': per_page}

        if status:
            params['filter[status]'] = status
        if transaction:
            params['filter[transaction]'] = transaction.lower()
        if city:
            params['filter[neighborhood.city.name]'] = city
        if neighborhood:
            params['filter[neighborhood.name]'] = neighborhood
        if price_gte:
            params['filter[price]'] = f'>={price_gte}'
        if bedroom_qty:
            params['filter[by_room][bedroom][value]'] = bedroom_qty
            params['filter[by_room][bedroom][filter]'] = 'greater_equals'
        if prop_type:
            params['filter[subtype.type.title]'] = prop_type
        if min_area:
            params['filter[by_area][built_area][greater_equals]'] = min_area
        if max_area:
            params['filter[by_area][built_area][lower_equals]'] = max_area
        if reference:
            params['filter[reference]'] = reference

        data = cls._get('/api/properties', params=params)
        if not data:
            return None

        items = data.get('data', [])
        meta = data.get('meta', {})
        return {
            'properties': [cls.normalize(item, detailed=False) for item in items],
            'total': meta.get('total', len(items)),
            'current_page': meta.get('current_page', 1),
            'last_page': meta.get('last_page', 1),
            'per_page': meta.get('per_page', per_page),
        }

    @classmethod
    def fetch_property_by_id(cls, property_uuid):
        """
        Busca detalhe completo de um imóvel via GET /api/properties/{id}
        O id é um UUID (string).
        """
        if not cls._is_active():
            return None
        data = cls._get(f'/api/properties/{property_uuid}')
        if not data or 'data' not in data:
            return None
        return cls.normalize(data['data'], detailed=True)

    @classmethod
    def send_lead(cls, name, phone, email=None, property_id=None, message=None):
        """
        Registra um Lead (visitante/interessado) via POST /api/leads/store-person
        """
        if not cls._is_active():
            return False

        ddd = ''
        number = phone
        if len(phone) >= 11:
            ddd = phone[:2]
            number = phone[2:]

        payload = {
            "name": name,
            "phones": [{"ddi": 55, "number": f"{ddd}{number}", "description": "Celular/WhatsApp"}]
        }
        if email:
            payload["email"] = email

        result = cls._post('/api/leads/store-person', payload)

        # Se tiver property_id, relate o lead ao imóvel
        if result and property_id:
            person_id = (result.get('data') or {}).get('id')
            if person_id:
                cls._post('/api/leads/relate-person', {
                    "person_id": person_id,
                    "property_id": str(property_id),
                    "note": message or "Interesse via site 7X Imóveis"
                })
        return bool(result)

    # ─────────────────────────────────────────────
    # NORMALIZADOR: campos reais da API → modelo 7X
    # ─────────────────────────────────────────────
    @classmethod
    def normalize(cls, item, detailed=False):
        """
        Converte o payload real da API Tecimob para o formato interno 7X Imóveis.

        Campos da API (listagem e detalhe):
          id, price, transaction, reference, url, status
          street_address, street_number, zip_code, complement_address
          neighborhood.name → neighborhood.city.name → neighborhood.city.state.acronym
          type, subtype
          user.name, user.email, user.cellphone, user.creci, user.file_url
          characteristics[]  → {title, quantity}  (quartos, garagem, suíte, etc.)
          condo_characteristics[] → idem, para condomínio
          [detalhe apenas]:
            description, areas[], rooms, condominium_price, territorial_tax_price
            informations[], is_financeable, has_furniture, furniture_note
            maps_latitude, maps_longitude, situation, solar_position
        """
        if not item:
            return None

        # ── Localização ────────────────────────────────
        nbhood = item.get('neighborhood') or {}
        city_obj = nbhood.get('city') or {}
        state_obj = city_obj.get('state') or {}

        neighborhood_name = nbhood.get('name', 'Centro')
        city_name = city_obj.get('name', 'São Paulo')
        state_acronym = state_obj.get('acronym', 'SP')
        street = item.get('street_address') or ''
        number = item.get('street_number') or ''
        address_full = f"{street}, {number}".strip(', ') if street else 'Endereço não informado'

        # ── Preço ──────────────────────────────────────
        # A API retorna price como string formatada: "R$ 300.000,00"
        raw_price = item.get('price', '') or ''
        numeric_price = 0.0
        try:
            clean = re.sub(r'[^\d,]', '', raw_price).replace(',', '.')
            # Handle "300.000.00" → strip last dot if has 2 decimals
            parts = clean.split('.')
            if len(parts) > 2:
                clean = ''.join(parts[:-1]) + '.' + parts[-1]
            numeric_price = float(clean)
        except (ValueError, AttributeError):
            numeric_price = 0.0

        # ── Transação/Finalidade ────────────────────────
        transaction = (item.get('transaction') or 'VENDA').upper()
        purpose_map = {'VENDA': 'Venda', 'ALUGUEL': 'Aluguel', 'TEMPORADA': 'Temporada'}
        purpose = purpose_map.get(transaction, 'Venda')

        # ── Tipo/Subtipo ───────────────────────────────
        prop_type = item.get('type') or item.get('subtype') or 'Imóvel'

        # ── Características (quartos, suítes, banheiros, vagas, área) ──
        characteristics = item.get('characteristics') or []
        rooms_map = {}
        for c in characteristics:
            title_lower = (c.get('title') or '').lower()
            qty = c.get('quantity')
            if qty is not None:
                rooms_map[title_lower] = qty

        # Extrair áreas (somente no detalhe)
        areas = item.get('areas') or []
        area_built = 0
        area_total = 0
        for a in areas:
            name = (a.get('name') or '').lower()
            val = a.get('value') or 0
            if 'built' in name or 'construida' in name or 'util' in name:
                area_built = val
            elif 'total' in name:
                area_total = val
        area = area_built or area_total or 0

        # Rooms também pode vir como array no detalhe
        rooms_detail = item.get('rooms') or []
        if isinstance(rooms_detail, list):
            for r in rooms_detail:
                title_lower = (r.get('title') or '').lower()
                qty = r.get('quantity')
                if qty is not None:
                    rooms_map[title_lower] = qty

        bedrooms = int(rooms_map.get('quartos', rooms_map.get('dormitórios',
                       rooms_map.get('dormitorios', 0))) or 0)
        suites = int(rooms_map.get('suítes', rooms_map.get('suites', 0)) or 0)
        bathrooms = int(rooms_map.get('banheiros', 0) or 0)
        garage = int(rooms_map.get('vagas', rooms_map.get('garagem', 0)) or 0)

        # ── Imagens ───────────────────────────────────
        # Na listagem: sem imagens (campo 'images' só vem no detalhe)
        # No detalhe: item['images'] = [{file_url, order, gallery}, ...]
        images_list = item.get('images') or []
        gallery_urls = []
        if images_list:
            # Ordenar por 'order' e pegar file_url
            sorted_imgs = sorted(images_list, key=lambda x: x.get('order', 999))
            gallery_urls = [img['file_url'] for img in sorted_imgs if img.get('file_url')]
        else:
            # Fallback: busca em informations (campo legado)
            informations = item.get('informations') or []
            for info in informations:
                if 'imagem' in (info.get('name') or '').lower() or info.get('name') == 'images':
                    v = info.get('value')
                    if isinstance(v, list):
                        gallery_urls.extend(v)
                    elif isinstance(v, str) and v.startswith('http'):
                        gallery_urls.append(v)

        prop_url = item.get('url') or ''
        main_image = gallery_urls[0] if gallery_urls else None

        # ── Corretor ──────────────────────────────────
        user = item.get('user') or {}
        cellphone = user.get('cellphone') or ''
        if cellphone and user.get('cellphone_ddi'):
            cellphone = f"+{user.get('cellphone_ddi')} {cellphone}"

        agent = {
            'name': user.get('name') or 'Atendimento 7X Imóveis',
            'phone': cellphone or '(11) 99999-7777',
            'email': user.get('email') or 'contato@7ximoveis.com.br',
            'creci': user.get('creci') or '',
            'avatar_url': user.get('file_url') or ''
        }

        # ── Comodidades (características + condomínio) ──
        condo_chars = item.get('condo_characteristics') or []
        amenities_property = [c['title'] for c in characteristics if c.get('title') and not c.get('quantity')]
        amenities_condo = [c['title'] for c in condo_chars if c.get('title') and not c.get('quantity')]
        all_chars = characteristics + condo_chars
        amenities = [c['title'] for c in all_chars if c.get('title') and not c.get('quantity')]
        if not amenities:
            amenities = ['Portaria 24h', 'Garagem Coberta']
        if not amenities_property:
            amenities_property = amenities[:4]
        if not amenities_condo:
            amenities_condo = amenities[4:] or ['Portaria 24h', 'Segurança']

        # ── Dados exclusivos do detalhe ───────────────
        description = ''
        condominium_price = 0.0
        iptu_price = 0.0
        is_financeable = False
        accepts_exchange = False
        latitude = None
        longitude = None
        situation = ''
        condominium_name = ''
        solar_position = item.get('solar_position') or ''
        furnished = item.get('furniture_note') or ('Mobiliado' if item.get('has_furniture') else 'Não Mobiliado')
        floor_number = item.get('floor') or ''

        if detailed:
            raw_desc = item.get('description') or ''
            # Remove HTML tags se vier com HTML
            description = re.sub(r'<[^>]+>', '', raw_desc).strip()

            raw_condo = item.get('condominium_price') or ''
            try:
                clean_c = re.sub(r'[^\d,]', '', raw_condo).replace(',', '.')
                condominium_price = float(clean_c) if clean_c else 0.0
            except ValueError:
                condominium_price = 0.0

            raw_iptu = item.get('territorial_tax_price') or ''
            try:
                clean_i = re.sub(r'[^\d,]', '', raw_iptu).replace(',', '.')
                iptu_price = float(clean_i) if clean_i else 0.0
            except ValueError:
                iptu_price = 0.0

            is_financeable = bool(item.get('is_financeable'))
            accepts_exchange = bool(item.get('accepts_exchange') or item.get('permuta'))
            latitude = item.get('maps_latitude')
            longitude = item.get('maps_longitude')
            situation = item.get('situation') or ''

            condo_obj = item.get('condominium') or {}
            condominium_name = condo_obj.get('title') or ''

        return {
            # Identificação
            'id': item.get('id', ''),
            'reference': item.get('reference', ''),
            'slug': f"imovel-{item.get('reference') or item.get('id', 'sem-ref')}",
            'title': cls._build_title(prop_type, neighborhood_name, city_name, item.get('reference')),
            'url_tecimob': prop_url,

            # Tipologia
            'type': prop_type,
            'subtype': item.get('subtype') or prop_type,
            'purpose': purpose,
            'status': item.get('status') or 'Disponível',
            'badge': situation or '',

            # Localização
            'address': address_full,
            'neighborhood': neighborhood_name,
            'city': city_name,
            'state': state_acronym,
            'zip_code': item.get('zip_code') or '',
            'latitude': latitude,
            'longitude': longitude,

            # Preços e Condições
            'price': numeric_price,
            'price_formatted': raw_price,
            'condo_fee': condominium_price,
            'iptu': iptu_price,
            'is_financeable': is_financeable,
            'accepts_exchange': accepts_exchange,
            'condominium_name': condominium_name,
            'furnished': furnished,
            'solar_position': solar_position,
            'floor_number': floor_number,

            # Características
            'area': area,
            'area_total': area_total or area,
            'bedrooms': bedrooms,
            'suites': suites,
            'bathrooms': bathrooms,
            'garage': garage,
            'garage_type': f"{garage} vaga{'s' if garage != 1 else ''}" if garage else 'Sem vaga',

            # Conteúdo
            'description': description,
            'amenities': amenities,
            'amenities_property': amenities_property,
            'amenities_condo': amenities_condo,
            'featured': False,

            # Imagens
            'image': main_image,
            'gallery': gallery_urls if gallery_urls else [main_image],

            # Agente/Corretor
            'agent': agent
        }

    @classmethod
    def _build_title(cls, prop_type, neighborhood, city, reference):
        """Gera um título descritivo quando a API não fornece um campo 'title' direto."""
        parts = [p for p in [prop_type, 'em', neighborhood, '-', city] if p]
        title = ' '.join(parts)
        if reference:
            title = f"{title} (Ref: {reference})"
        return title
