"""
Logic module for processing client data and making intervention predictions.
Handles data cleaning, model predictions, and intervention combinations analysis.
"""

# Standard library imports
import os
import json
from itertools import product
from app.utils import TextConverter

# Third-party imports
import pickle
import numpy as np

from app.clients.service.model_path import ModelPath

# Constants
COLUMN_INTERVENTIONS = [
    "Life Stabilization",
    "General Employment Assistance Services",
    "Retention Services",
    "Specialized Services",
    "Employment-Related Financial Supports for Job Seekers and Employers",
    "Employer Financial Supports",
    "Enhanced Referrals for Skills Development",
]
CURRENT_MODEL = "forest regression"

# Load model
# CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(CURRENT_DIR, FOREST_REGRSSION)
# with open(MODEL_PATH, "rb") as model_file:
#     MODEL = pickle.load(model_file)


def load_model(model):
    """
    Load the machine learning model from the specified path.
    """
    global CURRENT_MODEL
    model_name = model.lower()
    model_type = ""
    if model_name == "forest regression":
        model_type = ModelPath.FOREST_REGRSSION
    elif model_name == "extra trees regression":
        model_type = ModelPath.EXTRA_TREES_REGRESSOR
    elif model_name == "ada boost regression":
        model_type = ModelPath.ADA_BOOST_REGRESSOR

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(CURRENT_DIR, model_type.value)
    CURRENT_MODEL = model_name

    try:
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)
        return model
    except FileNotFoundError:
        raise RuntimeError(f"Model file not found at {MODEL_PATH}.")
    except Exception:
        raise Exception("The model was not able to be loaded.")


def get_current_model():
    """
    Method to get the current model in use
    """
    return CURRENT_MODEL


def list_all_models():
    """
    Method to list all models that our application has available
    """
    return json.dumps([{"model name": model.name} for model in ModelPath])


def clean_input_data(input_data):
    """
    Clean and transform input data into model-compatible format.

    Args:
        input_data (dict): Raw input data from the client

    Returns:
        list: Cleaned and formatted data ready for model input
    """
    columns = [
        "age",
        "gender",
        "work_experience",
        "canada_workex",
        "dep_num",
        "canada_born",
        "citizen_status",
        "level_of_schooling",
        "fluent_english",
        "reading_english_scale",
        "speaking_english_scale",
        "writing_english_scale",
        "numeracy_scale",
        "computer_scale",
        "transportation_bool",
        "caregiver_bool",
        "housing",
        "income_source",
        "felony_bool",
        "attending_school",
        "currently_employed",
        "substance_use",
        "time_unemployed",
        "need_mental_health_support_bool",
    ]
    demographics = {key: input_data[key] for key in columns}
    output = []
    for column in columns:
        value = demographics.get(column, None)
        if isinstance(value, str):
            value = TextConverter.convert_text(
                value
            )  # Removed 'column' from here as it wasn't used
        output.append(value)
    return output


def create_matrix(row_data):
    """
    Create matrix of all possible intervention combinations.

    Args:
        row_data (list): Base data row

    Returns:
        np.array: Matrix of all possible intervention combinations
    """
    data = [row_data.copy() for _ in range(128)]
    perms = intervention_permutations(7)
    return np.concatenate((np.array(data), np.array(perms)), axis=1)


def intervention_permutations(num):
    """
    Generate all possible intervention combinations.

    Args:
        num (int): Number of interventions

    Returns:
        np.array: Matrix of all possible combinations
    """
    return np.array(list(product([0, 1], repeat=num)))


def get_baseline_row(row_data):
    """
    Create baseline row with no interventions.

    Args:
        row_data (list): Input data row

    Returns:
        np.array: Baseline row with zeros for interventions
    """
    base_interventions = np.zeros(7)
    return np.concatenate((np.array(row_data), base_interventions))


def intervention_row_to_names(row_data):
    """
    Convert intervention row to list of intervention names.

    Args:
        row_data (np.array): Row of intervention indicators

    Returns:
        list: Names of active interventions
    """
    return [COLUMN_INTERVENTIONS[i] for i, value in enumerate(row_data) if value == 1]


def process_results(baseline_pred, results_matrix):
    """
    Process model results into structured output.

    Args:
        baseline_pred (float): Baseline prediction
        results_matrix (np.array): Matrix of results

    Returns:
        dict: Processed results with baseline and interventions
    """
    result_list = [
        (row[-1], intervention_row_to_names(row[:-1])) for row in results_matrix
    ]
    return {"baseline": baseline_pred[-1], "interventions": result_list}


def interpret_and_calculate(input_data):
    """
    Main function to process input data and generate intervention recommendations.

    Args:
        input_data (dict): Raw input data from client

    Returns:
        dict: Processed results with recommendations
    """
    global CURRENT_MODEL
    raw_data = clean_input_data(input_data)
    baseline_row = get_baseline_row(raw_data).reshape(1, -1)
    intervention_rows = create_matrix(raw_data)
    model = load_model(CURRENT_MODEL)
    print("Currently using model: ", end="")
    print(CURRENT_MODEL)
    baseline_prediction = model.predict(baseline_row)
    intervention_predictions = model.predict(intervention_rows).reshape(-1, 1)
    result_matrix = np.concatenate(
        (intervention_rows, intervention_predictions), axis=1
    )
    result_order = result_matrix[:, -1].argsort()
    result_matrix = result_matrix[result_order]
    top_results = result_matrix[-3:, -8:]
    return process_results(baseline_prediction, top_results)


if __name__ == "__main__":
    test_data = {
        "age": "23",
        "gender": "1",
        "work_experience": "1",
        "canada_workex": "1",
        "dep_num": "0",
        "canada_born": "1",
        "citizen_status": "2",
        "level_of_schooling": "2",
        "fluent_english": "3",
        "reading_english_scale": "2",
        "speaking_english_scale": "2",
        "writing_english_scale": "3",
        "numeracy_scale": "2",
        "computer_scale": "3",
        "transportation_bool": "2",
        "caregiver_bool": "1",
        "housing": "1",
        "income_source": "5",
        "felony_bool": "1",
        "attending_school": "0",
        "currently_employed": "1",
        "substance_use": "1",
        "time_unemployed": "1",
        "need_mental_health_support_bool": "1",
    }
    results = interpret_and_calculate(test_data)
    print(results)

# test
