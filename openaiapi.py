import os
import openai
from apikey import key

apikey=key
openai.api_key = apikey

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="write me an application for two days leave form my school\n\nTo: [Principal's Name] \nFrom: [Your Name] \n \nSubject: Request for Two Days Leave \n \nDear Principal [Name],\n\nI am writing to request two days of leave from school, starting [start date].\n\nI am under the weather and need two days of rest in order to recover. I understand that I may be required to provide a doctor's note for the period of my leave.\n\nI have already made arrangements to complete any assignments or tasks assigned to me during this time. I will keep in touch to ensure that I do not fall behind in my classes.\n\nThank you for your understanding.\n\nSincerely,\n[Your Name]",
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

print(response)



'''
{
  "warning": "This model version is deprecated. Migrate before January 4, 2024 to avoid disruption of service. Learn more https://platform.openai.com/docs/deprecations",
  "id": "cmpl-7ntqXIftmMlDyUo1a34f3htUQ1kIN",
  "object": "text_completion",
  "created": 1692127101,
  "model": "text-davinci-003",
  "choices": [
    {
      "text": "",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 161,
    "total_tokens": 161
  }
}
'''