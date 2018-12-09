import json


def to_json_serializable(ma_schema, object):
    """
    Convert marshmallow schema to python serializable dictionary/list
    :param ma_schema: marshmallow schema object
    :param object: any data object / generally sqlalchemy record object
    :return: dictionary representing object
    """
    try:
        return json.loads(ma_schema.dumps(object).data)
    except Exception as e:
        print('Unable to convert Error:', e)
