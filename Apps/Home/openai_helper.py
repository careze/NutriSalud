import openai

openai.api_key = 'sk-proj-6Kf0Sj5IYNihYr6pyff1T3BlbkFJUXHOnAAMmXM5e1OhPCQO'

def get_openai_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    message = response.choices[0].text.strip()
    return message
