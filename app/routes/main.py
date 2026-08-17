from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from app.models.property_model import PropertyRepository
from app.models.db_models import ExclusiveCollection
from app.services.tecimobi_service import TecimobService

main_bp = Blueprint('main', __name__)

# ── Dados dos lançamentos (futuramente viram modelo/DB) ──────────────────
LANCAMENTOS = [
    {
        'slug': 'eden-residences',
        'name': 'Eden Residences',
        'tagline': 'Onde a arquitetura encontra o céu',
        'location': 'Itaim Bibi · São Paulo',
        'type': 'Alto Padrão',
        'status': 'Lançamento',
        'units': '48 unidades',
        'cover': 'img/lancamento_eden.jpg',
        'accent': '#c9ac77',
    },
    {
        'slug': 'sky-penthouse',
        'name': 'Sky Penthouse',
        'tagline': 'O topo redefinido',
        'location': 'Jardins · São Paulo',
        'type': 'Cobertura',
        'status': 'Pré-lançamento',
        'units': '12 unidades exclusivas',
        'cover': 'img/lancamento_sky.jpg',
        'accent': '#c9ac77',
    },
    {
        'slug': 'villa-serena',
        'name': 'Villa Serena',
        'tagline': 'Privacidade absoluta. Sofisticação total.',
        'location': 'Morumbi · São Paulo',
        'type': 'Casa de Alto Padrão',
        'status': 'Breve',
        'units': '6 residências',
        'cover': 'img/lancamento_villa.jpg',
        'accent': '#c9ac77',
    },
]

@main_bp.route('/')
def index():
    # Coleção Exclusiva: vem da tabela exclusive_collection (max 3, com capa personalizada)
    exclusive_slots = ExclusiveCollection.query.order_by(ExclusiveCollection.display_order).limit(3).all()
    exclusive_properties = [slot.to_dict() for slot in exclusive_slots]
    
    high_end_properties = PropertyRepository.filter(category="Alto Padrão")['properties']
    featured_properties = PropertyRepository.get_featured()
        
    all_properties = PropertyRepository.get_all()
    cities = PropertyRepository.get_cities()
    types = PropertyRepository.get_types()
    return render_template(
        'main/index.html',
        featured_properties=featured_properties,
        exclusive_properties=exclusive_properties,
        high_end_properties=high_end_properties,
        total_properties=len(all_properties),
        cities=cities,
        types=types,
        lancamentos=LANCAMENTOS
    )

@main_bp.route('/sobre')
def about():
    return render_template('main/about.html')

@main_bp.route('/contato', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        if not name or not phone:
            flash('Nome e telefone são obrigatórios.', 'error')
            return redirect(url_for('main.contact'))

        # Tenta enviar o Lead para o Tecimob CRM
        msg = f"Contato via site: {message}" if message else "Contato via página principal do site"
        lead_sent = TecimobService.send_lead(
            name=name,
            phone=phone,
            email=email,
            message=msg
        )

        if lead_sent:
            flash(f'Obrigado, {name}! Sua mensagem foi enviada com sucesso. Nossa equipe entrará em contato em breve.', 'success')
        else:
            flash(f'Recebemos sua mensagem, {name}. Nossa integração com o sistema está offline no momento, mas um corretor retornará em breve.', 'success')
            
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html')

@main_bp.route('/links')
def links():
    import os
    from flask import current_app
    links_data = {
        'site': os.environ.get('LINK_SITE_URL') or current_app.config.get('LINK_SITE_URL', '/'),
        'instagram': os.environ.get('LINK_INSTAGRAM_URL') or current_app.config.get('LINK_INSTAGRAM_URL', 'https://instagram.com/7xpatrimonial'),
        'tiktok': os.environ.get('LINK_TIKTOK_URL') or current_app.config.get('LINK_TIKTOK_URL', 'https://tiktok.com/@7xpatrimonial'),
        'whatsapp': os.environ.get('LINK_WHATSAPP_URL') or current_app.config.get('LINK_WHATSAPP_URL', 'https://wa.me/5511999997777')
    }
    return render_template('main/links.html', links=links_data)

@main_bp.route('/lancamentos')
def lancamentos():
    return render_template('main/lancamentos.html', lancamentos=LANCAMENTOS)

@main_bp.route('/lancamentos/<slug>')
def lancamento_detail(slug):
    item = next((l for l in LANCAMENTOS if l['slug'] == slug), None)
    if not item:
        abort(404)
    return render_template('main/lancamento_detail.html', lancamento=item)
