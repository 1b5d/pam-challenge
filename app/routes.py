from app.views.event import Home, EventResource
from app.views.report import ReportResource


def configure_routes(api):
    """
    A common place to register all resources of the app and map them to urls.
    :param Api api:
    :return:
    """

    api.add_resource(Home, '/', methods=['GET'], endpoint='api.home')
    api.add_resource(EventResource, '/event/<uuid>', methods=['GET', 'DELETE'], endpoint='event.get')
    api.add_resource(EventResource, '/event', methods=['POST'], endpoint='event.post')
    api.add_resource(ReportResource, '/report', methods=['GET'], endpoint='report.get')
