import pandas as pd
import os, json, re, time, requests
from SciHubSpider import Scihub_Downloader as SD
import pickle

# Read CSV file with a single column
data = pd.read_csv('HINE为主题  doi存在缺失_HINE 主题.csv')


# 把 title 转变为符合 Windows 命名规范的 name
def title2filename(title):
    name = re.sub(r'[<>:"/\\|?*\n]+', '_', title)
    if len(name) > 100:
        name = name[:100]
    return name
output='hine-en'
if not os.path.exists(output):
    os.mkdir(output)
# 获取已下载文献数量
t = os.listdir(output)
if os.path.exists(output+"/fail2download.txt"):
    t.remove("fail2download.txt")
thesis_seq = len(t) + 1
    
paper_store = []

for index, row in data.iterrows():
    # print(row)
    doi=row["DOI"]
    title=row["Article Title"]
    journal=row['Journal Abbreviation']
    citation=''
    date=''
    name=title2filename(title)
    if doi:
        

        paper_store.append({
            'journal': journal,
            'title': title,
            'citation': citation,
            'date': date,
            'url1': doi,
        })
        with open('hine.pickle', 'wb') as file:        
            pickle.dump(paper_store, file)

        # try:
        #     sd = SD(doi)
        # except requests.exceptions.ConnectTimeout:
        #     # 连接超时的情况
        #     time.sleep(1)
        #     print(f"\r\033[1;33;40m{name}\033[0m is timeout-connecting.")
        #     with open(f"{output}/fail2download.txt", "a", encoding='utf-8') as fo:
        #         fo.write(f"{doi}\t{name}\tConnectTimeout.\n")
        # except requests.exceptions.ReadTimeout:
        #     # 读取(?)超时的情况
        #     time.sleep(1)
        #     print(f"\r\033[1;33;40m{name}\033[0m is timeout-reading.")
        #     with open(f"{output}/fail2download.txt", "a", encoding='utf-8') as fo:
        #         fo.write(f"{doi}\t{name}\tReadTimeout.\n")
        # except:
        #     # 未知情况
        #     time.sleep(1)
        #     print(f"\r\033[1;33;40m{name}\033[0m is fail to download.")
        #     with open(f"{output}/fail2download.txt", "a", encoding='utf-8') as fo:
        #         fo.write(f"{doi}\t{name}\tUnknown.\n")
        # else:
        #     if sd.downloadable:
        #         sd.save_pdf(f"{output}/{thesis_seq:0>4d}.{name}.pdf")
        #         thesis_seq += 1
        #     else:
        #         # 保存未成功下载的文献信息
        #         print(f"\r\033[1;33;40m{name}\033[0m is not included.")
        #         with open("fail2download.txt", "a", encoding='utf-8') as fo:
        #             fo.write(f"{doi}\t{name}\tNotIncluded.\n")
        # finally:
        #     print(f"\r进度：{index:>4d}/{len(data)}", end='')