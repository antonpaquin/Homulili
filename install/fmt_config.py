import jinja2
import os
import json
import random

# Places where a secret.py and a config.py will be generated
config_link_locations = [
    'src/bots/parser',
    'src/bots/scraper',
    'src/bots/scanner',
    'src/frontend/flask',
    'src/backend/flask',
    'src/backend/flask_interface',
    'src/cdn/flask',
    'scripts',
]

config_location = 'src'


# Templates that will be filled as needed
templates = [
    'install/postgres.sh.j2',
]


# Variables that the user needs to specify
prompt_vars = (
    'madokami_uname',
    'madokami_pass',
    'storage_dir',
    'user_database_dir',
    'api_hostname',
    'api_internal_port',
    'api_public_port',
    'admin_hostname',
    'admin_internal_port',
    'admin_public_port',
    'cdn_hostname',
    'cdn_internal_port',
    'cdn_public_port',
)

# Ask user for variables
args = {}
for arg in prompt_vars:
    args[arg] = input(arg + '= ')


# Generate a postgres password automatically
args['postgres_password'] = ''.join([random.choice(
    'abcdefghijlkmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
) for _ in range(30)])


# Find current project root automatically
project_root = os.path.dirname(os.getcwd())
args['project_root'] = project_root


# Prompt user to check input
print(json.dumps(args, indent=4))
print('Is this okay?')
if input('y/N').lower() not in {'yes', 'y', 'ye'}:
    exit(0)


# Generate config and secret output from templates
with open('template_conf/config.py.j2', 'r') as config_f:
    config_output = jinja2.Template(config_f.read()).render(**args)
with open('template_conf/secret.py.j2', 'r') as secret_f:
    secret_output = jinja2.Template(secret_f.read()).render(**args)

config_true_fname = os.path.join(project_root, config_location, 'config.py')
with open(config_true_fname, 'w') as config_f:
    config_f.write(config_output)
secret_true_fname = os.path.join(project_root, config_location, 'secret.py')
with open(secret_true_fname, 'w') as secret_f:
    secret_f.write(secret_output)


# Write config and secret outputs
for fname in config_link_locations:
    config_link_fname = os.path.join(project_root, fname, 'config.py')
    if not os.path.exists(config_link_fname):
        os.symlink(config_true_fname, config_link_fname)

    secret_link_fname = os.path.join(project_root, fname, 'secret.py')
    if not os.path.exists(secret_link_fname):
        os.symlink(secret_true_fname, secret_link_fname)


# Write less-generic templates
for fname in templates:
    out_fname = fname[:-3]
    with open(os.path.join(project_root, fname), 'r') as template_f:
        template = jinja2.Template(template_f.read())
    with open(os.path.join(project_root, out_fname), 'w') as out_f:
        out_f.write(template.render(**args))
