import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "z5w_7QoNuv-PziHyHPjrv_fKcKhYzVDd_vhj4IWS2dli"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [["f0","f1","f2"]], "values":[[123,5,320]] }]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/689614b2-8ded-4e79-aaac-49675c769d5b/predictions?version=2022-05-31', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
# print(response_scoring.json())
pred= response_scoring.json()
output=pred['predictions'][0]['values'][0][0]
print(output)