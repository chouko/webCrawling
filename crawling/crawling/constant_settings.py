from os.path import dirname, abspath

START_URLS = ['https://www.zjgj.ca/action?pageNum=1']
DOMAIN = 'https://www.zjgj.ca/'
HOST = 'www.zjgj.ca'

DETAIL_PATTERN = ".//div[contains(@class,'media item')]/a"
NEXT_PAGE_XPATH = "//ul[contains(@class,'pagingArea')]/li/a[3]/@href"
FINAL_PAGE_XPATH = "//ul[contains(@class,'pagingArea')]/li/a[4]/@href"
ABS_PATH = dirname(dirname(abspath(__file__))) + '/news2/'
HEAD = '<head>' \
       '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">' \
       '<title>加拿大中部省份公立中学教育局-中加国际</title>' \
       '<base href="/" />' \
       '<meta name="description">' \
       '<meta name="Keywords">' \
       '<link rel="shortcut icon" type="image/x-icon" ' \
       'href="http://xy-hzj.oss-cn-shanghai.aliyuncs.com/zj/1585564919587.png">' \
       '<meta http-equiv="X-UA-Compatible" content="ie=edge">' \
       '<meta name="renderer" content="webkit">' \
       '<link href="css/normalize.css" type="text/css" rel="stylesheet">' \
       '<link href="lib/bootstrap-3.3.7-dist/css/bootstrap.css" type="text/css" rel="stylesheet">' \
       '<script src="js/jquery-3.1.1.min.js"></script>' \
       '<script src="lib/bootstrap-3.3.7-dist/js/bootstrap.min.js"></script>' \
       '<script src="js/rem.js"></script><meta name="viewport" content="initial-scale=1,maximum-scale=1, ' \
       'minimum-scale=1">' \
       '<link rel="stylesheet" href="/css/init.css">' \
       '<script>' \
       'sessionStorage.setItem("firstactive", 6)' \
       '</script>' \
       '</head>'
BODY = '<body>%s<script src="js/main.js"></script></body>'
HTML = '<html lang="en" data-dpr="1" style="font-size: 82.9333px;">%s%s</html>'
KEY_WORD = ['项目', '快捷', '快速']
DATE_TIME_PATTERN = r'^(?:(?!0000)[0-9]{4}-(?:(?:0[1-9]|1[0-2])-(?:0[1-9]|1[0-9]|2[0-8])|' \
                    r'(?:0[13-9]|1[0-2])-(?:29|30)|' \
                    r'(?:0[13578]|1[02])-31)|' \
                    r'(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00)-02-29)' \
                    r'\s+([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$'
