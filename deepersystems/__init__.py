from urllib.parse import urlparse

from gridfs import GridFS
from pymongo import MongoClient
from pyramid.config import Configurator

from .models import DBSession, Base


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory='deepersystems.models.Root')

    db_url = urlparse(settings['mongo_uri'])
    config.registry.db = MongoClient(
        host=db_url.hostname,
        port=db_url.port,
    )

    def add_db(request):
        db = config.registry.db[db_url.path[1:]]
        if db_url.username and db_url.password:
            db.authenticate(db_url.username, db_url.password)
        return db

    def add_fs(request):
        return GridFS(request.db)

    config.add_request_method(add_db, 'db', reify=True)
    config.add_request_method(add_fs, 'fs', reify=True)

    config.include('pyramid_chameleon')
    # Thumbs views
    config.add_route('thumbsup_view', '/thumbs_up/{uid}')
    config.add_route('thumbsdown_view', '/thumbs_down/{uid}')
    # Themes views
    config.add_route('themes_view', '/themes')
    config.add_route('theme_add', '/themes/add')
    config.add_route('theme_view', '/themes/{uid}')
    config.add_route('theme_edit', '/themes/{uid}/edit')
    # Videos views
    config.add_route('videos_view', '/')
    config.add_route('video_add', '/add')
    config.add_route('video_view', '/{uid}')
    config.add_route('video_edit', '/{uid}/edit')

    config.add_static_view('deform_static', 'deform:static/')
    config.scan('.views')
    return config.make_wsgi_app()
