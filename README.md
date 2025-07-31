# FSA029 Validator

This python program is responsible for validating the FSA029 submission against the FSA029 schema for the Bank of England.

## Requirements

Only one external Python library is needed for parsing and validating each XML and XSD file formats.

```pip install lxml```

## Usage

You can run the validator program on its own, where you will be prompted with inputs for the schema directory and submission file.

Or, you can pass arguments into a command line to include the paths for both schema directory and submission file (don't  wrap in string quotations).

```python3 FSA029_validator.py schemaDir=/example submission=/example.xml```


## Notes

The FSA submission file does not need to be in the same directory as the FSA schema directory. However, the CommonTypes schema must be in the same source directory as the FSA schema.

The schema file is assumed to be named "FSA029-Schema.xsd". Its directory name doesn't matter, as well as the submission name.


## The extra mile

a) In the full submission file, the element "PartnershipsSoleTraders" is logged as not expected. The valid file provided is a subsection of the full file which works, using a document comparator website such as [TextCompare](https://www.diffchecker.com/text-compare/), which helps the developer in isolating which section is different/removed/added, to make any corrections to the submission or schema file.

Using the information available, of the full submission + valid submission + full schema + error log, I analyse which segments are changed from the website previously mentioned. The section from <PartnershipsSoleTraders> to </LLPS> is added as child elements of capital. The error message states:

```ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element '{urn:fsa-gov-uk:MER:FSA029:4}PartnershipsSoleTraders': This element is not expected.``

Since the element is not expected, I looked at its parent element to identify any possible restricting attributes. There is a choice between 3 elements with minoccurances = 1, between: IncorporatedEntities, PartnershipsSoleTraders and LLPs. The sample only included IncorporatedEntities, which was valid. However, since you can't have a choice of 1, out of 3 mandatory elements, I identified this as the problem.

---

b) If I made no changes to the schema, I would have to create 3 seperate submissions, where I only include 1 of each: IncludedEntities, PartnershipsSoleTraders and LLPs. If I had to make changes to the schema, I would add an extra attribute with choice, that minoccurs=1 and maxoccurs=unbounded, to allow for multiple of any in any order in one submission file.

---

c) Perhaps a regulator may have included a valid file with an invalid one, to request us to create new submissions from the invalid one for it to pass, or to adjust the schema to allow for multiple elements in one submission.