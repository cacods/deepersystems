import unittest

import transaction
from pyramid import testing


def _initTestingDB():
    from sqlalchemy import create_engine
    from .models import (
        DBSession,
        Theme,
        Video,
        Base
    )
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    with transaction.manager:
        theme_model = Theme(uid=1, name='Music')
        model = Video(name='FrontPage', theme_uid=theme_model.uid)
        DBSession.add(model)
    return DBSession


class VideosViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_videos_view(self):
        from deepersystems.views import VideoViews

        request = testing.DummyRequest()
        inst = VideoViews(request)
        response = inst.videos_view()
        self.assertEqual(response['title'], 'Videos View')


class VideosFunctionalTests(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('development.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        from .models import DBSession
        DBSession.remove()

    def test_it(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Videos: View', res.body)
        res = self.testapp.get('/add', status=200)
        self.assertIn(b'Add/Edit', res.body)


class ThemesViewTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_videos_view(self):
        from deepersystems.views import ThemeViews

        request = testing.DummyRequest()
        inst = ThemeViews(request)
        response = inst.themes_view()
        self.assertEqual(response['title'], 'Themes View')


class ThemesFunctionalTests(unittest.TestCase):
    def setUp(self):
        from pyramid.paster import get_app
        app = get_app('development.ini')
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        from .models import DBSession
        DBSession.remove()

    def test_it(self):
        res = self.testapp.get('/themes', status=200)
        self.assertIn(b'Themes: View', res.body)
        res = self.testapp.get('/themes/add', status=200)
        self.assertIn(b'Add/Edit', res.body)
