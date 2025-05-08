import requests

class EvolutionAPIClient:
    def __init__(self):
        pass

    @staticmethod
    def send_message(message: str, instance: str, instance_key: str, sender_number: str):
        url = f"http://localhost:8080/message/sendText/{instance}"
        payload = {
            "number": sender_number,
            "text": message,
            "delay": 2000,
        }
        headers = {
            "apikey": instance_key,
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        return response