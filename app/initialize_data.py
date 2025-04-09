import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Client, User, ClientCase, UserRole
from app.auth.router import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()


def initialize_database():
    print("Starting database initialization...")
    logging.info("DOCKER LOG: Starting database initialization...")
    db = SessionLocal()
    try:
        # Retrieve admin credentials from environment variables
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")
        # Retrieve case worker credentials from environment variables
        case_worker_username = os.getenv("CASE_WORKER_USERNAME")
        case_worker_email = os.getenv("CASE_WORKER_EMAIL")
        case_worker_password = os.getenv("CASE_WORKER_PASSWORD")

        # Create admin user if doesn't exist
        admin = db.query(User).filter(User.username == admin_username).first()
        if not admin:
            admin = User(
                username=admin_username,
                email=admin_email,
                hashed_password=get_password_hash(admin_password),
                role=UserRole.admin,
            )
            db.add(admin)
            db.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")

        # Create case worker if doesn't exist
        case_worker = (
            db.query(User).filter(User.username == case_worker_username).first()
        )
        if not case_worker:
            case_worker = User(
                username=case_worker_username,
                email=case_worker_email,
                hashed_password=get_password_hash(case_worker_password),
                role=UserRole.case_worker,
            )
            db.add(case_worker)
            db.commit()
            print("Case worker created successfully")
        else:
            print("Case worker already exists")

        # Load CSV data
        print("Loading CSV data...")
        df = pd.read_csv("app/clients/service/data_commontool.csv")

        # Convert data types
        integer_columns = [
            "age",
            "gender",
            "work_experience",
            "canada_workex",
            "dep_num",
            "level_of_schooling",
            "reading_english_scale",
            "speaking_english_scale",
            "writing_english_scale",
            "numeracy_scale",
            "computer_scale",
            "housing",
            "income_source",
            "time_unemployed",
            "success_rate",
        ]
        for col in integer_columns:
            df[col] = pd.to_numeric(df[col], errors="raise")

        # Process each row in CSV
        for index, row in df.iterrows():
            # Create client
            client = Client(
                age=int(row["age"]),
                gender=int(row["gender"]),
                work_experience=int(row["work_experience"]),
                canada_workex=int(row["canada_workex"]),
                dep_num=int(row["dep_num"]),
                canada_born=bool(row["canada_born"]),
                citizen_status=bool(row["citizen_status"]),
                level_of_schooling=int(row["level_of_schooling"]),
                fluent_english=bool(row["fluent_english"]),
                reading_english_scale=int(row["reading_english_scale"]),
                speaking_english_scale=int(row["speaking_english_scale"]),
                writing_english_scale=int(row["writing_english_scale"]),
                numeracy_scale=int(row["numeracy_scale"]),
                computer_scale=int(row["computer_scale"]),
                transportation_bool=bool(row["transportation_bool"]),
                caregiver_bool=bool(row["caregiver_bool"]),
                housing=int(row["housing"]),
                income_source=int(row["income_source"]),
                felony_bool=bool(row["felony_bool"]),
                attending_school=bool(row["attending_school"]),
                currently_employed=bool(row["currently_employed"]),
                substance_use=bool(row["substance_use"]),
                time_unemployed=int(row["time_unemployed"]),
                need_mental_health_support_bool=bool(
                    row["need_mental_health_support_bool"]
                ),
            )
            db.add(client)
            db.commit()

            # Create client_case
            client_case = ClientCase(
                client_id=client.id,
                user_id=admin.id,  # Assign to admin
                employment_assistance=bool(row["employment_assistance"]),
                life_stabilization=bool(row["life_stabilization"]),
                retention_services=bool(row["retention_services"]),
                specialized_services=bool(row["specialized_services"]),
                employment_related_financial_supports=bool(
                    row["employment_related_financial_supports"]
                ),
                employer_financial_supports=bool(row["employer_financial_supports"]),
                enhanced_referrals=bool(row["enhanced_referrals"]),
                success_rate=int(row["success_rate"]),
            )
            db.add(client_case)
            db.commit()

        print("Database initialization completed successfully!")
        logging.info("DOCKER LOG: Database initialization completed successfully!")

    except Exception as e:
        print(f"Error during initialization: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()
