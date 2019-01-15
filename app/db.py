from enum import Enum

from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import func
from sqlalchemy.orm import class_mapper, ColumnProperty

db = SQLAlchemy()


class EventDeviceType(str, Enum):
    DESKTOP = 'desktop'
    MOBILE = 'mobile'
    TABLET = 'tablet'

    @classmethod
    def values(cls):
        return list(map(lambda item: item.value, list(cls)))


class EventQuery(BaseQuery):
    def with_group_by(self, group_by, aggregates):
        if not group_by:
            return self
        aggregates = (getattr(func, k)(getattr(Event, v)) for k, v in aggregates.items())
        selection = tuple(map(lambda col: getattr(Event, col), group_by))
        group_by_columns = tuple(map(lambda col: getattr(Event, col), group_by))
        return self.from_self(*aggregates, *selection).group_by(*group_by_columns)

    def with_order_by(self, order_by):
        if not order_by:
            return self

        col_converter = lambda col: col if not col.startswith('-') \
            else col.replace('-', '') + ' desc'
        order_by_columns = ' '.join(map(col_converter, order_by))
        return self.order_by(order_by_columns)


class Event(db.Model):
    query_class = EventQuery

    id = db.Column(db.String, primary_key=True)
    device_type = db.Column(db.Enum(EventDeviceType), nullable=True)
    category = db.Column(db.Integer, nullable=True)
    client = db.Column(db.Integer, nullable=False)
    client_group = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    valid = db.Column(db.Boolean, nullable=False)
    value = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.id

    @classmethod
    def attribute_names(cls):
        return [prop.key for prop in class_mapper(cls).iterate_properties
                if isinstance(prop, ColumnProperty)]

    def to_dict(self):
        """
        This method is supposed to serialize the object into json
        to be able to be returned by the API. I don't like this way
        of serializing, I would rather separate the serialization logic
        in a separate place than the models themselves. And even use
        a third-party library for that like marshmallow
        https://marshmallow.readthedocs.io/en/3.0/

        :return str:
        """
        return {
            'id': self.id,
            'device_type': self.device_type.value if self.device_type else None,
            'category': self.category,
            'client': self.client,
            'client_group': self.client_group,
            # Maybe there is a cleaner way of formatting the datetime
            'timestamp': self.timestamp.isoformat(timespec='milliseconds') + 'Z',
            'valid': self.valid,
            'value': self.value
        }
