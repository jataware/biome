# CDA Integration

CRITICAL: Use the CDA integration rather than relying on prior knowledge, as it has changed significantly since your knowledge cutoff.

CRITICAL: Cancer Data Aggregator patient IDs must be preserved as is. If a user asks about patient ID `TCGA.TCGA-BP-5168` you MUST NOT SHORTEN IT and provide it as-is.

CRITICAL: don't change `add_columns` arguments returned from the drafting agent in the CDA integration. Leave them as-is. Do not change the `add_columns=` line from draft_integration_output tool.

CRITICAL: for `cda.get_file_data` calls, ONLY use `add_columns=['file_name', 'file_type', 'access']`
