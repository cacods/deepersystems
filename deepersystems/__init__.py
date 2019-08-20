from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from .models import DBSession, Base


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings,
                          root_factory='deepersystems.models.Root')
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
