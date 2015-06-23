import collections
import envy.logger as log
import envy.static as static
import os
import os.path
import shutil


config = collections.namedtuple('config', 
    ['location', 'plugins'])


class ConfigurationException(Exception):
    pass


# TODO: Create catchable exceptions for these failures
def ensure_envy_dir(path, autocreate):
    if os.path.isfile(path):
        err = 'Directory [%s] is actually a file!' % path
        log.error(err)
        raise ConfigurationException(err)

    if not os.path.exists(path):
        if autocreate:
            log.warning('Directory [%s] does not exist, creating it now' % path)
            os.makedirs(path)
        else:
            err = 'No envy directory exists at path [%s]. ' % path \
                + 'Try initializing one first with "envy init"'
            log.error(err)
            raise ConfigurationException(err)

    return path


def delete_envy_dir(basedir):
    root_dir = os.path.join(basedir, '.envy')
    shutil.rmtree(root_dir)


def find_envy_dir(basedir, autocreate):
    root_dir = os.path.join(basedir, '.envy')

    ensure_envy_dir(root_dir, autocreate)
    ensure_envy_dir(os.path.join(root_dir, 'bin'), autocreate)
    ensure_envy_dir(os.path.join(root_dir, 'logs'), autocreate)
    ensure_envy_dir(os.path.join(root_dir, 'plugins'), autocreate)

    return root_dir


def load_system_config():
    log.debug('Loading system-level envy configuration')
    root_dir = find_envy_dir(os.environ['HOME'], autocreate=True)

    return config(location=root_dir, plugins=[])


def load_config(basedir, autocreate):
    log.debug('Loading envy configuration')
    root_dir = find_envy_dir(basedir, autocreate=autocreate)

    with open(os.path.join(root_dir, 'init'), 'w') as f:
        f.write(static.__ACTIVATOR)

    return config(location=root_dir, plugins=[])


class Environment(object):
    def __init__(self, basedir):
        self.basedir = basedir
        self.name = os.path.basename(self.basedir)


    # TODO: Break out into separate `create`, `check`, and `load` methods
    def init(self, autocreate=False):
        self.system_config = load_system_config()
        self.config = load_config(self.basedir, autocreate)


    def destroy(self):
        delete_envy_dir(self.basedir)


    @property
    def extra_path(self):
        config_locations = [self.config.location, self.system_config.location]
        dirs = [os.path.join(p, 'bin') for p in config_locations]
        return ':'.join(dirs)
