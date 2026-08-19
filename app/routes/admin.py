from functools import wraps
import uuid
import os
import re
from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session, flash, current_app, jsonify
)
from app.models.property_model import PropertyRepository
from app.models.db_models import ExclusiveCollection, Property, Lancamento, PropertyCategory, AgentProfile
from app import db
from app.services.sync_service import SyncService
from app.services.storage_service import StorageService

admin_bp = Blueprint('admin', __name__)

MAX_LANCAMENTOS = 10


# ── Auth guard decorator ────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin.login', next=request.path))
        return f(*args, **kwargs)
    return decorated


def _slugify(text: str) -> str:
    """Gera slug simples a partir de um texto."""
    import unicodedata
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[\s_-]+', '-', text)


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
    total_lancamentos = Lancamento.query.count()

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
        total_lancamentos=total_lancamentos,
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
    all_props = Property.query.filter_by(status='Disponível').order_by(Property.title).all()
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

    prop = Property.query.get(property_id)
    if not prop:
        flash('Imóvel não encontrado.', 'error')
        return redirect(url_for('admin.exclusive_collection'))

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
    flash('Imóvel adicionado à Coleção Exclusiva!', 'success')
    return redirect(url_for('admin.exclusive_collection'))


@admin_bp.route('/exclusivos/<int:slot_id>/remover', methods=['POST'])
@login_required
def exclusive_remove(slot_id):
    slot = ExclusiveCollection.query.get_or_404(slot_id)
    if slot.cover_url:
        StorageService.delete_cover(slot.cover_url)
    db.session.delete(slot)
    db.session.commit()
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


# ══════════════════════════════════════════════════════════════════════════════
# ── Lançamentos ──────────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/lancamentos')
@login_required
def lancamentos_list():
    items = Lancamento.query.order_by(Lancamento.display_order, Lancamento.id).all()
    return render_template(
        'admin/lancamentos.html',
        lancamentos=items,
        max_lancamentos=MAX_LANCAMENTOS,
        count=len(items),
    )


@admin_bp.route('/lancamentos/novo', methods=['POST'])
@login_required
def lancamento_create():
    if Lancamento.query.count() >= MAX_LANCAMENTOS:
        flash(f'Limite de {MAX_LANCAMENTOS} lançamentos atingido. Exclua um antes de criar.', 'error')
        return redirect(url_for('admin.lancamentos_list'))

    name = request.form.get('name', '').strip()
    if not name:
        flash('O nome do lançamento é obrigatório.', 'error')
        return redirect(url_for('admin.lancamentos_list'))

    # Gera slug único
    base_slug = _slugify(name)
    slug = base_slug
    counter = 1
    while Lancamento.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    # Upload capa
    cover_url = None
    cover_file = request.files.get('cover_image')
    if cover_file and cover_file.filename:
        try:
            ext = os.path.splitext(cover_file.filename)[1].lower() or '.jpg'
            filename = f"lanc_{uuid.uuid4().hex}{ext}"
            cover_url = StorageService.upload_lancamento_cover(
                file_bytes=cover_file.read(),
                filename=filename,
                content_type=cover_file.content_type or 'image/jpeg'
            )
        except Exception as e:
            flash(f'Erro no upload da capa: {e}', 'error')
            return redirect(url_for('admin.lancamentos_list'))

    order = (db.session.query(db.func.max(Lancamento.display_order)).scalar() or 0) + 1
    item = Lancamento(
        name=name,
        slug=slug,
        tagline=request.form.get('tagline', '').strip(),
        location=request.form.get('location', '').strip(),
        type=request.form.get('type', '').strip(),
        status=request.form.get('status', 'Lançamento').strip(),
        units=request.form.get('units', '').strip(),
        cover_url=cover_url,
        display_order=order,
    )
    db.session.add(item)
    db.session.commit()
    flash(f'Lançamento "{name}" criado com sucesso!', 'success')
    return redirect(url_for('admin.lancamento_edit', lancamento_id=item.id))


@admin_bp.route('/lancamentos/<int:lancamento_id>', methods=['GET'])
@login_required
def lancamento_edit(lancamento_id):
    item = Lancamento.query.get_or_404(lancamento_id)
    return render_template('admin/lancamento_edit.html', lancamento=item)


