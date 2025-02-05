papers = pz.Dataset("bdf-usecase3-tiny", schema=ScientificPaper)
references = papers.convert(Reference, desc="A paper cited in the reference section", cardinality=pz.Cardinality.ONE_TO_MANY)
output = references

engine = pz.StreamingSequentialExecution
if "{{ policy_method }}" == "min_cost":
    policy = pz.MinCost()
elif "{{ policy_method }}" == "max_quality":
    policy = pz.MaxQuality()
iterable  =  pz.Execute(output,
                        policy = policy,
                        nocache=True,
                        allow_sentinels = False,
                        allow_code_synth=False,
                        allow_token_reduction=False,
                        execution_engine=engine)

references = []
statistics = []

for idx, (reference, plan, stats) in enumerate(iterable):
    
    record_time = time.time()
    statistics.append(stats)

    for ref in reference:
        try:
            index = ref.index
        except:
            continue
        ref_obj = {
            "title": ref.title,
            "index": index,
            "first_author": ref.first_author,
            "year": ref.year,
            "source": ref.filename,
        }
        print(ref_obj)
        references.append(ref_obj)

references_df = pd.DataFrame(references)
references_df