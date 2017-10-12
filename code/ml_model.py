from typing import List
import pandas as pd
from sklearn.externals import joblib
from code.models import ModelInput


class MLModel:
    """
    Sklearn wrapper
    """

    def __init__(self):
        self.__ml_pipeline = joblib.load('data/model.pkl')
        self.__features_cols = joblib.load('data/cols.pkl')

    def predict(self, data: List[ModelInput]) -> List:
        # create Matrix from input data
        data_dicts = [d._asdict() for d in data]
        data_df = pd.DataFrame(data_dicts)
        # arrange features in way it was passed in model
        data_df = data_df[self.__features_cols]

        return self.__ml_pipeline.predict(data_df)