@admin_bp.route('/lancamentos/<int:lancamento_id>/salvar', methods=['POST'])
@login_required
def lancamento_save(lancamento_id):
    item = Lancamento.query.get_or_404(lancamento_id)

    name = request.form.get('name', '').strip()
    if not name:
        flash('O nome é obrigatório.', 'error')
        return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))

    # Atualiza slug se o nome mudou
    if name != item.name:
        base_slug = _slugify(name)
        slug = base_slug
        counter = 1
        while True:
            existing = Lancamento.query.filter_by(slug=slug).first()
            if not existing or existing.id == item.id:
                break
            slug = f"{base_slug}-{counter}"
            counter += 1
        item.slug = slug

    item.name        = name
    item.tagline     = request.form.get('tagline', '').strip()
    item.location    = request.form.get('location', '').strip()
    item.type        = request.form.get('type', '').strip()
    item.status      = request.form.get('status', '').strip()
    item.units       = request.form.get('units', '').strip()
    item.description = request.form.get('description', '').strip()

    # Textos e títulos da galeria (text_0/title_0, text_1/title_1, ...)
    imgs = item.gallery
    for i in range(len(imgs)):
        imgs[i]['text']  = request.form.get(f'text_{i}',  '').strip()
        imgs[i]['title'] = request.form.get(f'title_{i}', '').strip()
    item.gallery = imgs

    # Nova capa (opcional)
    cover_file = request.files.get('cover_image')
    if cover_file and cover_file.filename:
        try:
            if item.cover_url:
                StorageService.delete_lancamento_file(item.cover_url)
            ext = os.path.splitext(cover_file.filename)[1].lower() or '.jpg'
            filename = f"lanc_{uuid.uuid4().hex}{ext}"
            item.cover_url = StorageService.upload_lancamento_cover(
                file_bytes=cover_file.read(),
                filename=filename,
                content_type=cover_file.content_type or 'image/jpeg'
            )
        except Exception as e:
            flash(f'Erro no upload da capa: {e}', 'error')
            return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))

    db.session.commit()
    flash('Lançamento salvo com sucesso!', 'success')
    return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))


@admin_bp.route('/lancamentos/<int:lancamento_id>/galeria/adicionar', methods=['POST'])
@login_required
def lancamento_add_image(lancamento_id):
    item = Lancamento.query.get_or_404(lancamento_id)
    if len(item.gallery) >= 6:
        flash('Limite de 6 imagens atingido.', 'error')
        return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))

    img_file = request.files.get('image')
    if not img_file or not img_file.filename:
        flash('Nenhuma imagem enviada.', 'error')
        return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))

    try:
        ext = os.path.splitext(img_file.filename)[1].lower() or '.jpg'
        filename = f"lanc_{lancamento_id}_{uuid.uuid4().hex[:8]}{ext}"
        url = StorageService.upload_lancamento_image(
            file_bytes=img_file.read(),
            filename=filename,
            content_type=img_file.content_type or 'image/jpeg'
        )
        item.add_gallery_image(url, text='')
        db.session.commit()
        flash('Imagem adicionada à galeria!', 'success')
    except Exception as e:
        flash(f'Erro no upload: {e}', 'error')

    return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))


@admin_bp.route('/lancamentos/<int:lancamento_id>/galeria/<int:img_index>/remover', methods=['POST'])
@login_required
def lancamento_remove_image(lancamento_id, img_index):
    item = Lancamento.query.get_or_404(lancamento_id)
    removed = item.remove_gallery_image(img_index)
    if removed:
        db.session.commit()
        try:
            file_url = removed.get('url', '') if isinstance(removed, dict) else removed
            StorageService.delete_lancamento_file(file_url)
        except Exception as e:
            current_app.logger.warning(f"Erro ao deletar imagem da galeria: {e}")
        flash('Imagem removida.', 'success')
    else:
        flash('Imagem não encontrada.', 'error')
    return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))


@admin_bp.route('/lancamentos/<int:lancamento_id>/galeria/textos', methods=['POST'])
@login_required
def lancamento_update_gallery_texts(lancamento_id):
    """Salva os textos de cada imagem da galeria."""
    item = Lancamento.query.get_or_404(lancamento_id)
    imgs = item.gallery  # lista de dicts {url, text}
    for i, img in enumerate(imgs):
        text = request.form.get(f'text_{i}', '').strip()
        imgs[i]['text'] = text
    item.gallery = imgs
    db.session.commit()
    flash('Textos da galeria salvos!', 'success')
    return redirect(url_for('admin.lancamento_edit', lancamento_id=lancamento_id))


@admin_bp.route('/lancamentos/<int:lancamento_id>/excluir', methods=['POST'])
@login_required
def lancamento_delete(lancamento_id):
    item = Lancamento.query.get_or_404(lancamento_id)
    name = item.name

    # Remove capa do storage
    if item.cover_url:
        try:
            StorageService.delete_lancamento_file(item.cover_url)
        except Exception as e:
            current_app.logger.warning(f"Erro ao deletar capa: {e}")

    # Remove todas as imagens da galeria
    for img in item.gallery:
        try:
            file_url = img.get('url', '') if isinstance(img, dict) else img
            StorageService.delete_lancamento_file(file_url)
        except Exception as e:
            current_app.logger.warning(f"Erro ao deletar galeria: {e}")

    db.session.delete(item)
    db.session.commit()
    flash(f'Lançamento "{name}" excluído com sucesso.', 'success')
    return redirect(url_for('admin.lancamentos_list'))


# ══════════════════════════════════════════════════════════════════════════════
# CATEGORIAS DE IMÓVEIS
# ══════════════════════════════════════════════════════════════════════════════

@admin_bp.route('/categorias')
@login_required
def categorias_list():
    cats = PropertyCategory.query.order_by(PropertyCategory.priority.asc()).all()
    return render_template('admin/categorias.html', categories=cats)


