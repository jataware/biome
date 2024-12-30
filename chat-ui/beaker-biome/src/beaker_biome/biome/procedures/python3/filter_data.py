if "dataset" not in locals():
    print("Setting dataset")
    dataset = pz.Dataset("{{ input_dataset }}", schema=ScientificPaper)
condition = "{{ filter_expression }}"

dataset = dataset.filter(condition)

dataset