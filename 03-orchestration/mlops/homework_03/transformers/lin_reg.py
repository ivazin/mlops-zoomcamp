if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


import sklearn

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, root_mean_squared_error

import mlflow
import os
import tempfile
import pickle

# mlflow.set_tracking_uri('sqlite:///./mlflow.db')
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment('my-ny-taxi')
# enable autologging
# mlflow.sklearn.autolog()


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    categorical = ['PULocationID', 'DOLocationID']
    # numerical = ['trip_distance']
    df[categorical] = df[categorical].astype(str)

    # train_dicts = df[categorical + numerical].to_dict(orient='records')
    train_dicts = df[categorical].to_dict(orient='records')
    # print("train_dicts", train_dicts)
    dv = DictVectorizer()

    X_train = dv.fit_transform(train_dicts)
    # print("X_train", X_train)
    # X_train.shape

    target = 'duration'
    y_train = df[target].values
    # y_train

    lr_model = LinearRegression()
    
    with mlflow.start_run() as run:
        lr_model.fit(X_train, y_train)

        y_pred = lr_model.predict(X_train)

        print(lr_model.intercept_)

        # mlflow.log_artifact(local_path='artifacts/rf.bin', artifact_path='artifacts')

        with tempfile.TemporaryDirectory() as temp_dir:
            
            lr_path = os.path.join(temp_dir, "LinearRegression.pkl")
            with open(lr_path, 'wb') as f_out:
                pickle.dump(lr_model, f_out)
            model_size_bytes = os.path.getsize(lr_path)

            mlflow.log_artifact(lr_path)
            # mlflow.log_model(lr_model, 'model') # from HW03 solution 

            dv_path = os.path.join(temp_dir, "DictVectorizer.pkl")

            with open(dv_path, 'wb') as f_out:
                pickle.dump(dv, f_out)

            mlflow.log_artifact(dv_path)

            mlflow.log_param("model_type", "LinearRegression")
            mlflow.log_metric("training_score", lr_model.score(X_train, y_train))
            mlflow.log_param("model_size_bytes", model_size_bytes)
            # mlflow.log_metric("test_score", lr_model.score(X_test_transformed, y_test))

    # return df
    return dv, lr_model


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'