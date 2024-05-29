## Q2
python3 ./02-experiment-tracking/preprocess_data.py --raw_data_path ./02-experiment-tracking/taxi_data_folder --dest_path ./02-experiment-tracking/output


## Q3
python3 ./02-experiment-tracking/train.py --data_path ./02-experiment-tracking/output


## Q4
<!-- mlflow ui --backend-store-uri sqlite:///./mlflow.db -->
<!-- mlflow server --host 127.0.0.1 --port 5000 -->
mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///./mlflow.db --default-artifact-root ./artifacts
python3 train.py --data_path ./output

## Q5
python3 hpo.py --data_path ./output


## Q6
python3 register_model.py --data_path ./output