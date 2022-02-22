import os

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor 

from src.utils.config import set_env_vars
from sqlalchemy import null

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


def train_and_validate_reg(
    X_train: np.array, X_test: np.array, 
    y_train: np.array, 
    y_test: np.array):
    mlflow.set_experiment(os.getenv("MLFLOW_EXPERIMENT_NAME"))
    with mlflow.start_run(run_name="RANDOM_FOREST_REGRESSOR"):
        forest_reg = RandomForestRegressor()
        mlflow.log_param("max_features", forest_reg.get_params()["max_features"])
        forest_reg.fit(X_train, y_train)
        
        # Evaluate on cross validation
        r2_cv_scores = (cross_val_score(forest_reg, X_train, y_train, cv=5, scoring='r2'))
        print("---------------------------------------------------------")
        print("  R2 on Cross Validation: %s" % r2_cv_scores.mean())

        mlflow.log_metric("r2_cv", r2_cv_scores.mean())

        # Evaluate on Test set
        y_test_pred = forest_reg.predict(X_test)
        (test_rmse, test_mae, test_r2) = eval_metrics(y_test, y_test_pred)
        print("---------------------------------------------------------")
        print("  RMSE on Test Set: %s" % test_rmse)
        print("  MAE on Test Set: %s" % test_mae)
        print("  R2 on Test Set: %s" % test_r2)

        
        mlflow.log_metric("rmse_test", test_rmse)
        mlflow.log_metric("r2_test", test_r2)
        mlflow.log_metric("mae_test", test_mae)

        mlflow.sklearn.log_model(
            sk_model=forest_reg,
            artifact_path="random-forest-model",
            registered_model_name="sk-learn-random-forest-reg-model",
        )