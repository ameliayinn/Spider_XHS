import json
import time
from apis.xhs_pc_apis import XHS_Apis
from xhs_utils.common_util import init
from xhs_utils.xhs_util import generate_request_params
from xhs_utils.xhs_creator_util import generate_xs, get_common_headers
from xhs_utils.xhs_util import splice_str, generate_x_b3_traceid
import requests
from xhs_utils.cookie_util import trans_cookies

def test_delete_endpoints():
    cookies_str, _ = init()
    xhs = XHS_Apis()

    # 获取 user_id
    success, msg, info2 = xhs.get_user_self_info2(cookies_str)
    if not success:
        return
    user_id = info2["data"]["user_id"]

    # 获取自己发布的笔记
    success, msg, res = xhs.get_user_note_info(user_id, "", cookies_str)
    if not success or not res.get("data", {}).get("notes"):
        print("没有发布的笔记", msg)
        return

    notes = res["data"]["notes"]
    note = notes[0]
    note_id = note["note_id"]
    title = note.get("title", "未知标题")
    print(f"尝试删除目标笔记: {note_id} - {title}")

    # edith_url
    edith_url = "https://edith.xiaohongshu.com"
    cookies_dict = trans_cookies(cookies_str)
    
    endpoints = [
        ("/web_api/sns/v1/note/delete", {"note_id": note_id}),
        ("/web_api/sns/v2/note/delete", {"note_id": note_id}),
        ("/api/sns/web/v1/note/delete", {"note_id": note_id}),
    ]

    for api, data in endpoints:
        print(f"\n--- 尝试 EDITH: POST {api}")
        try:
            # First try xhs_pc_apis logic
            headers, cookies, data_encoded = generate_request_params(cookies_str, api, data, 'POST')
            response = requests.post(
                "https://www.xiaohongshu.com" + api, 
                headers=headers, 
                data=data_encoded.encode('utf-8') if isinstance(data_encoded, str) else data_encoded, 
                cookies=cookies,
                proxies={"http": None, "https": None}
            )
            print(f"    [WWW] HTTP {response.status_code}")
            print(f"    [WWW] Response: {response.text[:500]}")
            if response.status_code == 200 and response.json().get("success"):
                return
        except Exception as e:
            print(f"    [WWW] Exception: {e}")

        try:
            # Then try creator logic
            headers = get_common_headers()
            xs, xt, data_gen = generate_xs(cookies_dict['a1'], api, data)
            headers['x-b3-traceid'] = generate_x_b3_traceid()
            headers['x-s'], headers['x-t'] = xs, str(xt)
            if isinstance(data_gen, dict):
                 data_encoded = json.dumps(data_gen, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
            else:
                 data_encoded = data_gen.encode('utf-8') if isinstance(data_gen, str) else data_gen
                 
            response = requests.post(
                edith_url + api, 
                headers=headers, 
                data=data_encoded, 
                cookies=cookies_dict,
                proxies={"http": None, "https": None}
            )
            print(f"    [EDITH] HTTP {response.status_code}")
            print(f"    [EDITH] Response: {response.text[:500]}")
            if response.status_code == 200 and response.json().get("success"):
                return
        except Exception as e:
            print(f"    [EDITH] Exception: {e}")
        time.sleep(1)

if __name__ == "__main__":
    test_delete_endpoints()
