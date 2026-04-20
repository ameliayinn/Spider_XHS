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
        return

    notes = res["data"]["notes"]
    note = notes[0]
    note_id = note["note_id"]
    title = note.get("title", "未知标题")
    print(f"尝试删除目标笔记: {note_id} - {title}")

    # Creator endpoints to try
    creator_url = "https://creator.xiaohongshu.com"
    cookies = trans_cookies(cookies_str)
    
    endpoints = [
        ("/api/galaxy/creator/note/delete", {"note_id": note_id}),
        ("/api/galaxy/creator/manage/delete", {"note_id": note_id}),
        ("/web_api/sns/v1/note/delete", {"note_id": note_id}),
        ("/web_api/sns/v2/note/delete", {"note_id": note_id}),
    ]

    for api, data in endpoints:
        print(f"\n--- 尝试 CREATOR: POST {api}")
        try:
            headers = get_common_headers()
            xs, xt, data_gen = generate_xs(cookies['a1'], api, data)
            headers['x-b3-traceid'] = generate_x_b3_traceid()
            headers['x-s'], headers['x-t'] = xs, str(xt)
            
            # encode data if necessary
            if isinstance(data_gen, dict):
                 data_encoded = json.dumps(data_gen, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
            else:
                 data_encoded = data_gen.encode('utf-8') if isinstance(data_gen, str) else data_gen
                 
            response = requests.post(
                creator_url + api, 
                headers=headers, 
                data=data_encoded, 
                cookies=cookies,
                proxies={"http": None, "https": None}
            )
            print(f"    HTTP {response.status_code}")
            print(f"    Response: {response.text[:500]}")
        except Exception as e:
            print(f"    Exception: {e}")
        time.sleep(1)

if __name__ == "__main__":
    test_delete_endpoints()
