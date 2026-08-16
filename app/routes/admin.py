from functools import wraps
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, current_app
)
from app.models.property_model import PropertyRepository

admin_bp = Blueprint('admin', __name__)


# ── Auth guard decorator ────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login', next=request.path))
        return f(*args, **kwargs)
    return decorated


# ── Login ───────────────────────────────────────────────────────────────────
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin.dashboard'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        valid_user = current_app.config.get('ADMIN_USERNAME')
        valid_pass = current_app.config.get('ADMIN_PASSWORD')

        if username == valid_user and password == valid_pass:
            session.permanent = True
            session['admin_logged_in'] = True
            session['admin_user'] = username
            next_url = request.args.get('next') or url_for('admin.dashboard')
            return redirect(next_url)
        else:
            error = 'Usuário ou senha incorretos.'

    return render_template('admin/login.html', error=error)


# ── Logout ──────────────────────────────────────────────────────────────────
@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


# ── Dashboard ───────────────────────────────────────────────────────────────
@admin_bp.route('/')
@login_required
def dashboard():
    all_props  = PropertyRepository.get_all()
    total      = len(all_props)
    for_sale   = sum(1 for p in all_props if p.get('purpose') == 'Venda')
    for_rent   = sum(1 for p in all_props if p.get('purpose') == 'Aluguel')
    featured   = sum(1 for p in all_props if p.get('featured'))
    avg_price  = (sum(p.get('price', 0) for p in all_props) / total) if total else 0

    # Group by type
    types = {}
    for p in all_props:
        t = p.get('type', 'Outros')
        types[t] = types.get(t, 0) + 1

    # Group by city
    cities = {}
    for p in all_props:
        c = p.get('city', '—')
        cities[c] = cities.get(c, 0) + 1

    recent = sorted(all_props, key=lambda x: x.get('id', 0), reverse=True)[:5]

    return render_template(
        'admin/dashboard.html',
        total=total,
        for_sale=for_sale,
        for_rent=for_rent,
        featured=featured,
        avg_price=avg_price,
        types=types,
        cities=cities,
        recent=recent,
    )


# ── Properties list ─────────────────────────────────────────────────────────
@admin_bp.route('/imoveis')
@login_required
def properties():
    query    = request.args.get('q', '')
    purpose  = request.args.get('purpose', '')
    sort_by  = request.args.get('sort', 'recent')

    props = PropertyRepository.filter(
        search_query=query,
        purpose=purpose,
        sort_by=sort_by,
    )

    return render_template(
        'admin/properties.html',
        properties=props,
        current_filters={'query': query, 'purpose': purpose, 'sort': sort_by},
    )


# ── Property detail (view-only) ─────────────────────────────────────────────
@admin_bp.route('/imoveis/<property_id>')
@login_required
def property_detail(property_id):
    prop = PropertyRepository.get_by_id(property_id)
    if not prop:
        flash('Imóvel não encontrado.', 'error')
        return redirect(url_for('admin.properties'))
    return render_template('admin/property_detail.html', property=prop)


# ── Toggle Exclusive ────────────────────────────────────────────────────────
@admin_bp.route('/imoveis/<property_id>/toggle-exclusive', methods=['POST'])
@login_required
def toggle_exclusive(property_id):
    status = PropertyRepository.toggle_exclusive(property_id)
    if status is not None:
        flash(f'Status de exclusividade atualizado para o imóvel #{property_id}.', 'success')
    else:
        flash('Imóvel não encontrado.', 'error')
    return redirect(request.referrer or url_for('admin.properties'))
