from BusTrack.controllers.parent.KidProfileController import KidProfileController


def register_controllers(api, prefix):
    """
    register all controllers in parent package
    :param api: flask_restful object
    :param prefix: prefix url to be append while adding resource
    :return: None
    """
    api.add_resource(KidProfileController,
                     prefix + '/kid',
                     prefix + '/kid/<int:kid_id>')
