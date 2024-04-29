from datetime import datetime

class DataTransformer():
    def __init__(self):
        pass

    @classmethod
    def models_to_dict_list(cls, models):
        data = [cls.model_to_dict(model) for model in models]
        return data
    
    @classmethod
    def model_to_dict(cls, model):
        return {column.name: getattr(model,column.name) for column in model.__table__.columns}
    
    @classmethod
    def get_current_time(cls):
        return datetime.now()