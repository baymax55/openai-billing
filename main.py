import requests
from datetime import datetime, timedelta
import json
from decimal import Decimal, ROUND_HALF_UP

# set url and form data
# 查询使用量URL
usage_url = '/v1/dashboard/billing/usage'
# 查询订阅信息URL
subscription_url = '/v1/dashboard/billing/subscription'

expire_time_url = 'dashboard/billing/credit_grants'
host = 'https://api.openai.com'
apikey = 'sk-xxx'
# set params as a dictionary
params = {
    # start date is 90 days ago
    'start_date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
    # end date is tomorrow
    'end_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
}

# set headers and authorization
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + apikey}

# set proxies
proxies = {'http': 'http://127.0.0.1:7890', 'https': 'https://127.0.0.1:7890'}

# send POST request
# expire_response = requests.get(host + expire_time_url, headers=headers)
usage_response = requests.get(host + usage_url, headers=headers, params=params)
subscription_response = requests.get(host + subscription_url, headers=headers)

# get response body
usage_result = usage_response.text
subscription_result = subscription_response.text

# 获取总额
total_usd = Decimal(json.loads(subscription_result)['hard_limit_usd'])
expire_seconds = Decimal(json.loads(subscription_result)['access_until'])
date = datetime.fromtimestamp(int(expire_seconds))

# 获取使用量
total_usage = Decimal(json.loads(usage_result)['total_usage'])

# divide by 100 to convert from cents to dollars
usage_in_dollars = total_usage / Decimal('100').quantize(Decimal('.001'), rounding=ROUND_HALF_UP)

print(f"实际已使用金额:{usage_in_dollars}")
print(f"总共金额:{total_usd}")
print(f"过期日期:{date.isoformat()}")
