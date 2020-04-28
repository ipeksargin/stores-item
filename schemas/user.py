from marshmallow import ma
from models.user import UserModel
"""to connect schema with sqlalchemy"""

class UserSchema(ma.ModelSchema): 
    class Meta:
        model = UserModel
        load_only = ("password",) #load password but dont return(show) it
        dump_only= ("activated", "id")
