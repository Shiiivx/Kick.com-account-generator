import requests, json, time, sys, console

apiKey = json.load(open("config.json"))["salamoonder_apiKey"]
pjs = "https://kick.com/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/p.js"
def salamoonder():
    headers = {"Host": "salamoonder.com", "Content-Type": "application/json"}
    payload = json.dumps({"api_key": apiKey, "task": {"type": "KasadaCaptchaSolver", "pjs": pjs, "cdOnly": "false"}})

    for _ in range(3):
        try:
            response = requests.post("https://salamoonder.com/api/createTask", headers=headers, data=payload, timeout=30).json()
            if "taskId" not in response:
                if response.get("error_description") == "Invalid API key.":
                    sys.exit("Invalid salamoonder.com API key")
                return salamoonder()

            taskId = response["taskId"]
            for _ in range(10):
                result = requests.post("https://salamoonder.com/api/getTaskResult", headers=headers, data=json.dumps({"api_key": apiKey, "taskId": taskId}), timeout=30).json()
                if result.get("status") == "ready":
                    if "error" in result.get("solution", {}) or "No solution created" in result.get("solution", {}):
                        return salamoonder()
                    return result["solution"]
                time.sleep(0.3)
        except Exception:
            time.sleep(0.3)
    return salamoonder()
