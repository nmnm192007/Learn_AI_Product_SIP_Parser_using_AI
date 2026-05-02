import requests


class LLMClient:
    def __init__(self, model="llama3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def generate_response(self, prompt: str):
        print("Started Prompting")
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = requests.post(self.url, json=data)

        if response.status_code == 200:
            result = response.json()
            return result["response"]
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
