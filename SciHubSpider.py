import requests, re
from bs4 import BeautifulSoup as BS
import random

class Scihub_Downloader:
    def __init__(self, doi):
        self.doi = doi
        self.downloadable = False
        try:
            self.pdf_url = self.get_pdf()
        except IndexError:
            self.pdf_url = None
        if self.pdf_url is None:
            self.downloadable = False

    def get_pdf(self):
        baseurl=['https://sci-hub.wf','https://sci-hub.ee', 'https://sci-hub.shop', 'https://sci-hub.se', 'https://sci-hub.st',
                'http://sci-hub.is', 'https://sci.hubg.org', 'https://sci.hubbza.co.za', 'https://sci-hub.ru',
                'https://sci-hub.hkvisa.net', 'https://sci-hub.mksa.top', 'http://sci-hub.ren', 'https://sci-hub.wf','https://sci-hub.se', 'https://sci-hub.st', 'https://sci-hub.ru', 'https://sci.hubg.org/']
        baseurl=list(set(baseurl))
        while True:

            try:
                
        
                # url = f"https://sci-hub.wf/{self.doi}"
                
                domain=random.choice(baseurl)
                url=domain+'/'+self.doi
                print(f'this time we choose is :{url}')
                header = {
                    "authority": domain.split('//')[-1], 
                    "referer": domain, 
                    "user-agent": "Mozilla/5.0"
                }            
                r = requests.get(url, timeout=10, headers=header)
                if r.status_code==200 and not  '404' in r.text:
                    soup = BS(r.text, "html.parser")
                    button = soup.select("#buttons > ul > li > a")
                    click = button[1].attrs["onclick"]
                    print('====',click)
                    pdf_url = re.findall(r"href='(.+?)'", click)[0]
                    print('====',pdf_url)
                    
                    pdf_url = pdf_url.replace("\\/", '/')
                    print(f'pdf url is {pdf_url}')
                    return pdf_url
                else:
                    print(f"404 found ,this doi is not available:{self.doi} in domain :{domain}")

            except:
                print(f"this doi is not available:{self.doi} in domain :{domain}")
                break
    def save_pdf(self, name):
        header = {
            "user-agent": "Mozilla/5.0"
        }
        if not  self.pdf_url is None:
            r_pdf = requests.get(self.pdf_url, headers=header)
            # if len(name) > 100:
            #     name = name[:100]  # 如果名字超过100字符，就只取前100个字符
            name = name if ".pdf" in name else name + ".pdf"
            with open(name, "wb") as fo:
                fo.write(r_pdf.content)
        else:
            print('pls give a valid pdf url',self.pdf_url)

# def test():
#     # 正常情况下，顺利下载
#     doi = "10.1109/tit.2011.2182033"
#     sd = Scihub_Downloader(doi)
#     # print(sd.pdf_url)
#     # sd.save_pdf("thesis/test")
#     print("success.")
    
#     # 通常情况下，没有这个文献
#     doi = "NeverGonnaGiveYouUp"
#     sd = Scihub_Downloader(doi)
#     if sd.downloadable:
#         sd.save_pdf("thesis/test")
#     else:
#         print(f"{doi}\tis fail to download.")
    
#     # 多次爬虫导致封ip测试
#     for i in range(1000):
#         print(f"\r{i+1}/1000", end='')
#         doi = "10.1109/tit.2011.2182033"
#         sd = Scihub_Downloader(doi)
#         if not sd.downloadable:
#             print(f"\n第 {i+1} 次时ip被封")
#             break
#     pass


# if __name__ == "__main__":
#     test()
#     print("finished.")