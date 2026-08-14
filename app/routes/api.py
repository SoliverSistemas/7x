from flask import Blueprint, jsonify, request
from app.models.property_model import PropertyRepository

api_bp = Blueprint('api', __name__)

@api_bp.route('/properties', methods=['GET'])
def get_properties():
    query = request.args.get('q', '')
    prop_type = request.args.get('type', '')
    purpose = request.args.get('purpose', '')
    city = request.args.get('city', '')
    min_price = request.args.get('min_price', None)
    max_price = request.args.get('max_price', None)
    bedrooms = request.args.get('bedrooms', None)
    sort_by = request.args.get('sort', 'recent')

    properties = PropertyRepository.filter(
        search_query=query,
        prop_type=prop_type,
        purpose=purpose,
        min_price=min_price,
        max_price=max_price,
        bedrooms=bedrooms,
        city=city,
        sort_by=sort_by
    )

    return jsonify({
        'status': 'success',
        'count': len(properties),
        'properties': properties
    })

@api_bp.route('/schedule-visit', methods=['POST'])
def schedule_visit():
    data = request.get_json() or request.form
    property_id = data.get('property_id')
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    visit_date = data.get('visit_date')
    visit_time = data.get('visit_time')

    if not name or not phone or not visit_date:
        return jsonify({
            'status': 'error',
            'message': 'Por favor, preencha todos os campos obrigatórios (nome, telefone, data).'
        }), 400

    return jsonify({
        'status': 'success',
        'message': f'Visita agendada com sucesso para {visit_date} às {visit_time}! Nosso corretor entrará em contato via WhatsApp.'
    })

@api_bp.route('/calculate-financing', methods=['POST'])
def calculate_financing():
    data = request.get_json() or {}
    try:
        property_value = float(data.get('property_value', 0))
        down_payment = float(data.get('down_payment', 0))
        years = int(data.get('years', 30))
        annual_rate = float(data.get('annual_rate', 10.5)) / 100.0 # Default 10.5% a.a.

        financed_amount = property_value - down_payment
        if financed_amount <= 0:
            return jsonify({'status': 'error', 'message': 'O valor financiado deve ser maior que zero.'}), 400

        total_months = years * 12
        monthly_rate = annual_rate / 12.0

        # Price amortization calculation formula
        if monthly_rate > 0:
            monthly_installment = financed_amount * (monthly_rate * (1 + monthly_rate)**total_months) / (((1 + monthly_rate)**total_months) - 1)
        else:
            monthly_installment = financed_amount / total_months

        total_paid = (monthly_installment * total_months) + down_payment
        total_interest = total_paid - property_value

        return jsonify({
            'status': 'success',
            'property_value': property_value,
            'down_payment': down_payment,
            'financed_amount': financed_amount,
            'years': years,
            'monthly_installment': round(monthly_installment, 2),
            'total_paid': round(total_paid, 2),
            'total_interest': round(total_interest, 2)
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Erro no cálculo: {str(e)}'}), 400
