from flask import Blueprint, render_template, abort
from app.models.db_models import AgentProfile

agents_bp = Blueprint('agents', __name__)


@agents_bp.route('/corretores')
def list_agents():
    """Lista de corretores cadastrados manualmente pelo admin."""
    agents = (
        AgentProfile.query
        .filter_by(is_active=True)
        .order_by(AgentProfile.display_order.asc(), AgentProfile.name.asc())
        .all()
    )
    return render_template('agents/list.html', agents=agents)


@agents_bp.route('/corretor/<int:agent_id>')
def agent_portfolio(agent_id):
    """Página de perfil de um corretor específico."""
    agent = AgentProfile.query.filter_by(id=agent_id, is_active=True).first_or_404()
    return render_template('agents/portfolio.html', agent=agent)
