import requests


class LLMClient:
    # def __init__(self, model="llama3"):
    def __init__(self, model="phi3"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def generate_response(self, prompt: str):
        print("Started Prompting")
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(self.url, json=data)
            print("Response Got !!")

            if response.status_code == 200:
                print("Inside 200 branch")
                result = response.json()
                print("LLM raw response :: \n")
                print(result)
                tmp_resp = result.get("response", "No response field got from LLM")
                if not tmp_resp.strip():
                    print("EMPTY response from LLM")
                    return "EMPTY response from LLM"
                return tmp_resp

            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None
        except requests.exceptions.Timeout:
            print("Request Timed Out -- Check Model Timeout or Slow Response")
            return None
        except Exception as e:
            print(f"Exception ::  {e}")
            return None
