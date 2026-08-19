from flask import Blueprint, render_template, abort
from app.models.property_model import PropertyRepository

agents_bp = Blueprint('agents', __name__)

@agents_bp.route('/corretores')
def list_agents():
    """Mostra a lista de todos os corretores com imóveis ativos."""
    agents = PropertyRepository.get_all_agents()
    return render_template('agents/list.html', agents=agents)

@agents_bp.route('/corretor/<nome>')
def agent_portfolio(nome):
    """Mostra o portfólio de imóveis de um corretor específico."""
    properties = PropertyRepository.get_properties_by_agent(nome)
    
    if not properties:
        # Se não encontrou imóveis para este corretor, pode ser que o nome esteja incorreto
        # ou ele não tenha imóveis ativos
        abort(404, description="Corretor não encontrado ou sem imóveis ativos.")
    
    # Pegamos os dados do corretor do primeiro imóvel dele
    agent_data = properties[0].get('agent', {})
    
    return render_template('agents/portfolio.html', agent=agent_data, properties=properties)
