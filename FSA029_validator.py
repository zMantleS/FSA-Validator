import os
import sys
from lxml import etree


def extraPrompt(message):
    prompt = str(input(message))
    if prompt.upper() == "Q":
        sys.exit("Exited program")
    elif prompt.upper() == "M":
        main()
    return str(prompt)

def checkRequirements(schemaDirectory):
    requiredResources = ["CommonTypes-Schema.xsd"]
    schemaDirectory = schemaDirectory.rstrip("/")
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
            
            if not os.path.isfile(f"{sourceDirectory}/FSA029-Schema.xsd"):
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
    try:
        schemaDir = fsaSchema.rstrip('/')
        schemaFile = f"{schemaDir}/FSA029-Schema.xsd"
        schemaTree = etree.parse(schemaFile)
        schemaRoot = schemaTree.getroot()
        schemaLocation = schemaRoot.find("{http://www.w3.org/2001/XMLSchema}include")

        if schemaLocation is not None:
            schemaLocation.set("schemaLocation", "CommonTypes-Schema.xsd")
        else:
            print("Unable to find schemaLocation ")

        schema = etree.XMLSchema(schemaTree)
        submissionTree = etree.parse(fsaSubmission)
        isvalid = schema.validate(submissionTree)

        if isvalid:
            return True
        else:
            return False
        
    except:
        print("Something went wrong during validation...")



def main(**kwargs):
    print("---------------------------------------\nType Q to exit program\nType M to return to main\nPress enter when done\n---------------------------------------\n")

    if "schemaDir" in kwargs and kwargs["schemaDir"]:
        fsaSchema = str(kwargs["schemaDir"])
    else:
        fsaSchema = extraPrompt(str("Enter the absolute path of the directory containing the FSA029 schema: "))

    if "submission" in kwargs and kwargs["submission"]:
        fsaSubmission = str(kwargs["submission"])
    else:
        fsaSubmission = extraPrompt(str("Enter the absolute path of the FSA029 submission: "))


    fsaSchema, fsaSubmission = fsaInput(fsaSchema, fsaSubmission)
    validateResults = validate(fsaSchema, fsaSubmission)
    
    match validateResults:
        case True:
            print("Submission successfully validated against schema.")
        case False:
            print("Submission unsuccessful validated against schema.")


if __name__ == "__main__":
    args = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, val = arg.split("=", 1)
            args[key] = val
        
    main(**args)