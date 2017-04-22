# some validation code related to form
from wtforms.validators import ValidationError

class Unique(object):
    def __init__(self,model,field=None,message='Element already exist.'):
        self.model=model
        self.field=field
        self.message=message

    def __call__(self,form,field):
        # check if this field already exist in Model
        # in case model require no field
        check=False
        if field is None:
            check=self.model.is_unique()
        else:
            check=self.model.is_unique(field.raw_data[0])
        if check==False:
            raise ValidationError(self.message)