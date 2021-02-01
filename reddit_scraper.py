import json
import requests
import multiprocessing
import bs4

num = 0

def recurse_comments(comment_node):
    print("===========================================================")
    print(comment_node.keys())
    global num
    num += 1
    score = comment_node["score"]
    body = comment_node["body"]
    replies = []
    if comment_node["replies"]:
        for child_comment in comment_node["replies"]["data"]["children"]:
            if child_comment["kind"] == "Listing":
                replies.append(recurse_comments(child_comment["data"]))
    return {
        "score": score,
        "body": body,
        "replies": replies,
    }

def parse_post():
    with open("sample_post.json", "r") as f:
        raw = f.read()
    post = json.loads(raw)
    post_info = {}
    post_info["title"] = post[0]["data"]["children"][0]["data"]["title"]
    post_info["content"] = post[0]["data"]["children"][0]["data"]["selftext"]
    post_info["comments"] = []
    for toplevel in post[1]["data"]["children"]:
        post_info["comments"].append(recurse_comments(toplevel["data"]))
    print(post_info["comments"])
    print(num)

def scrape_wsb():
    # top_posts_json = requests.get("https://www.reddit.com/r/wallstreetbets/top.json?t=today&limit=500", headers={
    #     # Spoof chrome browser client so there isn't a rate limitation :))
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    #     "Accept-Encoding": "gzip, deflate, br", 
    #     "Accept-Language": "en-US,en;q=0.9", 
    #     "Host": "www.reddit.com", 
    #     "Sec-Fetch-Dest": "document", 
    #     "Sec-Fetch-Mode": "navigate", 
    #     "Sec-Fetch-Site": "none", 
    #     "Sec-Fetch-User": "?1", 
    #     "Upgrade-Insecure-Requests": "1", 
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36", 
    #     "X-Amzn-Trace-Id": "Root=1-601311fc-0a691ab85e502bf44570dd8e",
    # })
    # Parse post json
    with open("sample_front.json", "r") as f:
        raw = f.read()
    top_posts = json.loads(raw)["data"]["children"]
    parsed_posts = []
    for post in top_posts:
        print("->", post["data"]["permalink"][-20:])
    # with multiprocessing.Pool() as threadpool:
    #     parsed_posts = threadpool.map(parse_post, [post["data"]["permalink"] for post in top_posts])
