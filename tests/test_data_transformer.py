from datetime import datetime
from src.data_transformer import DataTransformer
from unittest.mock import patch
import unittest

class TestDataTransformer(unittest.TestCase):

    class Column:
        def __init__(self, name):
            self.name = name
    class DummyTable:
        def __init__(self, cols):
            self.columns = [TestDataTransformer.Column(col) for col in cols]
    class DummyModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.__table__ = TestDataTransformer.DummyTable(vars(self).keys())


    def test_models_to_dict_list_should_pass_when_models_are_valid(self):
        models = [
            TestDataTransformer.DummyModel(name='John', age=30),
            TestDataTransformer.DummyModel(name='Alice', age=25)
        ]
        expected_result = [
            {'name': 'John', 'age': 30},
            {'name': 'Alice', 'age': 25}
        ]
        assert DataTransformer.models_to_dict_list(models) == expected_result

    def test_model_to_dict_should_pass_when_model_is_valid(self):
        model = TestDataTransformer.DummyModel(name='John', age=30)
        expected_result = {'name': 'John', 'age': 30}
        assert DataTransformer.model_to_dict(model) == expected_result

    @patch('src.data_transformer.datetime')
    def test_get_current_time(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 4, 24, 12, 0, 0)
        
        expected_result = datetime(2024, 4, 24, 12, 0, 0)
        assert DataTransformer.get_current_time() == expected_result