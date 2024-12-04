papers = pz.Dataset("bdf-usecase3-tiny", schema=ScientificPaper)
to_extract = papers.convert({{ schema }}, desc={{ schema }}.__doc__, cardinality=pz.Cardinality.ONE_TO_MANY)
output = to_extract

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
                        allow_code_synth={{ allow_code_synth }},
                        allow_token_reduction={{ allow_token_reduction }},
                        execution_engine=engine)

results = []
statistics = []

for idx, (extraction, plan, stats) in enumerate(iterable):
    
    record_time = time.time()
    statistics.append(stats)

    for ex in extraction:
        ex_obj = {}
        for name in {{ schema }}.fieldNames():
            ex_obj[name] = ex.__getattribute__(name)
        print(ex_obj)
        results.append(ex_obj)

results_df = pd.DataFrame(results)
results_df