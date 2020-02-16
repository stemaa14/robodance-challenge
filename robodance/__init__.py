from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
from .model import appmaker


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings)
    settings = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'
    config.scan()
    return config.make_wsgi_app()
