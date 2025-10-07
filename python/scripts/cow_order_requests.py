from eth_account import Account
from eth_account.datastructures import SignedMessage
import time

from constants.blockchain import BlockchainAddresses as ba


def generate_order_request(private_key: str = ba.ANVIL_TEST_ACCOUNT_2_SECRET):
    
    ## see https://docs.cow.fi/cow-protocol/reference/core/signing-schemes
    
    DOMAIN_DATA = {
        "name": "Gnosis Protocol",
        "version": "v2",
        "chainId": 1,
        "verifyingContract": "0x9008D19f58AAbD9eD0D60971565AA8510560ab41"
    }

    ORDER_TYPE = {
        "Order": [
            {"name": "sellToken", "type": "address"},
            {"name": "buyToken", "type": "address"},
            {"name": "receiver", "type": "address"},
            {"name": "sellAmount", "type": "uint256"},
            {"name": "buyAmount", "type": "uint256"},
            {"name": "validTo", "type": "uint32"},
            {"name": "appData", "type": "bytes32"},
            {"name": "feeAmount", "type": "uint256"},
            {"name": "kind", "type": "string"},
            {"name": "partiallyFillable", "type": "bool"},
            {"name": "sellTokenBalance", "type": "string"},
            {"name": "buyTokenBalance", "type": "string"}
        ]
    }

    ## App Data Known Hashes
    ## https://github.com/cowprotocol/services/blob/main/database/sql/V060__app_data_overrides.sql

    ORDER_DATA = {
        "sellToken": ba.WETH_CONTRACT,
        "buyToken": ba.DAI_CONTRACT,
        "receiver": ba.ANVIL_TEST_ACCOUNT_2,
        "sellAmount": "50000000000000000000",
        "buyAmount": "50000000000000000000",
        "validTo": int(time.time()) + 3600,  ## Valid for 1 hour from now
        "feeAmount": "0",
        "kind": "buy",
        "partiallyFillable": False,
        "sellTokenBalance": "erc20",
        "buyTokenBalance": "erc20",
        "appData": "0x1ba2c7f5680dd17a4d852b9c590afa0969893c2b1052a7f553542697f5668171",
    }


    acct :Account = Account.from_key(
    private_key)

    signed_message:SignedMessage = acct.sign_typed_data(
        domain_data=DOMAIN_DATA, 
        message_types=ORDER_TYPE, 
        message_data=ORDER_DATA
        )

    signature_hex = signed_message.signature.hex()

    request_body = ORDER_DATA
    request_body["signingScheme"] = "eip712"
    request_body["signature"] = "0x" + signature_hex

    return request_body
