import sys, os, shutil, json, base64
from slinn import version as slinn_version

RED = '\u001b[31m'
GREEN = '\u001b[32m'
BLUE = '\u001b[34m'
RESET = '\u001b[0m'
BOLD = '\u001b[1m'
GRAY = '\u001b[38;2;127;127;127m'


def arg_parse(arg: str):
	return base64.urlsafe_b64decode(arg.removeprefix('b64@').encode()+b'==').decode() if arg.startswith('b64@') else arg

def splits(string: str, delimeters: list[str]=[' ', '\n'], quotes: list[str]=[]):
		result = ['']
		current_quote = ''
		for char in str(string):
			if char in quotes:
				if current_quote == '':
					current_quote = char
					continue
				elif current_quote == char:
					current_quote = ''
					continue
			if current_quote == '':
				if char in delimeters:
					result.append('')
				else:
					result[-1] += char
			else:
				result[-1] += char
		return result

def get_args(expecting, text):
	text = text.strip()
	if text == '':
		return {}
	args = {'not_used': []}
	Ds = ['\n', ' ']
	Qs = ['"', "'", '`']
	spls  = splits(text, Ds, Qs)
	i = 0
	while i < len(spls):
		arg = str(spls[i])
		try:
			if arg.strip().endswith('='):
				W = arg.strip().removesuffix('=').strip()
				expecting.pop(expecting.index(W))
				args[W] = arg_parse(str(splits[i + 1]))
				i += 2
				continue
			if len(splits(arg, ['='], Qs)) == 2:
				spl = splits(arg, ['='])
				W = str(spl[0])
				if W not in args.keys():
					args[W] = arg_parse(str(spl[1]))
					expecting.pop(expecting.index(W))
				else:
					args[W] = [args[W]]
					args[W].append(arg_parse(str(spl[1])))
				i += 1
				continue
		except ValueError:
			pass

		if len(expecting) == 0:
			args['not_used'].append(arg_parse(arg))
			i += 1
			continue

		E = expecting.pop(0)
		args[E] = arg_parse(arg)
		i += 1
	return args

def replace_all(text: str, sss: list[str] | str, ss2: str) -> str:
	for ss1 in sss:
		text = text.replace(ss1, ss2)
	return text

def add_quotes_to_list(lst: list[str]):
		for l in lst:
			yield f'\'{l}\''

def update():
	project = open('project.json', 'r')
	project_json = json.loads(project.read())
	project.close()
	if 'apps' not in project_json.keys():
		return print(f'Updated project.json')
	apps = []
	for app in project_json['apps']:
		if os.path.isdir(app):
			apps.append(app)
	project_json['apps'] = apps
	project = open('project.json', 'w')
	project.write(json.dumps(project_json, indent=4))
	project.close()
	return print(f'Updated project.json')

