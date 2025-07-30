# FSA029 Validator

This python program is responsible for validating the FSA029 submission against the FSA029 schema for the Bank of England.

## Requirements

Only one external Python library is needed for parsing and validating each XML and XSD file formats.

```pip install lxml```

## Usage

You can run the validator program on its own, where you will be prompted with inputs for the schema directory and submission file.

Or, you can pass arguments into a command line to include the paths for both schema directory and submission file (don't  wrap in string quotations).

```python3 fsa_validator(schemaDir=/example, submission=/example.xml```


## Notes

The FSA submission file does not need to be in the same directory as the FSA schema directory. However, the CommonTypes schema must be in the same source directory as the FSA schema.