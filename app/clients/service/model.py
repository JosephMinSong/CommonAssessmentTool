"""
Model training module for the Common Assessment Tool.
Handles the preparation, training, and saving of the prediction model.
"""

# Standard library imports
import pickle
import os

# Third-party imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import AdaBoostRegressor
from app.clients.service.model_path import ModelPath
import logging

logging.basicConfig(level=logging.INFO)


def prepare_models():
    logging.info("DOCKER LOG: Preparing models")
    """
    Prepare and train the Random Forest model using the dataset.
    
    Returns:
        RandomForestRegressor: Trained model for predicting success rates
    """
    # Load dataset
    data = pd.read_csv("app/clients/service/data_commontool.csv")
    # Define feature columns
    feature_columns = [
        "age",  # Client's age
        "gender",  # Client's gender (bool)
        "work_experience",  # Years of work experience
        "canada_workex",  # Years of work experience in Canada
        "dep_num",  # Number of dependents
        "canada_born",  # Born in Canada
        "citizen_status",  # Citizenship status
        "level_of_schooling",  # Highest level achieved (1-14)
        "fluent_english",  # English fluency scale (1-10)
        "reading_english_scale",  # Reading ability scale (1-10)
        "speaking_english_scale",  # Speaking ability scale (1-10)
        "writing_english_scale",  # Writing ability scale (1-10)
        "numeracy_scale",  # Numeracy ability scale (1-10)
        "computer_scale",  # Computer proficiency scale (1-10)
        "transportation_bool",  # Needs transportation support (bool)
        "caregiver_bool",  # Is primary caregiver (bool)
        "housing",  # Housing situation (1-10)
        "income_source",  # Source of income (1-10)
        "felony_bool",  # Has a felony (bool)
        "attending_school",  # Currently a student (bool)
        "currently_employed",  # Currently employed (bool)
        "substance_use",  # Substance use disorder (bool)
        "time_unemployed",  # Years unemployed
        "need_mental_health_support_bool",  # Needs mental health support (bool)
    ]
    # Define intervention columns
    intervention_columns = [
        "employment_assistance",
        "life_stabilization",
        "retention_services",
        "specialized_services",
        "employment_related_financial_supports",
        "employer_financial_supports",
        "enhanced_referrals",
    ]
    # Combine all feature columns
    all_features = feature_columns + intervention_columns
    # Prepare training data
    features = np.array(data[all_features])  # Changed from X to features
    targets = np.array(data["success_rate"])  # Changed from y to targets
    # Split the dataset
    features_train, _, targets_train, _ = train_test_split(  # Removed unused variables
        features, targets, test_size=0.2, random_state=42
    )
    # Initialize and train the model
    forest_model = RandomForestRegressor(n_estimators=100, random_state=42)
    forest_model.fit(features_train, targets_train)

    extra_trees_model = ExtraTreesRegressor(n_estimators=100, random_state=42)
    extra_trees_model.fit(features_train, targets_train)

    ada_boost_model = AdaBoostRegressor(n_estimators=100, random_state=42)
    ada_boost_model.fit(features_train, targets_train)

    # Directory path
    directory = os.path.dirname(os.path.abspath(__file__))

    save_model(forest_model, os.path.join(directory, ModelPath.FOREST_REGRSSION.value))
    save_model(
        extra_trees_model,
        os.path.join(directory, ModelPath.EXTRA_TREES_REGRESSOR.value),
    )
    save_model(
        ada_boost_model, os.path.join(directory, ModelPath.ADA_BOOST_REGRESSOR.value)
    )
    logging.info("DOCKER LOG: Successfully created all models")


def save_model(model, filename):
    """
    Save the trained model to a file.

    Args:
        model: Trained model to save
        filename (str): Name of the file to save the model to
    """
    with open(filename, "wb") as model_file:
        pickle.dump(model, model_file)


def load_model(filename):
    """
    Load a trained model from a file.

    Args:
        filename (str): Name of the file to load the model from

    Returns:
        The loaded model
    """
    with open(filename, "rb") as model_file:
        return pickle.load(model_file)


def main():
    """Main function to train and save the model."""
    print("Starting model training...")
    prepare_models()
    print("Model training completed and saved successfully.")


if __name__ == "__main__":
    main()
