import datetime

from flask_sqlalchemy import Model
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import class_mapper

import config


def serialize(model, ignore_list=[]):
    if isinstance(model, list):
        result = []
        for row in model:
            result.append(_serialize_model(row, ignore_list))
        return result
    else:
        return _serialize_model(model, ignore_list)


def _serialize_model(model, ignore_list=[]):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    filter_column = ['_sa_instance_state', 'password']
    filter_column += ignore_list
    columns = [c for c in model.__dict__ if c not in filter_column]
    # then we return their values in a dict
    result = {}
    for c in columns:
        attr = getattr(model, c)
        if isinstance(attr, datetime.datetime):
            attr = attr.strftime(config.DATETIME_FORMAT)
        elif isinstance(attr, datetime.date):
            attr = attr.strftime(config.DATE_FORMAT)
        elif isinstance(attr, Model):
            attr = _serialize_model(attr)
        result[c] = attr
    return result
