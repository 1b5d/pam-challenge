from flask import request
from flask_restful import Resource

from app.db import Event


class ReportResource(Resource):

    def __render_row(self, row, column_names):
        if isinstance(row, Event):
            result = row.to_dict()
        else:
            result = dict(zip(column_names, row))
        return result

    def get(self):
        args = request.args
        default_page_size = 10
        default_offsite = 0

        per_page = int(args.get('limit', default_page_size))
        page = (int(args.get('offset', default_offsite)) / per_page) + 1

        group_by = args.getlist('group_by')
        order_by = args.getlist('order_by')
        clients = args.getlist('clients')
        client_groups = args.getlist('client_groups')
        device_types = args.getlist('device_types')
        categories = args.getlist('categories')
        valid = args.get('valid')
        start_date = args.get('start_date')
        end_date = args.get('end_date')

        aggregates = {'count': 'id', 'sum': 'value', 'avg': 'value'}
        rows = Event.query.with_group_by(group_by, aggregates)\
            .with_order_by(order_by)

        if clients:
            rows = rows.filter(Event.client.in_(clients))

        if client_groups:
            rows = rows.filter(Event.client_group.in_(client_groups))

        if device_types:
            rows = rows.filter(Event.device_type.in_(device_types))

        if categories:
            rows.filter(Event.category.in_(categories))

        if valid:
            rows.filter(Event.valid == valid)

        if start_date:
            rows.filter(Event.timestamp >= start_date)

        if end_date:
            rows.filter(Event.timestamp <= end_date)

        rows = rows.paginate(page, per_page, error_out=False)

        return {
            'pagination': {
                'total_count': rows.total,
                'offset': (rows.page - 1) * rows.per_page,
                'page_size': rows.per_page
            },
            'rows': list(map(lambda row: self.__render_row(row, list(aggregates.keys()) + group_by), rows.items))
        }
