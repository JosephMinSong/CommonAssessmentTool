# Team ShipHappens

## Project Requirements
1. Refactor code, configure linting
2. Feature Development Backend: ML Model Options
3. Implement Docker and Docker-Compose
4. CI/CD pipeline improvements
5. Deploy on AWS


### User Story

As a user of the backend API's, I want to call API's that can utilize and switch ML models with the CaseManagment service so that I more efficiently help previous clients by generating predictions of client success.

### Deliverables

Three machine learning models were trained and implemented. This project provides API's that allow the user to switch the model, generate client success predictions using the desired model, display the model currently used, and display all available models.

Improvements were added to update the CI/CD pipeline, running automatic tests and linting with Github Actions prior to merging and deployment.

Finally, this project is deployed via AWS to provide a publicly available endpoint for ease of access.

## Access Application Publicly
The backend application and endpoints can be accessed at the following link:

http://ec2-3-143-205-215.us-east-2.compute.amazonaws.com:8000/docs

The CD pipeline was also updated to allow new changes to be  automatically tested and deployed to update the public endpoint.

## Running Application Locally
### How to Use (Docker):

1. With Docker running, build the Docker image making sure to replace image_name with the desired name for your Docker image
```
docker build -t image_name .
```

2. Run the Docker image, making sure to replace image_name
```
docker run --env-file .env -p 8000:8000 image_name
```

### How to Use (Docker-Compose)

1. Update the container_name field in the docker-compose.yml file with desired container name. With Docker running build the docker-compose image

```
docker-compose build
```

2. Start the container
```
docker-compose up
```

Optional: To delete the container after use
```
docker-compose down
```

### Next Steps (Running App)

3. Go to SwaggerUI (http://0.0.0.0:8000/docs)

4. Log in as admin (username: admin password: admin123)

5. Click on each endpoint to use:

## Endpoints:

#### Clients and Auth (Existing)

- Create User (Only users in admin role can create new users. The role field needs to be either "admin" or "case_worker")

- Get clients (Display all the clients that are in the database)

- Get client (Allow authorized users to search for a client by id. If the id is not in database, an error message will show.)

- Update client (Allow authorized users to update a client's basic info by inputting in client_id and providing updated values.)

- Delete client (Allow authorized users to delete a client by id. If an id is no longer in the database, an error message will show.)

- Get clients by criteria (Allow authorized users to get a list of clients who meet a certain combination of criteria.)

- Get Clients by services (Allow authorized users to get a list of clients who meet a certain combination of service statuses.)

- Get clients services (Allow authorized users to view a client's services' status.)

- Get clients by success rate (Allow authorized users to search for clients whose cases have a success rate beyond a certain number.)

- Get clients by case worker (Allow users to view which clients are assigned to a specific case worker.)

- Update client services (Allow users to update the service status of a case.)

- Create case assignment (Allow authorized users to create a new case assignment.)

#### Model (Newly Added)

- Get current model (Allows user to see what the current ML model being used is.)

- List all models (Allows user to see all available ML models)

- Change model (Allows user to change the model used for predictions, currently supported for "forest regression", "ada boost regression", and "extra trees regression")

- Predictions (allows user to generate predictions based on input using the ML model chosen)
