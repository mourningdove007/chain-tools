import json
import requests
from constants.blockchain import BlockchainAddresses as ba
from scripts.order_requests import generate_order_request


request_body = generate_order_request(ba.ANVIL_TEST_ACCOUNT_2_SECRET)

# Here is our current error
# {"errorType":"InsufficientAllowance","description":"order owner must give allowance to VaultRelayer"}
try:
    response = requests.post(
        ba.ORDERS_URL, 
        headers=ba.HEADERS, 
        data=json.dumps(request_body)
        )
    response.raise_for_status()
    
    print(response)

except requests.exceptions.RequestException as e:
    print(response.text)
except json.JSONDecodeError:
    print(response.text)

