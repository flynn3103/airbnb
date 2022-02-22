import pickle

from dagster import Output, OutputDefinition, pipeline, solid

from src.utils.config import BASE_DIR, INPUT_DATASET_LOC
from src.data_processing import dataloaders, standarization, transform
from src.ml_workflow import model, train_test




@solid(
    output_defs=[
        OutputDefinition(name="dataset", is_required=True)
    ]
)
def get_dataset(context):
    dataset = dataloaders.get_dataset(INPUT_DATASET_LOC)
    context.log.info(f"Loaded data; N={len(dataset)}")
    yield Output(dataset, "dataset")


@solid(
    output_defs=[
        OutputDefinition(name="transformed_data", is_required=True)
    ]
)

def get_transform(context, data):
    transformed_data = transform.get_transform(data)
    context.log.info(f"Transformed data done; N={len(transformed_data)}")
    yield Output(transformed_data, "transformed_data")


@solid(
    output_defs=[
        OutputDefinition(name="X", is_required=True),
        OutputDefinition(name="y", is_required=True)
    ]
)
def get_standarization(context, transformed_data):
    X, y = standarization.get_standarization(transformed_data)
    context.log.info(f"Standarized data done; X={X.shape}, y={y.shape}")
    yield Output(X, "X")
    yield Output(y, "y")

@solid(
    output_defs=[
        OutputDefinition(name="X_train", is_required=True),
        OutputDefinition(name="X_test", is_required=True),
        OutputDefinition(name="y_train", is_required=True),
        OutputDefinition(name="y_test", is_required=True),
    ]
)
def train_test_split(context, X, y):
    X_train, X_test, y_train, y_test = train_test.get_train_test_split(X, y)
    context.log.info(
        f"Train test split done; X_train={X_train.shape}, X_test={X_test.shape}, "
        f"y_train={y_train.shape}, y_test={y_test.shape}"
    )
    yield Output(X_train, "X_train")
    yield Output(X_test, "X_test")
    yield Output(y_train, "y_train")
    yield Output(y_test, "y_test")

@solid(
    output_defs=[
        OutputDefinition(name="params", is_required=True),
        OutputDefinition(name="metrics", is_required=True),
        OutputDefinition(name="tags", is_required=True),
        OutputDefinition(name="artifacts", is_required=True),
    ]
)
def train_regression_model(context, X_train, X_test, y_train, y_test) -> None:
    params, metrics, tags, artifacts = model.train_and_validate_reg(X_train, X_test, y_train, y_test)
    context.log.info(f"Parameters: {params}")
    context.log.info(f"Metrics: {metrics}")
    context.log.info(f"Tags name: {tags}")
    context.log.info(f"Artifacts: {artifacts}")

    yield Output(params, "params")
    yield Output(metrics, "metrics")
    yield Output(tags, "tags")
    yield Output(artifacts, "artifacts")

@pipeline
def ml_pipeline():
    # 1. fetch training data
    data = get_dataset()
    # 2. make data distrubution more Gaussian
    transformed_data = get_transform(data)
    # 3. standarized data
    X, y = get_standarization(transformed_data)
    # 4. train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    # 5. model training, validation, registry, artifact storage
    train_regression_model(X_train, X_test, y_train, y_test)
