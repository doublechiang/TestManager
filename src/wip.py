from flask_restful_swagger_3 import swagger, Resource, Schema

from sfhand import SfHand

class Wip(Resource):
    def get(self):
        wip  = SfHand().getWip()
        return wip
    
class WipModel(Schema):
    properties = { 
        'racksn' : {
            'location' : 'string',
            'racksn' : 'string',
            'uuts': list('string')
        } 
    }
