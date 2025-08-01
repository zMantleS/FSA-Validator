import os
import sys
from lxml import etree

schemaFileName = "FSA029-Schema.xsd"

def extraPrompt(message):
    prompt = str(input(message))
    if prompt.upper() == "Q":
        sys.exit("Exited program")
    elif prompt.upper() == "M":
        main()
    return str(prompt)

def checkRequirements(schemaDirectory):
    requiredResources = ["CommonTypes-Schema.xsd"]
    schemaDirectory = schemaDirectory.rstrip("/") # Remove if any trailing / from end of path
    unmetResources = []
    requirementsMet = True


    for resource in requiredResources:
        if not os.path.isfile(f'{schemaDirectory}/{resource}'):
            unmetResources.append(resource)
            requirementsMet = False

    if not requirementsMet:
        message = f"Missing the following in {schemaDirectory}: "
        for resource in unmetResources:
            message += f"\n{resource}"

        message += f"\nPlease add requirements to schema directory: "
        extraPrompt(message)
        checkRequirements(schemaDirectory)



def fsaInput(schema: str, submission: str): # Defining type suggestions
    if os.path.exists(schema):
        if submission.split(".")[-1] == "xml":
            if not os.path.isfile(submission):
                message = (f"Submission file not found, re-enter the correct submission path: ")
                resubmit = extraPrompt(message)
                return fsaInput(schema, resubmit)
                        
            sourceDirectory = schema.rstrip("/") # Return directory name, removing any trailing whitespace, if a directory is given as a/b/, return a/b
            
            if not os.path.isfile(f"{sourceDirectory}/{schemaFileName}"):
                message = f"Please add FSA-Schema file to {sourceDirectory}: "
                resubmit = extraPrompt(message)
                return fsaInput(schema, submission)

            checkRequirements(sourceDirectory)
            return schema, submission
    
        else:
            message = f"Wrong file format for submission, re-enter the correct submission: "
            resubmit = extraPrompt(message)
            print(resubmit)
            return fsaInput(schema, resubmit) 

    else:
        message = f"Directory not found, re-enter the absolute path: "
        redirSchema = extraPrompt(message)
        return fsaInput(redirSchema, submission)

    
def validate(fsaSchema: str, fsaSubmission: str):
        schemaDir = fsaSchema.rstrip('/') # Removes any trailing slashes from directory path in case, to prevent path faults
        schemaFile = f"{schemaDir}/{schemaFileName}"

        try:
            schemaTree = etree.parse(schemaFile) # Converts .xsd into an ET object
            
        except Exception as E:
            extraPrompt(f"Error parsing schemafile:\n{E}: ")
            return main()
        
        try:
            schemaRoot = schemaTree.getroot()
            schemaLocation = schemaRoot.find("{http://www.w3.org/2001/XMLSchema}include") # The namespace is enwrapped by {} where it automatically assigns the prefix found which is xs:

            if schemaLocation is not None:
                schemaLocation.set("schemaLocation", "CommonTypes-Schema.xsd")
            else:
                extraPrompt(f"Unable to find schemaLocation: ")
                return main()
            
        except Exception as E:
            extraPrompt(f"Error modifying schema:\n{E}: ")
            return main()

        
        try:
            schema = etree.XMLSchema(schemaTree) # Converts the parsed schema elementtree object into an XML schema validator

        except Exception as E:
            extraPrompt(f"Error parsing schema ET:\n{E} ")
            return main()
        
        try:
            submissionTree = etree.parse(fsaSubmission) # Converts .xml submission into an ET object
            isvalid = schema.validate(submissionTree)

            if isvalid:
                return {"success": True}
            else:
                errors = ""
                for error in schema.error_log:
                    errors+=f"{error}\n"
                return {"success": False, "errors":errors}
        
        except Exception as E:
            print(f"Error parsing or validating:\n{E} ")
            main()



def main(**kwargs):
    print("---------------------------------------\nType Q to exit program\nType M to return to main\nPress enter for next step\n---------------------------------------\n")

    if "schemaDir" in kwargs and kwargs["schemaDir"]: # The double condition used for checking if key in kwargs, and it's not empty or none
        fsaSchema = str(kwargs["schemaDir"])
    else:
        fsaSchema = extraPrompt(str("Enter the absolute path of the directory containing the FSA029 schema: "))

    if "submission" in kwargs and kwargs["submission"]:
        fsaSubmission = str(kwargs["submission"])
    else:
        fsaSubmission = extraPrompt(str("Enter the absolute path of the FSA029 submission: "))


    fsaSchema, fsaSubmission = fsaInput(fsaSchema, fsaSubmission) # Returns any changes made to the schema or submission through input checking function

    validateResults = validate(fsaSchema, fsaSubmission) 
    
    
    if validateResults.get("success") == True:
        print("Submission successfully validated against schema.")
    elif validateResults.get("success") == False:
        print(f"Submission unsuccessful validated against schema:\n{validateResults.get('errors')}")


if __name__ == "__main__":
    args = {}
    for arg in sys.argv[1:]: # Case for handling passed args in cmd line
        if "=" in arg:
            key, val = arg.split("=", 1)
            args[key] = val
        
    main(**args)