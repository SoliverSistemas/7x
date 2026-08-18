from app import db
from app.models.db_models import Property
from app.models.property_model import PropertyRepository
from app.services.tecimobi_service import TecimobService
import math

class SyncService:
    @classmethod
    def sync_all_properties(cls):
        """
        Consome todos os imóveis da API Tecimob (paginando) e faz um upsert no banco de dados local.
        """
        if not TecimobService._is_active():
            return {"success": False, "message": "A integração Tecimob não está ativa no momento."}

        # Primeiro, buscamos a primeira página para saber o total de páginas
        first_page = TecimobService.fetch_properties(page=1, per_page=50)
        
        if not first_page:
            return {"success": False, "message": "Falha ao conectar com a API do Tecimob."}

        total_pages = first_page.get('last_page', 1)
        total_synced = 0
        total_errors = 0
        
        # Guardar IDs que vieram da API para inativar/remover os que não vieram
        synced_ids = []

        try:
            for page in range(1, total_pages + 1):
                # Para page=1, já temos os dados
                data = first_page if page == 1 else TecimobService.fetch_properties(page=page, per_page=50)
                
                if not data or not data.get('properties'):
                    continue

                for p_data in data['properties']:
                    # p_data is already normalized by TecimobService.normalize (listagem, sem imagens)
                    prop_id = str(p_data.get('id'))
                    if not prop_id:
                        continue

                    # Busca o detalhe do imóvel para obter as imagens reais
                    detail = TecimobService.fetch_property_by_id(prop_id)
                    if detail:
                        p_data['image'] = detail.get('image') or p_data.get('image')
                        p_data['gallery'] = detail.get('gallery') or p_data.get('gallery', [])
                        # Preenche campos extras que só vêm no detalhe
                        for field in ['description', 'condo_fee', 'iptu', 'is_financeable',
                                      'accepts_exchange', 'furnished', 'latitude', 'longitude',
                                      'condominium_name', 'amenities_property', 'amenities_condo', 'amenities']:
                            if detail.get(field) is not None:
                                p_data[field] = detail[field]

                    synced_ids.append(prop_id)

                    # Upsert (Update or Insert)
                    prop = Property.query.get(prop_id)
                    if not prop:
                        prop = Property(id=prop_id)
                        db.session.add(prop)

                    # Update fields
                    prop.reference = p_data.get('reference')
                    prop.title = p_data.get('title')
                    prop.slug = p_data.get('slug')
                    prop.type = p_data.get('type')
                    prop.subtype = p_data.get('subtype')
                    prop.purpose = p_data.get('purpose')
                    prop.price = p_data.get('price')
                    prop.condo_fee = p_data.get('condo_fee')
                    prop.iptu = p_data.get('iptu')
                    prop.area = p_data.get('area')
                    prop.area_total = p_data.get('area_total')
                    prop.bedrooms = p_data.get('bedrooms')
                    prop.suites = p_data.get('suites')
                    prop.bathrooms = p_data.get('bathrooms')
                    prop.garage = p_data.get('garage')
                    prop.garage_type = p_data.get('garage_type')
                    prop.solar_position = p_data.get('solar_position')
                    prop.floor_number = p_data.get('floor_number')
                    prop.total_floors = p_data.get('total_floors')
                    prop.condominium_name = p_data.get('condominium_name')
                    prop.is_financeable = p_data.get('is_financeable', False)
                    prop.accepts_exchange = p_data.get('accepts_exchange', False)
                    prop.furnished = p_data.get('furnished')
                    prop.city = p_data.get('city')
                    prop.state = p_data.get('state')
                    prop.neighborhood = p_data.get('neighborhood')
                    prop.address = p_data.get('address')
                    prop.zip_code = p_data.get('zip_code')
                    prop.latitude = p_data.get('latitude')
                    prop.longitude = p_data.get('longitude')
                    prop.featured = p_data.get('featured', False)
                    prop.status = p_data.get('status', 'Disponível')
                    prop.badge = p_data.get('badge')
                    prop.description = p_data.get('description')
                    prop.image = p_data.get('image')
                    # Calcula a categoria com base nos dados reais
                    prop.calculated_category = PropertyRepository.calculate_category(p_data)

                    # JSON fields
                    prop.amenities_property = p_data.get('amenities_property', [])
                    prop.amenities_condo = p_data.get('amenities_condo', [])
                    prop.amenities = p_data.get('amenities', [])
                    prop.gallery = p_data.get('gallery', [])
                    prop.agent = p_data.get('agent', {})
                    prop.establishments = p_data.get('establishments', [])

                    # Novos campos
                    prop.profile = p_data.get('profile')
                    prop.situation = p_data.get('situation')
                    prop.is_corner = p_data.get('is_corner', False)
                    prop.is_deeded = p_data.get('is_deeded', False)
                    prop.is_titled = p_data.get('is_titled', False)
                    prop.total_monthly_cost = p_data.get('total_monthly_cost')
                    prop.iptu_type = p_data.get('iptu_type')


                    total_synced += 1

                # Commit por página para salvar progresso gradualmente
                db.session.commit()

            # Remove properties that are no longer in Tecimob (exclusão física)
            if synced_ids:
                to_delete = Property.query.filter(Property.id.notin_(synced_ids)).all()
                for p in to_delete:
                    db.session.delete(p)
            
            db.session.commit()
            return {"success": True, "message": f"Sincronização concluída: {total_synced} imóveis atualizados/inseridos."}

        except Exception as e:
            db.session.rollback()
            import traceback
            traceback.print_exc()
            return {"success": False, "message": f"Erro interno durante a sincronização: {str(e)}"}
