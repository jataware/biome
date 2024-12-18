if "dataset" not in locals():
    dataset = pz.Dataset("{{ input_dataset }}", schema=ScientificPaper)
convert_schema = {{ schema }}

cardinality_str = "{{cardinality}}"

cardinality = pz.Cardinality.ONE_TO_MANY if cardinality_str == "one_to_many" else pz.Cardinality.ONE_TO_ONE

dataset = dataset.convert(convert_schema, desc={{ schema }}.__doc__, cardinality=cardinality)

dataset