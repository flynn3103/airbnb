import os

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor 

from src.utils.config import set_env_vars

# setting env vars for minio artifact storage
set_env_vars()

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

# creates a new mlflow experiment MLFLOW_EXPERIMENT_NAME if it doesn't exist
exps = [exp.name for exp in mlflow.tracking.MlflowClient().list_experiments()]
if not os.getenv("MLFLOW_EXPERIMENT_NAME") in exps:
    mlflow.create_experiment(
        os.getenv("MLFLOW_EXPERIMENT_NAME"),
        artifact_location=os.getenv("MLFLOW_ARTIFACT_LOCATION"),
    )

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def eval_cross_validation(model, X, y, k):
    rmse = (-cross_val_score(model, X, y, cv=k, scoring='neg_root_mean_squared_error'))
    mae = (-cross_val_score(model, X, y, cv=k, scoring='neg_mean_absolute_error'))
    r2 = cross_val_score(model, X, y, cv=k, scoring='r2')
    return rmse, mae, r2

def fetch_logged_data(run_id):
    client = mlflow.tracking.MlflowClient()
    data = client.get_run(run_id).data
    tags = {k: v for k, v in data.tags.items() if not k.startswith("mlflow.")}
    artifacts = [f.path for f in client.list_artifacts(run_id, "model")]
    return data.params, data.metrics, tags, artifacts

def train_and_validate_reg(
    X_train: np.array, X_test: np.array, 
    y_train: np.array, 
    y_test: np.array):
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME"))
    # enable autologging
    mlflow.sklearn.autolog()
    with mlflow.start_run(run_name="RANDOM_FOREST_REGRESSOR") as run:
        forest_reg = RandomForestRegressor()
        mlflow.log_param("max_features", forest_reg.get_params()["max_features"])
        forest_reg.fit(X_train, y_train)

        # Evaluate on Train Set
        y_train_pred = forest_reg.predict(X_train)
        (train_rmse, train_mae, train_r2) = eval_metrics(y_train, y_train_pred)
        print("---------------------------------------------------------")
        print("  RMSE on Train Set: %s" % train_rmse)
        print("  MAE on Train Set: %s" % train_mae)
        print("  R2 on Train Set: %s" % train_r2)

        # Evaluate on cross validation
        (cv_rmse, cv_mae, cv_r2) = eval_cross_validation(forest_reg, X_train, y_train, k=5)

        print("---------------------------------------------------------")
        print("  RMSE on Cross Validation: %s" % cv_rmse.mean())
        print("  MAE on Cross Validation: %s" % cv_mae.mean())
        print("  R2 on Cross Validation: %s" % cv_r2.mean())

        # # Evaluate on Test set
        y_test_pred = forest_reg.predict(X_test)
        (test_rmse, test_mae, test_r2) = eval_metrics(y_test, y_test_pred)
        print("---------------------------------------------------------")
        print("  RMSE on Test Set: %s" % test_rmse)
        print("  MAE on Test Set: %s" % test_mae)
        print("  R2 on Test Set: %s" % test_r2)

        mlflow.sklearn.log_model(
            sk_model=forest_reg,
            artifact_path="random-forest-model",
            registered_model_name="sk-learn-random-forest-reg-model",
        )
    # fetch logged data
    params, metrics, tags, artifacts = fetch_logged_data(run.info.run_id)
    return params, metrics, tags, artifacts