@admin_bp.route('/categorias/salvar', methods=['POST'])
@login_required
def categoria_save():
    """Cria ou edita uma categoria (id='' → nova)."""
    cat_id   = request.form.get('id', '').strip()
    name     = request.form.get('name', '').strip()
    color    = request.form.get('color', '#c9ac77').strip()
    priority = int(request.form.get('priority', 10) or 10)

    raw_min = request.form.get('min_price', '').strip().replace('.', '').replace(',', '.')
    raw_max = request.form.get('max_price', '').strip().replace('.', '').replace(',', '.')
    min_price = float(raw_min) if raw_min else None
    max_price = float(raw_max) if raw_max else None

    is_exclusive_flag = 'is_exclusive_flag' in request.form
    is_featured_flag  = 'is_featured_flag'  in request.form

    if not name:
        flash('Nome da categoria é obrigatório.', 'error')
        return redirect(url_for('admin.categorias_list'))

    if cat_id:
        cat = PropertyCategory.query.get(int(cat_id))
        if not cat:
            flash('Categoria não encontrada.', 'error')
            return redirect(url_for('admin.categorias_list'))
    else:
        cat = PropertyCategory()
        db.session.add(cat)

    cat.name              = name
    cat.color             = color
    cat.priority          = priority
    cat.min_price         = min_price
    cat.max_price         = max_price
    cat.is_exclusive_flag = is_exclusive_flag
    cat.is_featured_flag  = is_featured_flag
    db.session.commit()

    flash(f'Categoria "{name}" salva.', 'success')
    return redirect(url_for('admin.categorias_list'))


@admin_bp.route('/categorias/<int:cat_id>/excluir', methods=['POST'])
@login_required
def categoria_delete(cat_id):
    cat = PropertyCategory.query.get_or_404(cat_id)
    name = cat.name
    db.session.delete(cat)
    db.session.commit()
    flash(f'Categoria "{name}" excluída.', 'success')
    return redirect(url_for('admin.categorias_list'))


@admin_bp.route('/categorias/recalcular', methods=['POST'])
@login_required
def categorias_recalcular():
    """Re-aplica calculate_category() a todos os imóveis e salva no banco."""
    props = Property.query.all()
    count = 0
    for p in props:
        nova = PropertyRepository.calculate_category(p.to_dict())
        if p.calculated_category != nova:
            p.calculated_category = nova
            count += 1
    db.session.commit()
    flash(f'Recálculo concluído — {count} imóvel(is) atualizado(s).', 'success')
    return redirect(url_for('admin.categorias_list'))


@admin_bp.route('/categorias/criar-padroes', methods=['POST'])
@login_required
def categorias_criar_padroes():
    """Popula a tabela com as categorias padrão do sistema."""
    if PropertyCategory.query.count() > 0:
        flash('Já existem categorias cadastradas. Exclua-as antes de criar os padrões.', 'error')
        return redirect(url_for('admin.categorias_list'))

    padroes = [
        PropertyCategory(name='Exclusivo',    color='#c9ac77', priority=1,  is_exclusive_flag=True),
        PropertyCategory(name='Alto Padrão',  color='#3b82f6', priority=2,  min_price=2_000_000),
        PropertyCategory(name='Médio Padrão', color='#8b5cf6', priority=3,  min_price=500_000, max_price=1_999_999),
        PropertyCategory(name='Padrão',       color='#10b981', priority=4,  max_price=499_999),
        PropertyCategory(name='Destaque',     color='#f59e0b', priority=5,  is_featured_flag=True),
    ]
    for p in padroes:
        db.session.add(p)
    db.session.commit()
    flash('Categorias padrão criadas com sucesso!', 'success')
    return redirect(url_for('admin.categorias_list'))


# ── Corretores ──────────────────────────────────────────────────────────────
@admin_bp.route('/corretores', methods=['GET'])
@login_required
def list_agents():
    agents = PropertyRepository.get_all_agents()
    return render_template('admin/agents.html', agents=agents)

@admin_bp.route('/corretores/<agent_name>', methods=['POST'])
@login_required
def update_agent(agent_name):
    from werkzeug.utils import secure_filename

    prof = AgentProfile.query.filter_by(name=agent_name).first()
    if not prof:
        prof = AgentProfile(name=agent_name)
        db.session.add(prof)
        
    avatar_file = request.files.get('avatar')
    if avatar_file and avatar_file.filename:
        # Upload new avatar
        if prof.avatar_url:
            StorageService.delete_agent_avatar(prof.avatar_url)
            
        ext = os.path.splitext(avatar_file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        file_bytes = avatar_file.read()
        
        try:
            url = StorageService.upload_agent_avatar(file_bytes, filename, avatar_file.content_type)
            prof.avatar_url = url
        except Exception as e:
            flash(f'Erro ao fazer upload da imagem: {e}', 'error')
            return redirect(url_for('admin.list_agents'))

    prof.instagram = request.form.get('instagram')
    prof.description = request.form.get('description')
    
    db.session.commit()
    flash(f'Perfil de {agent_name} atualizado com sucesso!', 'success')
    return redirect(url_for('admin.list_agents'))
