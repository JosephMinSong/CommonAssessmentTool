"""
Client service module handling all database operations for clients.
Provides CRUD operations and business logic for client management.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from app.models import Client, ClientCase, User
from app.clients.schema import ClientUpdate, ServiceUpdate, ServiceResponse

class ClientService:
    @staticmethod
    def get_client(db: Session, client_id: int):
        """Get a specific client by ID"""
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        return client

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 50):
        """
        Get clients with optional pagination.
        Default shows first 50 clients, which means you'd need 3 pages for 150 records.
        """
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value cannot be negative"
            )
        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be greater than 0"
            )
        
        clients = db.query(Client).offset(skip).limit(limit).all()
        total = db.query(Client).count()
        return {"clients": clients, "total": total}

    @staticmethod
    def __update_query_by_filter(query, elements):
        for element, value in elements:
            if value is not None and element != "age":
                query = query.filter(getattr(Client, element) == value)
            elif value is not None and element is "age":
                query = query.filter(getattr(Client, "age") >= value)
        return query

    @staticmethod
    def __education_level_validation(education_level):
        if education_level is not None and not (1 <= education_level <= 14):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Education level must be between 1 and 14"
            )

    @staticmethod
    def __age_validation(age_min):
        if age_min is not None and age_min < 18:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Minimum age must be at least 18"
            )

    @staticmethod
    def __gender_validation(gender):
        if gender is not None and gender not in [1, 2]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Gender must be 1 or 2"
            )

    @staticmethod
    def get_clients_by_criteria(
            db: Session,
            employment_status: Optional[bool] = None,
            education_level: Optional[int] = None,
            age_min: Optional[int] = None,
            gender: Optional[int] = None,
            work_experience: Optional[int] = None,
            canada_workex: Optional[int] = None,
            dep_num: Optional[int] = None,
            canada_born: Optional[bool] = None,
            citizen_status: Optional[bool] = None,
            fluent_english: Optional[bool] = None,
            reading_english_scale: Optional[int] = None,
            speaking_english_scale: Optional[int] = None,
            writing_english_scale: Optional[int] = None,
            numeracy_scale: Optional[int] = None,
            computer_scale: Optional[int] = None,
            transportation_bool: Optional[bool] = None,
            caregiver_bool: Optional[bool] = None,
            housing: Optional[int] = None,
            income_source: Optional[int] = None,
            felony_bool: Optional[bool] = None,
            attending_school: Optional[bool] = None,
            substance_use: Optional[bool] = None,
            time_unemployed: Optional[int] = None,
            need_mental_health_support_bool: Optional[bool] = None
    ):
        """Get clients filtered by any combination of criteria"""
        query = db.query(Client)

        ClientService.__education_level_validation(education_level)
        ClientService.__age_validation(age_min)
        ClientService.__gender_validation(gender)

        elements = {
            "currently_employed": employment_status,
            "age": age_min,
            "gender": gender,
            "level_of_schooling": education_level,
            "work_experience": work_experience,
            "canada_workex": canada_workex,
            "dep_num": dep_num,
            "canada_born": canada_born,
            "citizen_status": citizen_status,
            "fluent_english": fluent_english,
            "reading_english_scale": reading_english_scale,
            "speaking_english_scale": speaking_english_scale,
            "writing_english_scale": writing_english_scale,
            "numeracy_scale": numeracy_scale,
            "computer_scale": computer_scale,
            "transportation_bool": transportation_bool,
            "caregiver_bool": caregiver_bool,
            "housing": housing,
            "income_source": income_source,
            "felony_bool": felony_bool,
            "attending_school": attending_school,
            "substance_use": substance_use,
            "time_unemployed": time_unemployed,
            "need_mental_health_support_bool": need_mental_health_support_bool,
        }

        query = ClientService.__update_query_by_filter(query, elements)
        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}"
            )

    @staticmethod
    def get_clients_by_services(
        db: Session,
        **service_filters: Optional[bool]
    ):
        """
        Get clients filtered by multiple service statuses.
        """
        query = db.query(Client).join(ClientCase)
    
        for service_name, status in service_filters.items():
            if status is not None:
                filter_criteria = getattr(ClientCase, service_name) == status
                query = query.filter(filter_criteria)
    
        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}"
            )

    @staticmethod
    def get_client_services(db: Session, client_id: int):
        """Get all services for a specific client with case worker info"""
        client_cases = db.query(ClientCase).filter(ClientCase.client_id == client_id).all()
        if not client_cases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}"
            )
        return client_cases

    @staticmethod
    def get_clients_by_success_rate(db: Session, min_rate: int = 70):
        """Get clients with success rate at or above the specified percentage"""
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100"
            )
            
        return db.query(Client).join(ClientCase).filter(
            ClientCase.success_rate >= min_rate
        ).all()

    @staticmethod
    def get_clients_by_case_worker(db: Session, case_worker_id: int):
        """Get all clients assigned to a specific case worker"""
        case_worker = db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found"
            )
            
        return db.query(Client).join(ClientCase).filter(
            ClientCase.user_id == case_worker_id
        ).all()

    @staticmethod
    def update_client(db: Session, client_id: int, client_update: ClientUpdate):
        """Update a client's information"""
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        update_data = client_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client, field, value)

        try:
            db.commit()
            db.refresh(client)
            return client
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}"
            )
    
    @staticmethod
    def update_client_services(
        db: Session, 
        client_id: int,
        user_id: int,
        service_update: ServiceUpdate
    ):
        """Update a client's services and outcomes for a specific case worker"""
        client_case = db.query(ClientCase).filter(
            ClientCase.client_id == client_id,
            ClientCase.user_id == user_id
        ).first()
    
        if not client_case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No case found for client {client_id} with case worker {user_id}. "
                    f"Cannot update services for a non-existent case assignment."
            )

        update_data = service_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(client_case, field, value)

        try:
            db.commit()
            db.refresh(client_case)
            return client_case
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}"
            )
    
    @staticmethod
    def create_case_assignment(
        db: Session, 
        client_id: int,
        case_worker_id: int
    ):
        """Create a new case assignment"""
        # Check if client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        # Check if case worker exists
        case_worker = db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found"
            )

        # Check if assignment already exists
        existing_case = db.query(ClientCase).filter(
            ClientCase.client_id == client_id,
            ClientCase.user_id == case_worker_id
        ).first()
    
        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to case worker {case_worker_id}"
        )

        try:
            # Create new case assignment with default service values
            new_case = ClientCase(
                client_id=client_id,
                user_id=case_worker_id,
                employment_assistance=False,
                life_stabilization=False,
                retention_services=False,
                specialized_services=False,
                employment_related_financial_supports=False,
                employer_financial_supports=False,
                enhanced_referrals=False,
                success_rate=0
            )
            db.add(new_case)
            db.commit()
            db.refresh(new_case)
            return new_case

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}"
            )
    
    @staticmethod
    def delete_client(db: Session, client_id: int):
        """Delete a client and their associated records"""
        # First check if client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )

        try:
            # Delete associated client_cases
            db.query(ClientCase).filter(
                ClientCase.client_id == client_id
            ).delete()
        
            # Delete the client
            db.delete(client)
            db.commit()
        
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}"
            )
