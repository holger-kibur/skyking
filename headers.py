headers = [
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Cache-Control": "no-cache", 
        "Host": "www.reddit.com", 
        "Pragma": "no-cache", 
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "none", 
        "Sec-Fetch-User": "?1", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36", 
        "X-Amzn-Trace-Id": "Root=1-60131662-71b4fdab2d6c82bf60d0149c"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.9", 
        "Host": "www.reddit.com", 
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "none", 
        "Sec-Fetch-User": "?1", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.53", 
        "X-Amzn-Trace-Id": "Root=1-601316b7-66b8501f5bf01b1c44fc3db3"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.5", 
        "Host": "www.reddit.com", 
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0", 
        "X-Amzn-Trace-Id": "Root=1-6013176d-50e3a036628bf63a723946e1"
    },
    {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-us", 
        "Host": "www.reddit.com", 
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Mobile/15E148 Safari/604.1", 
        "X-Amzn-Trace-Id": "Root=1-60131760-2346a31d07037bd94c0c5a5b"
    },
]

class HeaderRotator(object):
    def __init__(self):
        self.cur_index = 0

    def get_header(self):
        ret_header = headers[self.cur_index]
        self.cur_index = (self.cur_index + 1) % len(headers)
        return ret_header