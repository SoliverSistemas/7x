from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify, Response, make_response
import os
from datetime import datetime
from app.models.property_model import PropertyRepository
from app.models.db_models import ExclusiveCollection, Lancamento, ChatLead
from app.services.tecimobi_service import TecimobService
from app import db

main_bp = Blueprint('main', __name__)

# ── Fallback estático (usado apenas enquanto o DB não tiver lançamentos) ──
_LANCAMENTOS_STATIC = [
    {
        'slug': 'eden-residences',
        'name': 'Eden Residences',
        'tagline': 'Onde a arquitetura encontra o céu',
        'location': 'Itaim Bibi · São Paulo',
        'type': 'Alto Padrão',
        'status': 'Lançamento',
        'units': '48 unidades',
        'cover': 'img/lancamento_eden.jpg',
        'cover_url': None,
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
        'cover_url': None,
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
        'cover_url': None,
        'accent': '#c9ac77',
    },
]


def _get_lancamentos():
    """Retorna lançamentos do DB; usa fallback estático se vazio."""
    try:
        db_items = Lancamento.query.order_by(Lancamento.display_order, Lancamento.id).all()
        if db_items:
            return [l.to_dict() for l in db_items]
    except Exception:
        pass
    return _LANCAMENTOS_STATIC


@main_bp.route('/')
def index():
    # Coleção Exclusiva: vem da tabela exclusive_collection (max 3, com capa personalizada)
    exclusive_slots = ExclusiveCollection.query.order_by(ExclusiveCollection.display_order).limit(3).all()
    exclusive_properties = [slot.to_dict() for slot in exclusive_slots]

    high_end_properties = PropertyRepository.filter(category="Alto Padrão", per_page=10)['properties']
    featured_properties = PropertyRepository.get_featured(limit=10)

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
        lancamentos=_get_lancamentos()
    )

@main_bp.route('/sobre')
def about():
    return render_template('main/about.html')

@main_bp.route('/consorcio')
def consorcio():
    return render_template('main/consorcio.html')

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

@main_bp.route('/publique-seu-imovel')
def publique():
    return render_template('main/publique.html')

@main_bp.route('/lancamentos')
def lancamentos():
    return render_template('main/lancamentos.html', lancamentos=_get_lancamentos())

@main_bp.route('/lancamentos/<slug>')
def lancamento_detail(slug):
    whatsapp = os.getenv('WHATSAPP_NUMBER', '')
    # Tenta buscar no DB primeiro
    try:
        item = Lancamento.query.filter_by(slug=slug).first()
        if item:
            return render_template(
                'main/lancamento_detail.html',
                lancamento=item.to_dict(),
                whatsapp_number=whatsapp
            )
    except Exception:
        pass
    # Fallback estático
    item = next((l for l in _LANCAMENTOS_STATIC if l['slug'] == slug), None)
    if not item:
        abort(404)
    return render_template(
        'main/lancamento_detail.html',
        lancamento=item,
        whatsapp_number=whatsapp
    )


# ══ Chatbot Lead ══════════════════════════════════════════════════════════════
@main_bp.route('/chatbot/lead', methods=['POST'])
def chatbot_lead():
    """Salva lead capturado pelo chatbot."""
    data = request.get_json(silent=True) or {}
    name    = str(data.get('name',    '')).strip()[:120]
    phone   = str(data.get('phone',   '')).strip()[:30]
    message = str(data.get('message', '')).strip()[:1000]
    page    = str(data.get('page',    '')).strip()[:300]

    if not name and not phone:
        return jsonify({'ok': False, 'error': 'Dados insuficientes'}), 400

    lead = ChatLead(name=name, phone=phone, message=message, page=page)
    db.session.add(lead)
    db.session.commit()
    return jsonify({'ok': True, 'id': lead.id})


# ══ SEO: robots.txt ══════════════════════════════════════════════════════════
@main_bp.route('/robots.txt')
def robots_txt():
    """Serve o arquivo robots.txt permitindo indexação completa pelo Google."""
    content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /admin
Disallow: /chatbot/lead

Sitemap: https://7xpatrimonial.com.br/sitemap.xml
"""
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Cache-Control'] = 'public, max-age=86400'
    return response


# ══ SEO: sitemap.xml ═════════════════════════════════════════════════════════
@main_bp.route('/sitemap.xml')
def sitemap_xml():
    """Gera o sitemap.xml dinamicamente com todas as URLs públicas do site."""
    base_url = 'https://7xpatrimonial.com.br'
    today = datetime.utcnow().strftime('%Y-%m-%d')

    # Páginas estáticas
    static_pages = [
        ('/', '1.0', 'daily'),
        ('/imoveis/', '0.9', 'daily'),
        ('/sobre', '0.7', 'monthly'),
        ('/contato', '0.7', 'monthly'),
        ('/lancamentos', '0.8', 'weekly'),
        ('/publique-seu-imovel', '0.6', 'monthly'),
        ('/consorcio', '0.6', 'monthly'),
        ('/links', '0.4', 'monthly'),
    ]

    urls = []
    for path, priority, changefreq in static_pages:
        urls.append(f"""  <url>
    <loc>{base_url}{path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>""")

    # Imóveis individuais
    try:
        from app.models.property_model import PropertyRepository
        all_props = PropertyRepository.get_all()
        for prop in all_props:
            prop_id = getattr(prop, 'id', None) or (prop.get('id') if isinstance(prop, dict) else None)
            if prop_id:
                urls.append(f"""  <url>
    <loc>{base_url}/imoveis/{prop_id}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>""")
    except Exception:
        pass

    # Lançamentos individuais
    try:
        lancamentos = _get_lancamentos()
        for item in lancamentos:
            slug = item.get('slug') if isinstance(item, dict) else getattr(item, 'slug', None)
            if slug:
                urls.append(f"""  <url>
    <loc>{base_url}/lancamentos/{slug}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>""")
    except Exception:
        pass

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml_content += '\n'.join(urls)
    xml_content += '\n</urlset>'

    response = make_response(xml_content)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    response.headers['Cache-Control'] = 'public, max-age=3600'
    return response
