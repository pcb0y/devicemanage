import requests
import json


def token():
    """获取token"""
    app_key = {
              "appKey": "dingpg6vwrr9vldamuph",
              "appSecret": "3e0O1wehazNSr2xQmf2WjNPkQw8oQf1YcA6hFnYSUkQmLekqz0QrfFNQrkLRNzVx"
            }
    data = json.dumps(app_key)
    header = {
        "Content-Type": "application/json"
    }

    response = requests.post(url="https://api.dingtalk.com/v1.0/oauth2/accessToken", data=data, headers=header)
    return json.loads(response.text)


def get_user_id(token_value, phone):

    mobile = {
        "mobile": phone,
        "support_exclusive_account_search": "true"}
    header = {
        "Content-Type": "application/json"
    }
    mobile_json = json.dumps(mobile)
    response = requests.post(url=f"https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token_value}",
                             data=mobile_json, headers=header)
    return json.loads(response.text)


def get_user_detail(token_value, userid):
    data = {
        "language": "zh_CN",
        "userid": userid
        }
    data_json = json.dumps(data)
    header = {
        "Content-Type": "application/json"
    }
    response = requests.post(url=f"https://oapi.dingtalk.com/topapi/v2/user/get?access_token={token_value}",
                             data=data_json, headers=header)
    return json.loads(response.text)


def create_oa(token_value, dept_id, user_id, category, description_problem, device_name):
    """创建机电维修审批流"""

    user_id_list = '[\"'+user_id+'\"]'

    data = {
            "originatorUserId": user_id,
            "processCode": "PROC-A7907958-0B72-42BB-91F2-5605209EC9E1",
            "deptId": dept_id,
            "formComponentValues": [
                    {
                        "name": "申请人",
                        "value": user_id_list

                    },
                    {
                        "name": "维修类别",
                        "value": category

                    },
                    {
                        "name": "维修内容",
                        "value": description_problem
                    },
                    {
                        "name": "维修位置",
                        "value": device_name
                    }
            ]
        }
    data_json = json.dumps(data, ensure_ascii=True)
    print(data_json)
    header = {
        "Content-Type": "application/json"
    }
    response = requests.post(url=f"https://api.dingtalk.com/v1.0/workflow/processInstances?x-acs-dingtalk-access-token={token_value}",
                             data=data_json, headers=header)
    return json.loads(response.text)


if __name__ == '__main__':
    # 获取token
    token = token().get('accessToken')
    phone = '13563238899'
    # 通过手机号获取userid
    user_id = get_user_id(token, phone)
    user = user_id.get("result").get("userid")
    # 通过userid获取用户的dept_id_list部门id
    user_detail = get_user_detail(token, user)
    dept_id_list = user_detail.get('result').get('dept_id_list')[0]
    Category = '电气问题'
    description_problem = '不工作'
    device_name = 'n号封边机'
    response = create_oa(token, dept_id_list, user, Category, description_problem, device_name)
    print(response)
