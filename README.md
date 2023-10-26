# Responsabilities per Layer

The user_id must be provided and validate in ApiGateway.

## Presentation

Deliver data

### Controller

1. Initialize the Dependency Injection
    1. Create repository
    2. Create producer broker
    3. Create use case
2. Call the method passing the Data Transfer Object from Interface
3. Response deliver a dictionary

### Interface

1. Apply some validation rules
2. User domain classmethods to validate some aspects
3. Return Data Transfer Object (namedTuple)

### Route

1. From params send in request as dictionary create struct
2. Create controller 
3. Send Struct to controller
4. Recive response and encapsulate in response

## Application

Convert data into information

1. Use state machine to deliver the struct to the specific case
2. Convert and validate Data Transfer Object to Struct
3. Use Repository to for validation
4. Persist information into repository
5. return dictionary with information that method provided

## Infrastructure

Deliver the framework

1. Provide the configuration
2. Create the Comunication with external modules

# Annotations
pip show flake8 
export PATH=$PATH:/home/pat/.local/lib/python3.10/site-packages
source ~/.profile