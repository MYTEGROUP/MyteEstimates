import json

project_description_template = {
    "Introduction": {
        "Purpose": {"description": "Describe the purpose of the document and the software product.", "response": ""},
        "Scope": {"description": "Define the scope of the software, including its intended use and objectives.", "response": ""}
    },
    "Overall Description": {
        "Product Perspective": {"description": "Explain how the product fits into the broader system or business context.", "response": ""},
        "Product Functions": {"description": "Outline the main functions the software will perform.", "response": ""},
        "User Classes and Characteristics": {"description": "Describe the different types of users who will interact with the software and their characteristics.", "response": ""},
        "Operating Environment": {"description": "Specify the operating environment for the software, including hardware and software platforms.", "response": ""},
        "Design and Implementation Constraints": {"description": "List any constraints that might affect the design or implementation of the software, such as regulatory requirements or hardware limitations.", "response": ""},
        "User Documentation": {"description": "Detail the user documentation to be provided, such as user manuals, installation guides, and help files.", "response": ""}
    },
    "System Features and Requirements": {
        "Feature Description": {"description": "A brief description of the feature.", "response": ""},
        "Functional Requirements": {"description": "Detailed descriptions of the functionality that the feature must provide, including data input and output, calculations, or any other processing requirements.", "response": ""},
        "Performance Requirements": {"description": "Specify performance constraints, such as response time, throughput, or data capacity requirements.", "response": ""},
        "Security Requirements": {"description": "Outline the security requirements, including authentication, authorization, data encryption, and compliance with security standards.", "response": ""},
        "Software Quality Attributes": {"description": "Define the desired quality attributes for the software, such as reliability, maintainability, scalability, and usability.", "response": ""}
    },
    "External Interface Requirements": {
        "User Interfaces": {"description": "Describe the user interface of the software, including screen layouts, menus, dialogs, and user interaction flows.", "response": ""},
        "Hardware Interfaces": {"description": "Specify the hardware devices that the software will interface with and the nature of those interactions.", "response": ""},
        "Software Interfaces": {"description": "Detail the interactions with other software applications or systems, including APIs, data formats, and protocols.", "response": ""},
        "Communications Interfaces": {"description": "Describe any communication interfaces, such as network protocols, messaging systems, or email integration.", "response": ""}
    },
    "Non-functional Requirements": {
        "Performance Requirements": {"description": "Mention any specific performance metrics the software should meet.", "response": ""},
        "Safety Requirements": {"description": "Describe any safety requirements that need to be considered to prevent harm to users or damage to hardware.", "response": ""},
        "Security Requirements": {"description": "Detail security and privacy requirements, including data protection, user authentication, and audit trails.", "response": ""},
        "Software Quality Attributes": {"description": "Discuss quality attributes such as reliability, scalability, maintainability, and usability.", "response": ""}
    },
    "Data Models/Data Dictionary": {
        "Data Models": {"description": "Provide a conceptual data model that outlines the key data entities and their relationships.", "response": ""},
        "Data Dictionary": {"description": "A detailed description of all data elements, including name, description, type, format, and any constraints or relationships.", "response": ""}
    }
}

# Writing the project description template to a JSON file
with open('storage/project_description_template.json', 'w') as file:
    json.dump(project_description_template, file, indent=4)

print("Project description template saved as 'project_description_template.json'.")
