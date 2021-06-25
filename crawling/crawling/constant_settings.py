from os.path import dirname, abspath

START_URLS = ['https://www.zjgj.ca/action?pageNum=1']
DOMAIN = 'https://www.zjgj.ca/'
HOST = 'www.zjgj.ca'

DETAIL_PATTERN = "//div[contains(@class,'media item')]/a"
NEXT_PAGE_XPATH = "//ul[contains(@class,'pagingArea')]/li/a[3]/@href"
FINAL_PAGE_XPATH = "//ul[contains(@class,'pagingArea')]/li/a[4]/@href"
ABS_PATH = dirname(dirname(abspath(__file__))) + '/news/'
