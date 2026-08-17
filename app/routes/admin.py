from functools import wraps
import uuid
import os
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, current_app, jsonify
)
from app.models.property_model import PropertyRepository
from app.models.db_models import ExclusiveCollection, Property
from app import db
from app.services.sync_service import SyncService
from app.services.storage_service import StorageService

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
    query   = request.args.get('q', '')
    purpose = request.args.get('purpose', '')
    sort_by = request.args.get('sort', 'recent')
    page    = request.args.get('page', 1, type=int)

    result = PropertyRepository.filter(
        search_query=query,
        purpose=purpose,
        sort_by=sort_by,
        page=page,
        per_page=30,
    )

    return render_template(
        'admin/properties.html',
        properties=result['properties'],
        pagination=result,
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


# ── Sync Properties (Cron/Admin) ────────────────────────────────────────────
@admin_bp.route('/sync-properties', methods=['POST'])
@login_required
def sync_properties():
    result = SyncService.sync_all_properties()
    if result.get("success"):
        flash(result.get("message"), 'success')
    else:
        flash(result.get("message"), 'error')
    return redirect(url_for('admin.dashboard'))


# ── Coleção Exclusiva ───────────────────────────────────────────────────
@admin_bp.route('/exclusivos', methods=['GET'])
@login_required
def exclusive_collection():
    slots = ExclusiveCollection.query.order_by(ExclusiveCollection.display_order).limit(3).all()
    # Todos os imoveis para o select de adicionar
    all_props = Property.query.filter_by(status='Disponível').order_by(Property.title).all()
    # Remover os que já estão na coleção
    used_ids = {s.property_id for s in slots}
    available_props = [p for p in all_props if p.id not in used_ids]
    return render_template(
        'admin/exclusive.html',
        slots=slots,
        available_props=available_props,
        max_slots=3
    )


@admin_bp.route('/exclusivos/adicionar', methods=['POST'])
@login_required
def exclusive_add():
    count = ExclusiveCollection.query.count()
    if count >= 3:
        flash('A coleção já tem 3 imóveis. Remova um antes de adicionar.', 'error')
        return redirect(url_for('admin.exclusive_collection'))

    property_id = request.form.get('property_id')
    if not property_id:
        flash('Selecione um imóvel.', 'error')
        return redirect(url_for('admin.exclusive_collection'))

    # Verifica se o imóvel existe
    prop = Property.query.get(property_id)
    if not prop:
        flash('Imóvel não encontrado.', 'error')
        return redirect(url_for('admin.exclusive_collection'))

    # Upload da capa se enviada
    cover_url = None
    cover_file = request.files.get('cover_image')
    if cover_file and cover_file.filename:
        try:
            ext = os.path.splitext(cover_file.filename)[1].lower() or '.jpg'
            filename = f"{property_id}_{uuid.uuid4().hex[:8]}{ext}"
            cover_url = StorageService.upload_cover(
                file_bytes=cover_file.read(),
                filename=filename,
                content_type=cover_file.content_type or 'image/jpeg'
            )
        except Exception as e:
            flash(f'Erro no upload da imagem: {e}', 'error')
            return redirect(url_for('admin.exclusive_collection'))

    order = count + 1
    slot = ExclusiveCollection(property_id=property_id, cover_url=cover_url, display_order=order)
    db.session.add(slot)
    db.session.commit()
    flash(f'Imóvel adicionado à Coleção Exclusiva!', 'success')
    return redirect(url_for('admin.exclusive_collection'))


@admin_bp.route('/exclusivos/<int:slot_id>/remover', methods=['POST'])
@login_required
def exclusive_remove(slot_id):
    slot = ExclusiveCollection.query.get_or_404(slot_id)
    # Deleta a imagem do Supabase Storage
    if slot.cover_url:
        StorageService.delete_cover(slot.cover_url)
    db.session.delete(slot)
    db.session.commit()
    # Reordena
    for i, s in enumerate(ExclusiveCollection.query.order_by(ExclusiveCollection.display_order).all(), start=1):
        s.display_order = i
    db.session.commit()
    flash('Imóvel removido da Coleção Exclusiva.', 'success')
    return redirect(url_for('admin.exclusive_collection'))


@admin_bp.route('/exclusivos/<int:slot_id>/capa', methods=['POST'])
@login_required
def exclusive_update_cover(slot_id):
    slot = ExclusiveCollection.query.get_or_404(slot_id)
    cover_file = request.files.get('cover_image')
    if not cover_file or not cover_file.filename:
        flash('Nenhuma imagem enviada.', 'error')
        return redirect(url_for('admin.exclusive_collection'))

    try:
        # Remove antiga
        if slot.cover_url:
            StorageService.delete_cover(slot.cover_url)
        ext = os.path.splitext(cover_file.filename)[1].lower() or '.jpg'
        filename = f"{slot.property_id}_{uuid.uuid4().hex[:8]}{ext}"
        slot.cover_url = StorageService.upload_cover(
            file_bytes=cover_file.read(),
            filename=filename,
            content_type=cover_file.content_type or 'image/jpeg'
        )
        db.session.commit()
        flash('Capa atualizada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro no upload: {e}', 'error')
    return redirect(url_for('admin.exclusive_collection'))
