import urllib.request
import re

req = urllib.request.Request('https://swagger.tecimob.com.br/', headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8')
print("Fetched HTML:", len(html), "bytes")

match = re.search(r'url:\s*[\"\'\']([^\"\'\']+)[\"\'\']', html)
print('Match:', match)
if match:
    swagger_url = match.group(1)
    if not swagger_url.startswith('http'):
        swagger_url = 'https://swagger.tecimob.com.br/' + swagger_url.lstrip('/')
    print('Swagger URL:', swagger_url)
    
    import json
    req2 = urllib.request.Request(swagger_url, headers={'User-Agent': 'Mozilla/5.0'})
    json_data = urllib.request.urlopen(req2).read().decode('utf-8')
    data = json.loads(json_data)
    
    schemas = data.get('components', {}).get('schemas', {}) or data.get('definitions', {})
    for name, schema in schemas.items():
        if 'prop' in name.lower() or 'imovel' in name.lower():
            print(f'Found schema: {name}')
            if 'properties' in schema:
                keys = list(schema['properties'].keys())
                print(f'Fields for {name}: {keys}')
                if 'title' in keys or 'titulo' in keys or 'nome' in keys:
                    print(f'---> HAS TITLE!')
