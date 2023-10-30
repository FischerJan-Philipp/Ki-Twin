import openai
import json
import dotenv
import logging

config = dotenv.dotenv_values(".env")
openai.api_key = config['OPENAI_API_KEY']

testResponseOfCallFuntion = ""

def get_person_description(name, position):
    """Get the description of a person by its name and position"""
    person_info = {
        "name": name,
        "position": position,
        "description": "Kyrill is a student at the HTW currently and works as working student at juwelo Deutschland in Web3 Projectmanagement.",
    }
    testResponseOfCallFuntion = json.dumps(person_info)
    print("__________________________________________________________")
    logging.info('Function get_person_description was called')
    return json.dumps(person_info)

logging.basicConfig(level=logging.INFO)

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": "Kyrill is a student at the HTW currently and works as working student at juwelo Deutschland in Web3 Projectmanagement."}],
    functions=[
    {
        "name": "get_person_description",
        "description": "Get the description of a person by its name and position",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the person",
                },
                "position": {
                    "type": "string",
                    "description": "The position of the person, e.g. CEO, CTO, CFO, Student etc."
                },
            },
            "required": ["name", "position"],
        },
    }
    ],
    function_call="auto",
)

print(testResponseOfCallFuntion)
print(completion)
json_response = json.loads(completion['choices'][0]['message']['function_call']['arguments'])
print(json_response)

reply_content = completion.choices[0]
#funcs = reply_content.to_dict()['function_call']['arguments']
#funcs = json.loads(funcs)
#print(funcs)
#print(funcs['location'])

print(reply_content)