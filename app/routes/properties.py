from flask import Blueprint, render_template, request, abort
from app.models.property_model import PropertyRepository

properties_bp = Blueprint('properties', __name__)

@properties_bp.route('/')
def list_properties():
    # Retrieve query parameters
    query = request.args.get('q', '')
    prop_type = request.args.get('type', '')
    purpose = request.args.get('purpose', '')
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    bedrooms = request.args.get('bedrooms', None)
    sort_by = request.args.get('sort', 'recent')

    filtered_properties = PropertyRepository.filter(
        search_query=query,
        prop_type=prop_type,
        purpose=purpose,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        city=city,
        sort_by=sort_by
    )

    cities = PropertyRepository.get_cities()
    types = PropertyRepository.get_types()
    neighborhoods = PropertyRepository.get_neighborhoods()

    return render_template(
        'properties/index.html',
        properties=filtered_properties,
        cities=cities,
        types=types,
        neighborhoods=neighborhoods,
        current_filters={
            'query': query,
            'type': prop_type,
            'purpose': purpose,
            'city': city,
            'min_price': min_price or '',
            'max_price': max_price or '',
            'bedrooms': bedrooms or '',
            'sort': sort_by
        }
    )

@properties_bp.route('/<int:property_id>')
def detail(property_id):
    prop = PropertyRepository.get_by_id(property_id)
    if not prop:
        abort(404)
    
    # Related properties (same type or neighborhood)
    all_props = PropertyRepository.get_all()
    related = [p for p in all_props if p['id'] != prop['id'] and (p['type'] == prop['type'] or p['city'] == prop['city'])][:3]

    return render_template('properties/detail.html', property=prop, related_properties=related)
