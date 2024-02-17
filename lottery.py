from statistics import mean
import time
from web3 import Web3
import requests
import random
from datetime import datetime
import config
import fun
from fun import *


current_datetime = datetime.now()
print(f"\n\n {current_datetime}")
print(f'============================================= Плюшкин Блог =============================================')
print(f'subscribe to : https://t.me/plushkin_blog \n============================================================================================================\n')

keys_list = []
with open("private_keys.txt", "r") as f:
    for row in f:
        private_key=row.strip()
        if private_key:
            keys_list.append(private_key)

random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i+=1
    if config.proxy_use == 2:
        while True:
            try:
                requests.get(url=config.proxy_changeIPlink)
                fun.timeOut("teh")
                result = requests.get(url="https://yadreno.com/checkip/", proxies=config.proxies)
                print(f'Ваш новый IP-адрес: {result.text}')
                break
            except Exception as error:
                print(' !!! Не смог подключиться через Proxy, повторяем через 2 минуты... ! Чтобы остановить программу нажмите CTRL+C или закройте терминал')
                time.sleep(120)

    try:
        web3 = Web3(Web3.HTTPProvider(config.rpc_links['rpc'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address    
        log(f"I-{i}: Начинаю работу с {wallet}")
        balance = web3.eth.get_balance(wallet)
        balance_decimal = Web3.from_wei(balance, 'ether')        

        if balance_decimal < config.minimal_need_balance:
            log("Недостаточно эфира.  жду когда пополнишь. на следующем круге попробую снова")
            fun.save_wallet_to("no_money_wa", wallet)
            keys_list.append(private_key)
            timeOut("teh")
            continue 

        
        value = web3.to_wei(0.005 , "ether")
        to = web3.to_checksum_address("0x714cC658141275e6E1cb4bF6BeC5b7d99f5d6B06")
        input_data_1 = '0x1249c58b'

        gas_price = int(web3.eth.gas_price*config.gas_kef)
        transaction = {
            'chainId': web3.eth.chain_id,
            'from': wallet,
            'to': to,
            'value': value,
            "gasPrice": gas_price,
            'nonce': web3.eth.get_transaction_count(wallet),
            'data': input_data_1,
        }
        gasLimit = web3.eth.estimate_gas(transaction)
        transaction['gas'] = int(gasLimit * config.gas_kef)

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        txn_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
        tx_result = web3.eth.wait_for_transaction_receipt(txn_hash)

        if tx_result['status'] == 1:
            fun.log_ok(f'MINT  OK: https://testnet.blastscan.io/tx/{txn_hash}')
        else:
            fun.log_error(f'MINT  false: https://testnet.blastscan.io/tx/{txn_hash}')
            keys_list.append(private_key)   



    except Exception as error:
        fun.log_error(f'false: {error}') 
        keys_list.append(private_key)
        timeOut()

        

    timeOut()
    
    # keys_list.append(private_key)

        
  
    
log("Ну типа все, кошельки закончились!")        

