import collections
import envy.logger as log
import os
import os.path

config = collections.namedtuple('conig', 
	['location', 'plugins'])

def ensure_dir(path):
	if os.path.isfile(path):
		err = 'Directory [%s] is actually a file!' % path
		log.error(err)
		raise err

	if not os.path.exists(path):
		log.warning('Directory [%s] does not exist, creating it now' % path)
		os.makedirs(path)

	return path

def find_envy_dir(basedir=os.environ['HOME']):
	root_dir = os.path.join(basedir, '.envy')

	ensure_dir(root_dir)
	ensure_dir(os.path.join(root_dir, 'logs'))
	ensure_dir(os.path.join(root_dir, 'plugins'))

	return root_dir

def load_system_config():
	log.debug('Loading system-level envy configuration')
	root_dir = find_envy_dir()

	return config(location=root_dir, plugins=[])
