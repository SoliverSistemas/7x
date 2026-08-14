from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.property_model import PropertyRepository

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_properties = PropertyRepository.get_featured()
    all_properties = PropertyRepository.get_all()
    cities = PropertyRepository.get_cities()
    types = PropertyRepository.get_types()
    return render_template(
        'main/index.html',
        featured_properties=featured_properties,
        total_properties=len(all_properties),
        cities=cities,
        types=types
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
        
        # Flash feedback message
        flash(f'Obrigado, {name}! Sua mensagem foi enviada com sucesso. Nossa equipe entrará em contato em breve.', 'success')
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
