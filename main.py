import os
import openai

openai.api_key =  os.getenv("OPENAI_API_KEY")

def run():
	while True:
		msg = input("<MSG>: ")
		response = getResponse(msg)
		print("<IA>: " + response)

def getResponse(prompt):
	response = openai.ChatCompletion.create(
	model="gpt-3.5-turbo",
	messages=[
		{
		"role": "system",
		"content": "Eres una IA amistosa"
		 },{
		"role": "user",
		"content": prompt
			}
		],
		max_tokens=200
	)
	return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
	run()