from app.views import Home, EventResource


def configure_routes(api):
    """
    A common place to register all resources of the app and map them to urls.
    :param Api api:
    :return:
    """

    api.add_resource(Home, '/', methods=['GET'], endpoint='api.home')
    api.add_resource(EventResource, '/event/<uuid>', methods=['GET', 'DELETE'], endpoint='event.get')
