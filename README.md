# Project Background
The goal of this project was to evaluate the use of generative AI in mapping the SAP PM data model to MIMOSA CCOM data model. With the motivation to increase interoperability between the data models and allow easier transfer of data between them.

# System Design
The system has two distinct functions.
1. To interact with generative AI to produce and improve mappings (a mapping is a pair of fields one from SAP PM one from MIMOSA CCOM that are comparable). 
2. To validate the output of this mapping to determine how likely it is to be correct.

The system was designed to be interacted with through a web interface, with functionality to store historical maps, generate new mappings based on text prompts and to find equivalent field when provided with either SAP PM or MIMOSA CCOM field.

# Initial Setup


# Codebase Structure
