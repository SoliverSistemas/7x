from flask import Blueprint, render_template, request, abort
from app.models.property_model import PropertyRepository

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/')
def list_properties():
    page        = request.args.get('page', 1, type=int)
    query       = request.args.get('q', '')
    prop_type   = request.args.get('type', '')
    purpose     = request.args.get('purpose', '')
    city        = request.args.get('city', '')
    neighborhood= request.args.get('neighborhood', '')
    min_price   = request.args.get('min_price', None)
    max_price   = request.args.get('max_price', None)
    bedrooms    = request.args.get('bedrooms', None)
    suites      = request.args.get('suites', None)
    bathrooms   = request.args.get('bathrooms', None)
    garage      = request.args.get('garage', None)
    min_area    = request.args.get('min_area', None)
    max_area    = request.args.get('max_area', None)
    financeable = request.args.get('financeable', None)
    exchange    = request.args.get('exchange', None)
    furnished   = request.args.get('furnished', None)
    sort_by     = request.args.get('sort', 'recent')
    category    = request.args.get('category', '')

    filter_results = PropertyRepository.filter(
        page=page,
        per_page=12,
        search_query=query,
        prop_type=prop_type,
        purpose=purpose,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        suites=suites,
        bathrooms=bathrooms,
        garage=garage,
        min_area=min_area,
        max_area=max_area,
        city=city,
        neighborhood=neighborhood,
        financeable=financeable,
        exchange=exchange,
        furnished=furnished,
        sort_by=sort_by,
        category=category
    )

    cities        = PropertyRepository.get_cities()
    types         = PropertyRepository.get_types()
    neighborhoods = PropertyRepository.get_neighborhoods()

    return render_template(
        'properties/index.html',
        properties=filter_results['properties'],
        pagination=filter_results,
        cities=cities,
        types=types,
        neighborhoods=neighborhoods,
        current_filters={
            'query':        query,
            'type':         prop_type,
            'purpose':      purpose,
            'city':         city,
            'neighborhood': neighborhood,
            'min_price':    min_price or '',
            'max_price':    max_price or '',
            'bedrooms':     bedrooms or '',
            'suites':       suites or '',
            'bathrooms':    bathrooms or '',
            'garage':       garage or '',
            'min_area':     min_area or '',
            'max_area':     max_area or '',
            'financeable':  financeable or '',
            'exchange':     exchange or '',
            'furnished':    furnished or '',
            'sort':         sort_by,
            'category':     category,
        }
    )


@properties_bp.route('/<property_id>')
def detail(property_id):
    prop = PropertyRepository.get_by_id(property_id)
    if not prop:
        abort(404)
    
    # Calculate price per square meter
    price = prop.get('price', 0)
    area = prop.get('area', 0)
    price_per_sqm = (price / area) if (price and area and area > 0) else 0

    # Total monthly cost estimation (Condomínio + IPTU)
    condo = prop.get('condo_fee', 0) or 0
    iptu = prop.get('iptu', 0) or 0
    monthly_cost = condo + iptu

    # Related properties (same type, city or purpose)
    all_props = PropertyRepository.get_all()
    related = [p for p in all_props if str(p.get('id')) != str(prop.get('id')) and (p.get('type') == prop.get('type') or p.get('city') == prop.get('city'))][:3]

    return render_template(
        'properties/detail.html',
        property=prop,
        related_properties=related,
        price_per_sqm=price_per_sqm,
        monthly_cost=monthly_cost
    )
