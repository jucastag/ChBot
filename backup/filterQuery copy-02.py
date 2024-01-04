import os
from dotenv import load_dotenv
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")
endpoint=OPENAI_API_BASE
deployment_name=AZURE_OPENAI_DEPLOYMENT
api_key=OPENAI_API_KEY

kernel = sk.Kernel()

deployment, api_key, endpoint = AZURE_OPENAI_DEPLOYMENT, OPENAI_API_KEY, OPENAI_API_BASE
azure_chat_service = AzureChatCompletion(deployment_name="chat", endpoint=endpoint, api_key=api_key)   # set the deployment name to the value of your chat model
kernel.add_chat_service("chat_completion", azure_chat_service)

sk_prompt = """
{{$input}}

## Task Goal

Analyze input and generate ganerate a filter query for performance and speed, camera quality and diplay quality features.
Inputs is from an app user looking for different cellphone models recommendations from an AI assistant. From their input it could be infered a valuation for features 'performance_and_speed', 'camera_quality' and 'display_quality'

## Task instructions

filterable fields:'performance_and_speed' 'camera_quality' and 'display_quality'.
Posible values: 'High', 'Medium', 'Low'.

Analyze input and identify if it references to of features performance and speed, camera quality or display quality. Generate a filter query string like the examples below:
"".
"(camera_quality eq 'High')".
"(performance_and_speed eq 'Medium') and (camera_quality eq 'Medium' or camera_quality eq 'Low') and (display_quality eq 'Low' or -display_quality eq 'Medium')".
"(performance_and_speed eq 'Low') and (camera_quality eq 'Low') and (display_quality eq 'Low')".

- The output is a string object with the generated filter query string.
- Do not generate code or though process used to generate the filter query. The only output should be the generated filter query string object, nothing else.
- Do not include the word string at begginning of the output.
- If not clear reference to features, return an empty string "". Do not associate brands and models with feature valuations.
- Use your imagination and create innovative and creative filter querys. do not stick with examples given. We need you to work in new filter queries.
- The output should not include the word ANSWER or any other text execpt for the filter query string.
"""
text = """
    Im looking for a phone to use at work.
"""

tldr_function = kernel.create_semantic_function(prompt_template=sk_prompt, max_tokens=300, temperature=0, top_p=0.5)

summary = tldr_function(text)

print(f"Output: {summary}") # Output: Robots must not harm humans.