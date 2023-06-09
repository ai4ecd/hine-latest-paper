# hine-latest-paper

this can used to create a baseline of past research on any topic you are interested in.

also it can used to track weekly,monthly,yearly of your topic paper that show in google scholarship



## 文献追踪

## 文献下载

## 文献初筛

chatpaper

```
       messages = [
            {"role": "system",
             "content": "You are a researcher in the field of [" + self.key_word + "] who is good at summarizing papers using concise statements"},
            # chatgpt 角色
            {"role": "assistant",
             "content": "This is the <summary> and <Method> part of an English document, where <summary> you have summarized, but the <Methods> part, I need your help to read and summarize the following questions." + clip_text},
            # 背景知识
            {"role": "user", "content": """                 
                 7. Describe in detail the methodological idea of this article. Be sure to use {} answers (proper nouns need to be marked in English). For example, its steps are.
                    - (1):...
                    - (2):...
                    - (3):...
                    - .......
                 Follow the format of the output that follows: 
                 7. Methods: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - (3):xxx;\n  
                    ....... \n\n     
                 
                 Be sure to use {} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not repeat the content of the previous <summary>, the value of the use of the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed, ....... means fill in according to the actual requirements, if not, you can not write.                 
                 """.format(self.language, self.language)},
        ]

        messages = [
            {"role": "system",
             "content": "You are a researcher in the field of [" + self.key_word + "] who is good at summarizing papers using concise statements"},
            {"role": "assistant",
             "content": "This is the title, author, link, abstract and introduction of an English document. I need your help to read and summarize the following questions: " + clip_text},
            {"role": "user", "content": """                 
                 1. Mark the title of the paper (with Chinese translation)
                 2. list all the authors' names (use English)
                 3. mark the first author's affiliation (output {} translation only)                 
                 4. mark the keywords of this article (use English)
                 5. link to the paper, Github code link (if available, fill in Github:None if not)
                 6. summarize according to the following four points.Be sure to use {} answers (proper nouns need to be marked in English)
                    - (1):What is the research background of this article?
                    - (2):What are the past methods? What are the problems with them? Is the approach well motivated?
                    - (3):What is the research methodology proposed in this paper?
                    - (4):On what task and what performance is achieved by the methods in this paper? Can the performance support their goals?
                 Follow the format of the output that follows:                  
                 1. Title: xxx\n\n
                 2. Authors: xxx\n\n
                 3. Affiliation: xxx\n\n                 
                 4. Keywords: xxx\n\n   
                 5. Urls: xxx or xxx , xxx \n\n      
                 6. Summary: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - (3):xxx;\n  
                    - (4):xxx.\n\n     
                 
                 Be sure to use {} answers (proper nouns need to be marked in English), statements as concise and academic as possible, do not have too much repetitive information, numerical values using the original numbers, be sure to strictly follow the format, the corresponding content output to xxx, in accordance with \n line feed.                 
                 """.format(self.language, self.language, self.language)},
```

## 文献翻译

这也是我第一次使用我刚发布的沉浸式双语网页翻译扩展后翻译的第一本英文电子书。首先在离线电子书网站导入 epub 文件，使用扩展翻译后保存为离线 html，再使用 html to epub 工具重新导出为电子书，最后发送到 Kindle 和手机上阅读。

