import time
import random
from apis.xhs_pc_apis import XHS_Apis
from xhs_utils.common_util import init
from loguru import logger

class BatchCleaner:
    def __init__(self, cookies_str: str):
        self.cookies_str = cookies_str
        self.xhs_apis = XHS_Apis()

    def get_self_user_id(self):
        # 优先使用自用的 userInfo2 获取 24 位 user_id
        success, msg, self_info2 = self.xhs_apis.get_user_self_info2(self.cookies_str)
        if success:
            return self_info2.get("data", {}).get("user_id")
        
        # fallback 获取方式
        success, msg, self_info = self.xhs_apis.get_user_self_info(self.cookies_str)
        if success:
            return self_info.get("data", {}).get("basic_info", {}).get("red_id")
        return None

    def batch_unlike(self):
        user_id = self.get_self_user_id()
        if not user_id:
            logger.error("无法获取当前登录用户的 user_id，请检查 cookie！")
            return
        
        cursor = ""
        total_unliked = 0
        logger.info(f"开始批量取消点赞任务，操作用户ID: {user_id}")
        
        while True:
            logger.info(f"正在拉取点赞列表，当前游标 cursor: {cursor}")
            success, msg, res_json = self.xhs_apis.get_user_like_note_info(user_id, cursor, self.cookies_str)
            if not success:
                logger.error(f"拉取点赞列表失败: {msg}")
                break
            
            notes = res_json.get("data", {}).get("notes", [])
            if not notes:
                logger.info("当前页没有点赞记录！")
                break
            
            for note in notes:
                note_id = note.get("note_id")
                title = note.get("title", "未知标题")
                if not note_id:
                    continue
                    
                logger.info(f"尝试取消点赞: {note_id} | 标题: {title}")
                success_unlike, msg_unlike, res = self.xhs_apis.unlike_note(note_id, self.cookies_str)
                
                if success_unlike:
                    like_count = res.get("data", {}).get("like_count", "?")
                    logger.info(f"✅ 成功取消点赞 [ {note_id} ] 当前赞数: {like_count}")
                    total_unliked += 1
                else:
                    logger.error(f"❌ 取消点赞失败 [ {note_id} ]: {msg_unlike} 响应 -> {res}")
                
                # 核心防封逻辑：随机延迟
                sleep_time = random.uniform(3.0, 6.0)
                logger.info(f"休眠 {sleep_time:.2f} 秒，防止操作过频风控...")
                time.sleep(sleep_time)

            cursor = res_json.get("data", {}).get("cursor")
            has_more = res_json.get("data", {}).get("has_more")
            if not has_more or not cursor:
                logger.info("所有点赞记录已处理完毕！")
                break

        logger.info(f"批量取消点赞任务结束。共计取消了 {total_unliked} 个赞。")


    def batch_uncollect(self):
        user_id = self.get_self_user_id()
        if not user_id:
            logger.error("无法获取当前登录用户的 user_id，请检查 cookie！")
            return
        
        cursor = ""
        total_uncollected = 0
        logger.info(f"开始批量取消收藏任务，操作用户ID: {user_id}")
        
        while True:
            logger.info(f"正在拉取收藏列表，当前游标 cursor: {cursor}")
            success, msg, res_json = self.xhs_apis.get_user_collect_note_info(user_id, cursor, self.cookies_str)
            if not success:
                logger.error(f"拉取收藏列表失败: {msg}")
                break
            
            notes = res_json.get("data", {}).get("notes", [])
            if not notes:
                logger.info("当前页没有收藏记录！")
                break
            
            for note in notes:
                note_id = note.get("note_id")
                title = note.get("title", "未知标题")
                if not note_id:
                    continue
                    
                logger.info(f"尝试取消收藏: {note_id} | 标题: {title}")
                success_uncollect, msg_uncollect, res = self.xhs_apis.uncollect_note(note_id, self.cookies_str)
                
                if success_uncollect:
                    logger.info(f"✅ 成功取消收藏 [ {note_id} ]")
                    total_uncollected += 1
                else:
                    logger.error(f"❌ 取消收藏失败 [ {note_id} ]: {msg_uncollect} 响应 -> {res}")
                
                # 核心防封逻辑：随机延迟
                sleep_time = random.uniform(3.0, 6.0)
                logger.info(f"休眠 {sleep_time:.2f} 秒，防止操作过频风控...")
                time.sleep(sleep_time)

            cursor = res_json.get("data", {}).get("cursor")
            has_more = res_json.get("data", {}).get("has_more")
            if not has_more or not cursor:
                logger.info("所有收藏记录已处理完毕！")
                break

        logger.info(f"批量取消收藏任务结束。共计取消了 {total_uncollected} 个收藏。")


    def batch_delete_notes(self):
        user_id = self.get_self_user_id()
        if not user_id:
            logger.error("无法获取当前登录用户的 user_id，请检查 cookie！")
            return
            
        cursor = ""
        total_deleted = 0
        logger.info(f"开始批量删除自己发布的笔记，操作用户ID: {user_id}")
        
        while True:
            logger.info(f"正在拉取发布的笔记列表，当前游标: {cursor}")
            success, msg, res_json = self.xhs_apis.get_user_note_info(user_id, cursor, self.cookies_str)
            if not success:
                logger.error(f"拉取笔记列表失败: {msg}")
                break
                
            notes = res_json.get("data", {}).get("notes", [])
            if not notes:
                logger.info("当前页没有发布的笔记！")
                break
                
            for note in notes:
                note_id = note.get("note_id")
                title = note.get("title", "未知标题")
                if not note_id:
                    continue
                    
                logger.info(f"⚠️ 尝试删除笔记: {note_id} | 标题: {title}")
                # 注意：目前删除笔记的大部分请求都会被网关拦截
                success_del, msg_del, res = self.xhs_apis.delete_note(note_id, self.cookies_str)
                
                if success_del:
                    logger.info(f"✅ 成功删除笔记 [ {note_id} ]")
                    total_deleted += 1
                else:
                    logger.error(f"❌ 删除笔记失败 [ {note_id} ]: {msg_del} 响应 -> {res}")
                    
                sleep_time = random.uniform(3.0, 6.0)
                time.sleep(sleep_time)

            cursor = res_json.get("data", {}).get("cursor")
            has_more = res_json.get("data", {}).get("has_more")
            if not has_more or not cursor:
                break
                
        logger.info(f"批量删除笔记结束。共计尝试删除 {total_deleted} 篇。")

    def batch_delete_comments(self):
        logger.warning("注意：小红书官方API不支持'获取我的所有评论'的功能。")
        logger.warning("要批量删除评论，通常只能针对某篇已知的特定笔记。")
        note_id = input("请输入要删除评论的目标笔记ID (直接回车退出): ").strip()
        if not note_id:
            return
            
        comment_id = input("请输入你要删除的评论ID: ").strip()
        if not comment_id:
            return
            
        logger.info(f"尝试删除笔记 {note_id} 下的评论 {comment_id}...")
        success, msg, res = self.xhs_apis.delete_note_comment(note_id, comment_id, self.cookies_str)
        if success:
            logger.info("✅ 成功删除评论")
        else:
            logger.error(f"❌ 删除评论失败: {msg} 响应 -> {res}")


if __name__ == "__main__":
    # 初始化读取 .env 中的 Cookies 等配置
    cookies_str, _ = init()
    cleaner = BatchCleaner(cookies_str)
    
    print("-----------------------------------")
    print("      小红书批量删除执行器")
    print("  警告：批量写操作容易触发账号风控!")
    print("-----------------------------------")
    print("1. 批量取消点赞 (Batch Unlike)")
    print("2. 批量取消收藏 (Batch Uncollect)")
    print("3. 批量删除笔记 (Batch Delete Notes)")
    print("4. 删除指定评论 (Delete Target Comment)")
    choice = input("请输入要执行的操作编号 (1/2/3/4): ").strip()
    
    if choice == "1":
        cleaner.batch_unlike()
    elif choice == "2":
        cleaner.batch_uncollect()
    elif choice == "3":
        cleaner.batch_delete_notes()
    elif choice == "4":
        cleaner.batch_delete_comments()
    else:
        print("未知的选择，退出...")
