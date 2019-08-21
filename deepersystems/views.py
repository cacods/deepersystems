import colander
import deform
from bson import ObjectId
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .models import DBSession, Video, Theme


class VideoViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def video_form(self):

        class Schema(colander.Schema):
            choices = [('', '- Select -')]
            themes = self.request.db['themes'].find()
            for theme in themes:
                choices.append((theme['_id'], theme['name']))
            name = colander.SchemaNode(colander.String())
            theme = colander.SchemaNode(
                colander.String(),
                widget=deform.widget.SelectWidget(values=choices),
            )
        schema = Schema()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.video_form.get_widget_resources()

    @view_config(route_name='videos_view', renderer='videos_view.pt')
    def videos_view(self):
        videos = self.request.db['videos'].find()
        return dict(title='Videos View', videos=videos)

    @view_config(route_name='video_add',
                 renderer='video_addedit.pt')
    def video_add(self):
        form = self.video_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.video_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(form=e.render())

            name = appstruct['name']
            theme_id = appstruct['theme']
            # TODO: Put try/exception here for catch not existent model
            #  instance
            theme = self.request.db['themes'].find_one(
                {'_id': ObjectId(theme_id)})
            video_id = self.request.db['videos'].insert_one(
                {'name': name, 'theme_id': theme['_id']}
            ).inserted_id

            url = self.request.route_url('video_view', uid=video_id)
            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='video_view', renderer='video_view.pt')
    def video_view(self):
        video_id = self.request.matchdict['uid']
        # video = DBSession.query(Video).filter_by(uid=uid).one()
        # theme = DBSession.query(Theme).filter_by(uid=video.theme_uid).one()
        video = self.request.db['videos'].find_one({'_id': ObjectId(video_id)})
        theme = self.request.db['themes'].find_one(
            {'_id': ObjectId(video['theme_id'])}
        )

        return dict(video=video, theme=theme)

    @view_config(route_name='video_edit',
                 renderer='video_addedit.pt')
    def video_edit(self):
        video_id = self.request.matchdict['uid']
        video = self.request.db['videos'].find_one(
            {'_id': ObjectId(video_id)}
        )

        video_form = self.video_form

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = video_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(video=video, form=e.render())

            new_name = appstruct['name']
            new_theme_id = appstruct['theme']
            self.request.db['videos'].find_one_and_update(
                {'_id': ObjectId(video_id)},
                {'$set': {'name': new_name, 'theme_id': ObjectId(new_theme_id)}}
            )
            url = self.request.route_url('video_view', uid=video_id)
            return HTTPFound(url)

        form = self.video_form.render(dict(
            name=video['name'], theme=video['theme_id']
        ))

        return dict(video=video, form=form)

    @view_config(route_name='thumbsup_view')
    def thumbsup_view(self):
        uid = int(self.request.matchdict['uid'])
        video = DBSession.query(Video).filter_by(uid=uid).one()
        video.thumbs_up += 1
        theme = DBSession.query(Theme).filter_by(uid=video.theme_uid).one()
        theme.score = 0
        for video in theme.videos:
            theme.score += video.thumbs_up + video.thumbs_down / 2
        url = self.request.route_url('videos_view')
        return HTTPFound(url)

    @view_config(route_name='thumbsdown_view')
    def thumbsdown_view(self):
        uid = int(self.request.matchdict['uid'])
        video = DBSession.query(Video).filter_by(uid=uid).one()
        video.thumbs_down += 1
        theme = DBSession.query(Theme).filter_by(uid=video.theme_uid).one()
        theme.score = 0
        for video in theme.videos:
            theme.score += video.thumbs_up + video.thumbs_down / 2
        url = self.request.route_url('videos_view')
        return HTTPFound(url)


class ThemePage(colander.MappingSchema):
    name = colander.SchemaNode(colander.String())


class ThemeViews(object):
    def __init__(self, request):
        self.request = request

    @property
    def theme_form(self):
        schema = ThemePage()
        return deform.Form(schema, buttons=('submit',))

    @property
    def reqts(self):
        return self.theme_form.get_widget_resources()

    @view_config(route_name='themes_view', renderer='themes_view.pt')
    def themes_view(self):
        themes = self.request.db['themes'].find()
        return dict(title='Themes View', themes=themes)

    @view_config(route_name='theme_add',
                 renderer='theme_addedit.pt')
    def theme_add(self):
        form = self.theme_form.render()

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = self.theme_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(form=e.render())

            name = appstruct['name']
            theme_id = self.request.db['themes'].insert_one(
                {'name': name}).inserted_id

            url = self.request.route_url('theme_view', uid=theme_id)
            return HTTPFound(url)

        return dict(form=form)

    @view_config(route_name='theme_view', renderer='theme_view.pt')
    def theme_view(self):
        theme_id = self.request.matchdict['uid']
        theme = self.request.db['themes'].find_one({'_id': ObjectId(theme_id)})
        return dict(theme=theme)

    @view_config(route_name='theme_edit',
                 renderer='theme_addedit.pt')
    def theme_edit(self):
        theme_id = self.request.matchdict['uid']
        theme = self.request.db['themes'].find_one(
            {'_id': ObjectId(theme_id)}
        )

        theme_form = self.theme_form

        if 'submit' in self.request.params:
            controls = self.request.POST.items()
            try:
                appstruct = theme_form.validate(controls)
            except deform.ValidationFailure as e:
                return dict(video=theme, form=e.render())

            new_name = appstruct['name']
            self.request.db['themes'].find_one_and_update(
                {'_id': ObjectId(theme_id)},
                {'$set': {'name': new_name}},
            )
            url = self.request.route_url('theme_view', uid=theme_id)
            return HTTPFound(url)

        form = self.theme_form.render(dict(
            name=theme['name']
        ))

        return dict(theme=theme, form=form)