def main():
	if len(sys.argv) > 1:
		if sys.argv[1].lower() == 'run':
			from slinn import Server, Address


			def config():
				file = open('project.json')
				cfg = json.loads(file.read())
				file.close()
				return cfg


			def load_imports(apps):
				imports = []
				for app in apps:
					imports.append(f'from {app} import dp_{app}')
				return imports


			def get_dispatchers(apps):
				dispachers = []
				for app in apps:
					dispachers.append(f'dp_{app}')
				return dispachers


			cfg = config()
			apps = cfg['apps'] if 'apps' in cfg.keys() else []
			port = cfg['port'] if 'port' in cfg.keys() else 8080
			host = cfg['host'] if 'host' in cfg.keys() else ''
			ssl_fullchain, ssl_key = None, None
			if 'ssl' in cfg.keys() and 'fullchain' in cfg.keys() and 'key' in cfg.keys():
				ssl_fullchain = '"'+cfg['ssl']['fullchain']+'"' if cfg['ssl']['fullchain'] else None    
				ssl_key = '"'+cfg['ssl']['key']+'"' if cfg['ssl']['key'] else None
			start = ';'.join(load_imports(apps))+f';Server({",".join(get_dispatchers(apps))}, ssl_fullchain={ssl_fullchain}, ssl_key={ssl_key}).listen(Address({port}, "{host}"))'
			print('Starting server...')
			exec(start)
		elif sys.argv[1].lower() == 'create':
			args = get_args(['name', 'host'], ' '.join(sys.argv[2:]))
			if 'name' not in args.keys():
				return print(f'{RED}The app`s name is not specified{RESET}')
			ensure_appname = replace_all(args['name'], '-&$#!@%^().,', '_')
			if os.path.isdir(ensure_appname):
				return print(f'{BLUE}The app named {args["name"]} exists{RESET}')
			os.mkdir(ensure_appname)
			with open(f'{ensure_appname}/__init__.py', 'w') as f:
				data = """from %appname%.app import dp_%appname%
""".replace('%appname%', ensure_appname)
				f.write(data)
			with open(f'{ensure_appname}/app.py', 'w') as f:
				data = """from slinn import Dispatcher, Filter, HttpResponse
 
dp_%appname% = Dispatcher(%host%)

# Write your code down here                         
""".replace('%appname%', ensure_appname).replace('%host%', '' if 'host' not in args.keys() else ', '.join(add_quotes_to_list(args['host'] if type(args['host']) == list else [args['host']])))
				f.write(data)
			fr = open('project.json', 'r')
			fj = json.loads(fr.read())
			fr.close()
			if 'apps' in fj.keys():
				fj['apps'].append(ensure_appname)
			else:
				fj['apps'] = []
			fw = open('project.json', 'w')
			fw.write(json.dumps(fj, indent=4))
			fw.close()
			update()
			print(f'{GREEN}App successfully created{RESET}')
		elif sys.argv[1].lower() == 'delete':
			args = get_args(['name'], ' '.join(sys.argv[2:]))
			if 'name' not in args.keys():
				return print(f'{RED}The app`s name is not specified{RESET}')
			ensure_appname = replace_all(args['name'], '-&$#!@%^().,', '_')
			if not os.path.isdir(ensure_appname):
				return print(f'{BLUE}The app named {args["name"]} does not exist{RESET}')
			if input(f'{RESET}Are you sure? (y/N) >>> ').lower() not in ['y', 'yes']:
				return print(f'{RESET}Aborted')
			shutil.rmtree(ensure_appname)
			update()
			return print(f'{GREEN}App successfully deleted{RESET}')
		elif sys.argv[1].lower() == 'update':
			return update()
		elif sys.argv[1].lower() == 'help':
			return print("""%BOLD%Slinn manager help page

Commands%RESET%:
	%cmd% run                                                              %GRAY%# Starts server%RESET%
	%cmd% create {app`s name} host=(host1) host=(host2)...                 %GRAY%# Creates a new app
		Example: %cmd% create localhost host=localhost host=127.0.0.1%RESET%
	%cmd% delete {app`s name}                                              %GRAY%# Deletes an app
		Example: %cmd% delete localhost%RESET%
	%cmd% template {template`s name} (projects`s path)                     %GRAY%# Installs a template
		Example: %cmd% template firstrun%RESET%
	%cmd% update                                                           %GRAY%# Updates project.py%RESET%
	%cmd% help                                                             %GRAY%# Prints this help%RESET%
	%cmd% version                                                          %GRAY%# Prints version of Slinn%RESET%
""".replace('%cmd%', f'py {sys.argv[0]}').replace('%GRAY%', GRAY).replace('%RESET%', RESET).replace('%BOLD%', BOLD))
		elif sys.argv[1].lower() == 'version':
			return print(slinn_version)
		elif sys.argv[1].lower() == 'template':
			args = get_args(['name', 'path'], ' '.join(sys.argv[2:]))
			apppath = (args['path']+'?').replace('/?', '').replace('?', '') if 'path' in args.keys() else '.'
			if 'name' not in args.keys():
				return print(f'{RED}Template name is not specified{RESET}')
			modulepath = os.path.abspath(slinn.__file__).replace('__init__.py', '')
			try:
				shutil.copytree(f'{modulepath}templates/{args["name"]}/', f'{apppath}/{args["name"]}')
				return print(f'{GREEN}Template {args["name"]} successfully installed{RESET}') 
			except FileExistsError:
				return print(f'{BLUE}Template {args["name"]} has already existed installed{RESET}')
			except FileNotFoundError:
				return print(f'{BLUE}Template {args["name"]} not found{RESET}')
		else:
			return print(f'{RED}Command {sys.argv[1].lower()} is not exists{RESET}')
	else:
		return print(f'{RED}Command was not specified{RESET}')

			
if __name__ == '__main__':
	main()