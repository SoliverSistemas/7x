# Documentação Oficial da Stack Tecnológica & Integração Tecimob API

**Projeto:** 7X Imóveis — Plataforma Imobiliária de Alto Padrão  
**Versão:** 1.2.0  
**Data:** 14/08/2026  
**Fonte da API:** [https://swagger.tecimob.com.br](https://swagger.tecimob.com.br)  

---

## 🛠️ 1. Stack Tecnológica Completa

| Camada | Tecnologia | Versão | Função |
| :--- | :--- | :--- | :--- |
| **Backend** | Python | 3.12+ | Linguagem base |
| **Framework Web** | Flask | 3.1.3 | Servidor e rotas |
| **Padrão de Projeto** | Application Factory + Blueprints | — | Modularidade e separação de concerns |
| **Templating** | Jinja2 | (Flask built-in) | Renderização HTML com filtros customizados |
| **Frontend** | HTML5 Semântico | — | Estrutura de páginas |
| **Estilos** | Vanilla CSS3 + Custom Properties | — | Design system, glassmorphism, grid responsivo |
| **Tipografia** | Google Fonts (Plus Jakarta Sans + Inter) | — | Hierarquia visual premium |
| **Animações** | GSAP 3 + ScrollTrigger | 3.12.5 | Animações web avançadas e fluidas |
| **JavaScript** | Vanilla ES6+ | — | Lógica de UI, AJAX, localStorage |
| **CRM/ERP** | Tecimob API Pública | v1 | Integração de anúncios em tempo real |
| **Ambiente** | python-dotenv | 1.2.x | Variáveis de ambiente |

### Estrutura de Arquivos (Flask Factory Pattern)

```text
7x_site/
├── config.py                        # Configurações por ambiente (Dev / Test / Prod)
├── run.py                           # Entrypoint → create_app()
├── requirements.txt                 # Flask, python-dotenv
├── DOCUMENTACAO_STACK_TECIMOB.md    # Este arquivo
└── app/
    ├── __init__.py                  # ★ Application Factory create_app()
    ├── models/
    │   └── property_model.py        # PropertyRepository (cache local + Tecimob)
    ├── services/
    │   └── tecimobi_service.py      # ★ Integração real com API Tecimob
    ├── routes/
    │   ├── main.py                  # Blueprint: Home, Sobre, Contato
    │   ├── properties.py            # Blueprint: Catálogo e detalhes de imóveis
    │   └── api.py                   # Blueprint: REST API interna do site
    ├── static/
    │   ├── css/main.css             # Design tokens, tipografia, grid, header glassmorphism
    │   ├── css/components.css       # Cards, badges, formulários, modais, calculadora
    │   ├── js/main.js               # Toast, modais, favoritos (localStorage), nav mobile
    │   ├── js/properties.js         # AJAX filtering, simulador financiamento, agendamento
    │   ├── js/animations.js         # ★ GSAP: hero timeline, ScrollTrigger, hover FX
    │   └── img/                     # Imagens geradas para preview
    └── templates/
        ├── base.html                # Layout master com GSAP CDN
        ├── 404.html / 500.html
        ├── main/ (index, about, contact)
        └── properties/ (index, detail)
```

---

## 🎬 2. Animações Avançadas com GSAP 3

### Carregamento (CDN)
```html
<!-- Incluído em base.html -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
```

### Efeitos implementados em [`animations.js`](file:///c:/Users/Caveira%20Soliver/Documents/7x/7x_site/app/static/js/animations.js)

| Efeito | API GSAP | Trigger |
| :--- | :--- | :--- |
| Entrada do header/logo/hero | `gsap.timeline()` | DOMContentLoaded |
| Cards de imóveis em cascata | `gsap.from()` + `stagger` | ScrollTrigger `top 85%` |
| Títulos de seção fade+slide | `gsap.from()` | ScrollTrigger `top 90%` |
| Diferencias e cards de texto | `gsap.from()` + `back.out` | ScrollTrigger |
| Hover em cards | `gsap.to()` | mouseenter / mouseleave |
| Hover em botões | `gsap.to()` + `scale` | mouseenter / mouseleave |

---

## 🔌 3. Integração com a API Pública do Tecimob

### Informações Gerais

- **Documentação oficial (Swagger):** [https://swagger.tecimob.com.br](https://swagger.tecimob.com.br)
- **URL Base (Produção):** `https://api.tecimob.com.br/v1`
- **Autenticação:** `Authorization: Bearer <token>`

> [!IMPORTANT]
> A API pública do Tecimob é um serviço adicional pago dentro da plataforma. Para habilitar, acesse **Ajustes Gerais → API → Contratar API Pública** no painel Tecimob e crie uma chave com os escopos necessários.

### Configuração do Ambiente (`.env`)

```env
# Habilita a integração ao vivo com a API do Tecimob
USE_TECIMOB_API=true

# Token Bearer gerado no painel do Tecimob
TECIMOB_API_TOKEN=seu_token_bearer_aqui
```

---

## 📡 4. Endpoints Consumidos pela Integração

### 4.1 `GET /api/properties` — Listagem de Imóveis

Retorna lista paginada dos anúncios ativos cadastrados no Tecimob.

**Parâmetros de filtro suportados:**

| Parâmetro | Tipo | Exemplo | Descrição |
| :--- | :--- | :--- | :--- |
| `page` | integer | `1` | Número da página (paginação) |
| `per_page` | integer | `20` | Itens por página |
| `filter[status]` | enum | `disponivel` | `disponivel` \| `vendido` \| `alugado` \| `excluido` |
| `filter[transaction]` | enum | `venda` | `venda` \| `aluguel` \| `temporada` |
| `filter[neighborhood.city.name]` | string | `São Paulo` | Filtro por cidade |
| `filter[neighborhood.name]` | string | `Itaim Bibi` | Filtro por bairro |
| `filter[price]` | string | `>=500000` | Preço com operador (`>=`, `<=`) |
| `filter[by_room][bedroom][value]` | integer | `3` | Quantidade de quartos |
| `filter[by_room][bedroom][filter]` | string | `greater_equals` | Operador do filtro de quartos |
| `filter[by_area][built_area][greater_equals]` | number | `80` | Área construída mínima (m²) |
| `filter[by_area][built_area][lower_equals]` | number | `200` | Área construída máxima (m²) |
| `filter[subtype.type.title]` | string | `Residencial` | Tipo de imóvel |
| `filter[subtype.title]` | string | `Apartamento` | Subtipo de imóvel |
| `filter[user_id]` | uuid | `...` | Filtrar por corretor responsável |
| `filter[reference]` | string | `AP0042` | Código de referência interno |

**Resposta (data[]):**
```json
{
  "data": [{
    "id": "uuid",
    "price": "R$ 850.000,00",
    "transaction": "VENDA",
    "reference": "AP0042",
    "status": "Disponível",
    "url": "https://...",
    "street_address": "Rua das Flores",
    "street_number": "123",
    "zip_code": "01310-100",
    "neighborhood": { "name": "Jardins", "city": { "name": "São Paulo", "state": { "acronym": "SP" }}},
    "type": "Residencial",
    "subtype": "Apartamento",
    "user": { "name": "Ricardo", "email": "...", "cellphone": "11999998888", "creci": "..." },
    "characteristics": [{ "title": "Quartos", "quantity": 3 }, { "title": "Vagas", "quantity": 2 }],
    "condo_characteristics": [{ "title": "Piscina", "quantity": null }],
    "maps_latitude": -23.56,
    "maps_longitude": -46.65
  }],
  "meta": { "current_page": 1, "last_page": 5, "per_page": 20, "total": 92 },
  "links": { "next": "https://...", "prev": null }
}
```

---

### 4.2 `GET /api/properties/{uuid}` — Detalhe de Imóvel

Retorna a ficha completa do imóvel — inclui todos os campos da listagem **mais** campos exclusivos:

| Campo Adicional | Tipo | Descrição |
| :--- | :--- | :--- |
| `description` | string (HTML) | Descrição completa do imóvel |
| `areas[]` | array | Áreas: `built_area`, `land_area`, `total_area` com valor e medida (`m²`) |
| `rooms[]` | array | Cômodos com quantidades detalhadas |
| `informations[]` | array | Dados gerais incluindo galeria de fotos |
| `condominium_price` | string | Valor do condomínio (`"R$ 1.200,00"`) |
| `territorial_tax_price` | string | IPTU (`"R$ 850,00"`) |
| `is_financeable` | boolean | Aceita financiamento |
| `has_furniture` | boolean | Mobiliado |
| `condominium` | object | Nome e dados do condomínio |
| `person` | object | Dados do proprietário |
| `situation` | string | Situação (em construção, pronto, etc.) |
| `solar_position` | string | Posição solar |
| `maps_latitude` / `longitude` | number | Coordenadas para mapa |

---

### 4.3 `POST /api/leads/store-person` — Envio de Lead

Registra um visitante/interessado como lead no CRM Tecimob automaticamente quando o usuário agenda uma visita ou envia interesse no site 7X.

```json
{
  "name": "Maria Oliveira",
  "email": "maria@email.com",
  "phones": [{ "ddi": 55, "number": "11998887766", "description": "WhatsApp" }]
}
```

### 4.4 `POST /api/leads/relate-person` — Vinculação Lead ↔ Imóvel

Associa o lead criado ao imóvel de interesse diretamente no funil do Tecimob.

```json
{
  "person_id": "uuid-do-lead",
  "property_id": "uuid-do-imovel",
  "note": "Interesse via site 7X Imóveis"
}
```

---

## 🔄 5. Pipeline de Normalização dos Dados

O [`TecimobService.normalize()`](file:///c:/Users/Caveira%20Soliver/Documents/7x/7x_site/app/services/tecimobi_service.py) transforma o payload real da API no formato interno:

| Campo API Tecimob | Campo 7X Model | Observação |
| :--- | :--- | :--- |
| `id` (UUID) | `id` | ID da API (string UUID) |
| `reference` | `reference` | Código interno do imóvel |
| `price` (string) | `price` (float) + `price_formatted` | Parser remove `R$ .` e converte |
| `transaction` | `purpose` | `VENDA→Venda`, `ALUGUEL→Aluguel` |
| `status` | `status` | Direto da API |
| `street_address` + `street_number` | `address` | Concatenados |
| `neighborhood.name` | `neighborhood` | — |
| `neighborhood.city.name` | `city` | — |
| `neighborhood.city.state.acronym` | `state` | `"SP"`, `"RJ"`, etc. |
| `characteristics[title=Quartos].quantity` | `bedrooms` | Extraído por título |
| `characteristics[title=Vagas].quantity` | `garage` | Extraído por título |
| `characteristics[title=Banheiros].quantity` | `bathrooms` | Extraído por título |
| `characteristics[title=Suítes].quantity` | `suites` | Extraído por título |
| `areas[name=built_area].value` | `area` | Área útil em m² |
| `description` (HTML) | `description` | Tags HTML removidas com regex |
| `condominium_price` (string) | `condo_fee` (float) | Parser numérico |
| `territorial_tax_price` (string) | `iptu` (float) | Parser numérico |
| `informations[name=images]` | `gallery[]` | URLs das fotos |
| `condo_characteristics[].title` | `amenities[]` | Sem `quantity` |
| `user.name` / `.email` / `.cellphone` | `agent.name/email/phone` | Corretor do Tecimob |
| `maps_latitude` / `maps_longitude` | `latitude` / `longitude` | Detalhe apenas |
| `is_financeable` | `is_financeable` | Detalhe apenas |
| `condominium.title` | `condominium_name` | Detalhe apenas |

---

## 🛡️ 6. Resiliência & Fallback

Quando `USE_TECIMOB_API=false` ou o token não está definido, o sistema opera com o repositório local de 6 imóveis de demonstração sem nenhuma perda de funcionalidade. Quando a API está ativa, qualquer falha de conexão (timeout, HTTP 4xx/5xx) é capturada com `try/except`, logada e o sistema faz fallback para o cache local automaticamente.
