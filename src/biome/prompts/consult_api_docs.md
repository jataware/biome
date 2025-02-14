This tool is used to ask a question of an API. It allows you to ask a question of an API's documentation and get results in
natural language, which may include code snippets or other information that you can then use to write code to interact with the API 
(e.g. using the `BiomeAgent__run_code` tool). You can also use this information to refine your goal when using the `draft_api_code` tool.

You can ask questions related to endpoints, payloads, etc. For example, you can ask "What are the endpoints for this API?"
or "What payload do I need to send to this API?" or "How do I query for datasets by keyword?" etc, etc.

If you use this tool, you MUST indicate so in your thinking. Wrap the tool name in backticks.

Args:
    api (str): The name of the API to use
    query (str): The question you want to ask about the API.

Returns:
    str: returns instructions on how to utilize the API based on the question asked. 