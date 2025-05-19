# Project Background
The goal of this project was to evaluate the use of generative AI in mapping the SAP PM data model to MIMOSA CCOM data model. With the motivation to increase interoperability between the data models and allow easier transfer of data between them.

# System Design
The system has two distinct functions.
1. To interact with generative AI to produce and improve mappings (a mapping is a pair of fields one from SAP PM one from MIMOSA CCOM that are comparable). 
2. To validate the output of this mapping to determine how likely it is to be correct.

The system was designed to be interacted with through a web interface, with functionality to store historical maps, generate new mappings based on text prompts and to find equivalent field when provided with either SAP PM or MIMOSA CCOM field.

# Initial Setup
Install required components by running `pip install`
Navigate to the SAP-MIMOSA directory and run the main.py file using the command `python3 main.py`
Create a new file called `.env` in the WebApp directory
Add open AI envrionment variable by running 

# Codebase Structure
The system has 3 main folders:

- **Data**: This folder is not used by the production application. It contains code used to collect the SAP schema and stores copies of schema and test files.

- **ValidationAndMapping**: Contains all of the code to validate mappings.
  - **ScoreManager**: This module takes a mapping object and returns a score based on various criteria.
  - **Models**: Contains the data models used to transfer data around the system, including definitions for mappings and their attributes.
  - **Accuracy**: This module checks a single field-to-field mapping against a series of criteria to determine its accuracy.
    - **DataType**: Checks if the data types of the different fields are comparable by normalizing and comparing their types.
    - **DescriptionSimilarity**: Calculates the similarity between the descriptions of the SAP and MIMOSA fields using a pre-trained model to generate embeddings and compute cosine similarity.
    - **FieldLength**: Compares the lengths of the fields in the SAP and MIMOSA models to assess their comparability.
    - **InfoOmitted**: Evaluates whether any important information is missing from the mapping entries.
    - **SAPChecker**: Validates the SAP fields against a predefined schema to ensure they conform to expected standards.
    - **MimosaChecker**: Validates the MIMOSA fields against a predefined schema to ensure they conform to expected standards.

- **WebApp**: This folder contains the web application code.
  - **app.py**: The main FastAPI application file that initializes the server, defines endpoints, and handles requests.
  - **ai_models.py**: Contains the `OpenAIModel` class, which interacts with the OpenAI API to generate and improve mappings based on user queries.
  - **Controllers**: Contains controller classes that handle specific functionalities, such as saving and loading mapping documents.
  - **Models**: Contains data models specific to the web application, including the `MappingDocument` class that represents the structure of mapping data exchanged with the frontend.