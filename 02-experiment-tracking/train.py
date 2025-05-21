import os
import pickle
import click
import mlflow

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Set up MLflow experiment and tracking URI
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("random-forest-train")


def load_pickle(filename: str):
    """Load data from a pickle file."""
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


@click.command()
@click.option(
    "--data_path",
    default="/Users/rajuparipelly/Documents/MLOPS/mlops-zoomcamp/02-experiment-tracking/output",
    help="Location where the processed NYC taxi trip data was saved"
)
def run_train(data_path: str):
    """Train a Random Forest Regressor and log parameters, metrics, and model with MLflow."""
    # Enable MLflow autologging for scikit-learn
    mlflow.sklearn.autolog()

    # Load training and validation data
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    with mlflow.start_run():  # Start an MLflow run

        # Initialize and fit the Random Forest model
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)

        # Predict on the validation set
        y_pred = rf.predict(X_val)

        # Calculate RMSE
        rmse = mean_squared_error(y_val, y_pred, squared=False)
        
        # Log the RMSE metric
        mlflow.log_metric("rmse", rmse)

        # Optionally, you can log a summary message
        print(f"Logged RMSE: {rmse}")


if __name__ == '__main__':
    run_train()