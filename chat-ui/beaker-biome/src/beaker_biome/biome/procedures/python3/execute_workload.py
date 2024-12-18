if "dataset" not in locals():
    output = "{{ output_dataset }}"
else:
    output = dataset

policy_method = "{{ policy_method }}"

# optimization block
engine = pz.StreamingSequentialExecution
if policy_method == "min_cost":
    policy = pz.MinCost()
elif policy_method == "max_quality":
    policy = pz.MaxQuality()
iterable  =  pz.Execute(output,
                        policy = policy,
                        nocache=True,
                        allow_code_synth="{{ allow_code_synth }}",
                        allow_token_reduction="{{ allow_token_reduction }}",
                        execution_engine=engine)

results = []
statistics = []

for idx, (extraction, plan, stats) in enumerate(iterable):
    
    record_time = time.time()
    statistics.append(stats)

    for ex in extraction:
        ex_obj = {}
        for name in output.schema.field_names():
            ex_obj[name] = ex.__getattribute__(name)
        print(ex_obj)
        results.append(ex_obj)

results_df = pd.DataFrame(results)
results_df