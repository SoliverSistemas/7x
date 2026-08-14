# Documentação Oficial da Stack Tecnológica & Integração Tecimobi API

**Projeto:** 7X Imóveis — Plataforma Imobiliária de Alto Padrão  
**Versão:** 1.1.0  
**Data:** 14/08/2026  

---

## 🛠️ 1. Stack Tecnológica Completa

O sistema foi desenvolvido seguindo as melhores práticas de arquitetura de software, alta performance e design responsivo.

### 🐍 Backend & Servidor
- **Python 3.12+**: Linguagem base para processamento das regras de negócio.
- **Flask 3.1.3**: Microframework Python leve e escalável.
- **Application Factory Pattern (`create_app`)**: Padrão de projeto utilizado para instanciar a aplicação, permitindo alternância simples entre ambientes de Desenvolvimento, Teste e Produção.
- **Flask Blueprints**: Modularização das rotas do sistema:
  - `main_bp` (`/`): Páginas institucionais (Início, Sobre Nós, Contato).
  - `properties_bp` (`/imoveis`): Catálogo interativo e visualização detalhada de imóveis.
  - `api_bp` (`/api`): REST API JSON para busca rápida via AJAX, calculadora de financiamento e agendamento de visitas.
- **Jinja2 Templating**: Engine de renderização HTML com filtros customizados de moeda brasileira (`R$ 2.850.000,00`) e área (`m²`).

### 🎨 Frontend & Design System
- **HTML5 Semântico**: Estrutura acessível com marcações otimizadas para SEO.
- **Vanilla CSS3**: Design System moderno sem frameworks pesados, utilizando:
  - **CSS Custom Properties (Variables)** para tokens de cores (*Midnight Navy*, *Amber Gold*, *Emerald Green*).
  - **Glassmorphism & Backdrop Blur** no cabeçalho e caixa de pesquisa.
  - **CSS Grid & Flexbox** para layouts totalmente responsivos em desktop, tablet e mobile.
- **Tipografia**: Fontes do Google Fonts (*Plus Jakarta Sans* para títulos e *Inter* para textos).
- **JavaScript ES6+ Vanilla**: Manipulação leve do DOM, requisições assíncronas `fetch` (AJAX), filtros dinâmicos sem recarregar a página e armazenamento local (`localStorage`) para salvar imóveis favoritos.

### 🎬 Animações Avançadas (GSAP 3)
- **GSAP 3 (GreenSock Animation Platform)**: Biblioteca para animações web de alta performance.
- **GSAP ScrollTrigger Plugin**: Gatilhos baseados em rolagem de tela para revelar elementos conforme a navegação do usuário.
- **Efeitos Implementados**:
  - *Hero Animation Timeline*: Revelação em cascata da marca, título, subtítulo e caixa de busca na abertura da página.
  - *Staggered Cards Entrance*: Animação fluida e sequencial na exibição dos cards de imóveis.
  - *Micro-interações de Hover*: Elevação suave dos cards e botões interativos.

---

## 🔌 2. Integração com a API da Tecimobi

O sistema conta com um módulo nativo de integração com o ERP/CRM imobiliário **Tecimobi** ([https://api.tecimobi.com.br](https://api.tecimobi.com.br)).

### 🗺️ Arquitetura da Integração
A integração é intermediada pela classe `TecimobiService` ([`app/services/tecimobi_service.py`](file:///c:/Users/Caveira%20Soliver/Documents/7x/7x_site/app/services/tecimobi_service.py)) e consumida pela camada de modelo `PropertyRepository` ([`app/models/property_model.py`](file:///c:/Users/Caveira%20Soliver/Documents/7x/7x_site/app/models/property_model.py)).

```text
[ Painel Tecimobi ERP ] 
        │ (REST JSON API)
        ▼
[ TecimobiService ] 
        │ (Normalização do Payload)
        ▼
[ PropertyRepository ] 
        │ (Filtros & Buscas)
        ▼
[ Blueprints / UI HTML5 + GSAP ]
```

### ⚙️ Configuração de Variáveis de Ambiente (`config.py` / `.env`)

Para ativar a sincronização ao vivo com a API da Tecimobi, configure as variáveis abaixo no arquivo `.env` ou em [`config.py`](file:///c:/Users/Caveira%20Soliver/Documents/7x/7x_site/config.py):

```env
USE_TECIMOBI_API=true
TECIMOBI_API_URL=https://api.tecimobi.com.br/v1
TECIMOBI_API_KEY=sua_chave_de_api_tecimobi_aqui
TECIMOBI_ACCOUNT_ID=seu_id_de_conta_aqui
```

### 📡 Endpoints Consumidos

1. **Listagem de Imóveis**:
   - `GET /v1/imoveis?page={page}&limit={limit}&finalidade={finalidade}&tipo={tipo}&cidade={cidade}`
   - Retorna a lista de imóveis cadastrados e ativos no CRM Tecimobi.

2. **Detalhes do Imóvel**:
   - `GET /v1/imoveis/{id}`
   - Retorna a ficha completa, incluindo galeria de fotos em alta resolução, ficha técnica e dados do corretor responsável.

### 🔄 Mapeamento de Dados (Normalization Pipeline)

O `TecimobiService` converte a estrutura do JSON da Tecimobi no formato padronizado da plataforma 7X Imóveis:

| Campo Tecimobi API | Campo 7X Imóveis Model | Tipo de Dado | Descrição |
| :--- | :--- | :--- | :--- |
| `id` / `codigo` | `id` | `Integer` | Código único do anúncio |
| `titulo` / `nome` | `title` | `String` | Título do anúncio |
| `valor_venda` / `valor_locacao` | `price` | `Float` | Valor do imóvel |
| `area_util` / `area_total` | `area` | `Float` | Área em metros quadrados ($m^2$) |
| `dormitorios` | `bedrooms` | `Integer` | Quantidade de quartos |
| `vagas` | `garage` | `Integer` | Vagas de garagem |
| `endereco.bairro` | `neighborhood` | `String` | Bairro do imóvel |
| `endereco.cidade` | `city` | `String` | Cidade do imóvel |
| `fotos` / `imagens` | `gallery` | `List[String]` | URLs da galeria de fotos |
| `diferenciais` | `amenities` | `List[String]` | Lista de comodidades |

### 🛡️ Estratégia de Fallback e Resiliência
Caso a chave de API da Tecimobi não seja fornecida ou haja alguma instabilidade na conexão remota, o sistema alterna automaticamente para o repositório local com cache de segurança, garantindo que o site permaneça 100% funcional e responsivo.
