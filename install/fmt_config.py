import jinja2
import os
import json


templates = [
    'src/bots/scanner/secret.py.j2',
    'src/bots/parser/config.py.j2',
    'src/bots/scraper/secret.py.j2',
    'src/bots/scraper/config.py.j2',
    'src/frontend/flask/config.py.j2',
    'src/frontend/flask/secret.py.j2',
    'src/manga_host/flask_interface/config.py.j2',
    'src/manga_host/flask/secret.py.j2',
    'src/manga_host/flask/config.py.j2',
    'install/postgres.sh.j2',
]

prompt_vars = (
    'madokami_uname',
    'madokami_pass',
    'storage_dir',
    'api_hostname',
    'api_internal_port',
    'api_public_port',
    'admin_hostname',
    'admin_internal_port',
    'admin_public_port',
    'postgres_pass',
    'auth_key',
)

args = {}
for arg in prompt_vars:
    args[arg] = input(arg + '= ')

project_root = os.path.dirname(os.getcwd())
args['project_root'] = project_root

templates = [project_root + '/' + t for t in templates]

print(json.dumps(args, indent=4))
print('Is this okay?')
if input('y/N').lower() not in {'yes', 'y', 'ye'}:
    exit(0)

for template_fname in templates:
    with open(template_fname, 'r') as template_f:
        template = jinja2.Template(template_f.read())
    output_fname = template_fname[:-3]
    with open(output_fname, 'w') as output_f:
        output_f.write(template.render(**args))
