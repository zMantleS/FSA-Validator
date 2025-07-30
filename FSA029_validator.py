import os
import sys
from lxml import etree

quitText = "or type Q to exit program: "

def quitPrompt(message):
    prompt = str(input(message))
    if prompt.upper() == "Q":
        sys.exit("Exited program")

def checkRequirements(schemaDirectory):
    requiredResources = ["CommonTypes-Schema.xsd"]
    requirementsMet = True


    for resource in requiredResources:
        if os.path.isfile(f'{schemaDirectory}/{resource}'):
            requiredResources.remove(resource)

        else:
            requirementsMet = False

    if not requirementsMet:
        message = f"Missing the following in {schemaDirectory}: "
        for resource in requiredResources:
            message += f"\n{resource}"

        message += f"\nPlease add requirements to schema directory, {quitText} "
        quitPrompt(message)
        checkRequirements(schemaDirectory)



def fsaInput(schema: str, submission: str): # Defining type suggestions
    if os.path.exists(schema):
        if submission.split(".")[-1] == "xml":
            sourceDirectory = os.path.dirname(schema.rstrip("/")) # Return directory name, removing any trailing whitespace, if a directory is given as a/b/, return a/b
            checkRequirements(sourceDirectory)
    
        else:
            message = f"Wrong file format for submission, re-enter the correct submission, {quitText}"
            quitPrompt(message)
            fsaInput(schema, submission)

    else:
        print(schema)
        message = f"Directory not found, re-enter the absolute path, {quitText}"
        quitPrompt(message)
        fsaInput(schema, submission)

    
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
    if "schemaDir" in kwargs and kwargs["schemaDir"]:
        fsaSchema = kwargs["schemaDir"]
    else:
        fsaSchema = str(input("Enter the absolute path of the directory containing the FSA029 schema: "))

    if "submission" in kwargs and kwargs["submission"]:
        fsaSubmission = kwargs["submission"]
    else:
        fsaSubmission = str(input("Enter the absolute path of the FSA029 submission: "))

    print(fsaSchema, fsaSubmission)

    fsaInput(fsaSchema, fsaSubmission)
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