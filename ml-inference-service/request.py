import requests

url = "https://ml-inference-service-101237808179.europe-west1.run.app/predict"
payload = {
    "features": [6.0, 2.2, 4.0, 1.0]

}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
