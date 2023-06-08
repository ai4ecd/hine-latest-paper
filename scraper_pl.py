import os.path
import random
import asyncio

from playwright.sync_api import sync_playwright
from random import randint
from time import sleep
import pickle
import re
from recaptcha_challenger import new_audio_solver


async def main():
    filename = 'journal-list.txt'
    filename = 'keywords-list.txt'

    with open(filename, 'r') as file:
        top_journals = file.readlines()
    proxy_server = 'socks5://127.0.0.1:1080'

    # Launch Playwright
    async with sync_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(proxy=proxy_server)
        
        page = await context.new_page()

        def build_keyword_url(keyword):
            keyword_split = keyword.strip()
            key_str = keyword_split
            return key_str

        def build_url(journal_name, start_seq):
            journal_split = journal_name.strip().split(' ')
            url = "https://scholar.google.com/scholar?start=" + str(start_seq) + "&q=source:" + journal_split[0].strip()
            if len(journal_split) >= 1:
                for split in journal_split[1:]:
                    url += '+source:' + split.strip()
            url += "&as_vis=1"
            return url

        def build_keys(journal_name):
            journal_split = journal_name.strip().split(' ')
            key_str = ''
            for split in journal_split:
                key_str += 'source:' + split + " "
            return key_str

        # high frequency random mouse walk.
        def random_mouse_walk():
            for i in range(10):
                page.mouse.move_by(randint(-20, 20), randint(-20, 20))
                sleep(random.uniform(0, 0.1))

        def scroll_down():
            page.evaluate("window.scrollBy(0, {});".format(randint(0, 1000)))

        def scroll_up():
            page.evaluate("window.scrollBy(0, {});".format(randint(-1000, 0)))

        def random_user_action():
            for i in range(10):
                roll = random.uniform(0, 1)
                if roll > 0.5:
                    random_mouse_walk()
                else:
                    if roll > 0.75:
                        scroll_up()
                    else:
                        scroll_down()

        def move_to_element(element):
            # Mock human interactive move to the element
            random_mouse_walk()
            element.scroll_into_view_if_needed()
            sleep(0.5)

        def check_for_bot():
            # Check if there is a human check in the page!
            html = page.content()
            match = re.search(r'recaptcha', html)
            if match:
                return True
            else:
                return False

        def fuck_reCAPTCHA():
            print("请完成人机身份验证，验证后请输入任何字符以继续")
            # Implement the reCAPTCHA solving logic here
            solver = new_audio_solver()
            if solver.utils.face_the_checkbox(page):
                solver.anti_recaptcha(page)
            return solver.response
        paper_store = []
        file_idx = 0
        while True:
            if os.path.exists(str(file_idx) + '.pickle'):
                file_idx += 1
            else:
                break
        print("History db found, start from " + str(file_idx) + '.pickle')

        total_cnt = 0

        start_year = 1990
        end_year = 2023
        if not os.path.exists(filename + '-log'):
            with open(filename + "-log", "w") as file:
                file.writelines("")

        with open(filename + '-log', 'r') as file:
            output = file.readlines()
            if len(output) == 2:
                check_journal = output[0]
                check_year = int(output[1])
                finished_journal = True
            else:
                finished_journal = False

        for journal in top_journals[:]:
            cur_year = start_year

            if (finished_journal == True) and (journal.strip() != check_journal.strip()):
                continue

            while cur_year <= end_year:
                if (finished_journal == True) and cur_year < check_year:
                    cur_year += 1
                    continue
                elif (finished_journal == True) and cur_year == check_year:
                    finished_journal = False
                    cur_year += 1
                    continue

                await page.goto("https://scholar.google.com")
                await asyncio.sleep(5)

                if check_for_bot():
                    fuck_reCAPTCHA()

                search_box = await page.wait_for_selector('name=q')
                move_to_element(search_box)
                if 'key' in filename:
                    await search_box.fill(build_keyword_url(journal))
                else:
                    await search_box.fill(build_keys(journal))

                await search_box.press('Enter')
                await asyncio.sleep(5)
                random_user_action()

                if check_for_bot():
                    fuck_reCAPTCHA()

                # exclude citation:
                sidebar = await page.wait_for_selector('#gs_bdy_sb')
                exclude_citation = await sidebar.query_selector_all('.gs_lbl')
                move_to_element(exclude_citation[2])
                await exclude_citation[2].click()
                await asyncio.sleep(5)

                if check_for_bot():
                    fuck_reCAPTCHA()

                # advance search!
                custom_range = await page.wait_for_selector('#gs_res_sb_yyc')
                move_to_element(custom_range)
                await custom_range.click()
                await asyncio.sleep(random.uniform(0.1, 0.5))
                sidebar = await page.wait_for_selector('#gs_bdy_sb')
                input_1 = await sidebar.wait_for_selector('name=as_ylo')
                move_to_element(input_1)
                await input_1.fill(str(cur_year))
                input_2 = await sidebar.wait_for_selector('name=as_yhi')
                move_to_element(input_2)
                await input_2.fill(str(cur_year))
                search_btn = await sidebar.wait_for_selector('.gs_btn_lsb')
                move_to_element(search_btn)
                await search_btn.click()
                await asyncio.sleep(5)

                if check_for_bot():
                    fuck_reCAPTCHA()

                while True:
                    if check_for_bot():
                        fuck_reCAPTCHA()

                    papers = await page.query_selector_all('.gs_r.gs_or.gs_scl')
                    for paper in papers:
                        title = await paper.query_selector('.gs_rt')
                        title = await title.text_content()
                        try:
                            url2 = await paper.query_selector('.gs_rt')
                            url2 = await url2.query_selector('a[href]')
                            url2 = await url2.get_attribute("href")
                        except:
                            url2 = ''

                        try:
                            citation = await paper.query_selector('.gs_ri')
                            citation = await citation.query_selector('.gs_fl')
                            citation = await citation.query_selector_all('xpath=./div')
                            match = re.match("\s*[^0-9]*\s*(\d*)", await citation[2].text_content())
                            citation = eval(match.group(1))
                        except:
                            citation = 0

                        date = cur_year

                        try:
                            url1 = await paper.query_selector('.gs_or_ggsm')
                            url1 = await url1.query_selector_all('xpath=./div')
                            url1 = await url1[0].get_attribute("href")
                        except:
                            url1 = ''

                        paper_store.append({
                            'journal': journal,
                            'title': title,
                            'citation': citation,
                            'date': date,
                            'url1': url1,
                            'url2': url2,
                        })
                        total_cnt += 1

                        if len(paper_store) >= 100:
                            print("Scraped " + str(total_cnt) + " papers.")
                            with open(str(file_idx) + '.pickle', 'wb') as file:
                                pickle.dump(paper_store, file)

                            paper_store = []
                            file_idx += 1

                            await asyncio.sleep(randint(5, 15))

                    # GOTO next. if no next is found. complete!
                    for i in range(3):
                        await scroll_down()

                    await asyncio.sleep(randint(10, 30))

                    try:
                        next = await page.query_selector('#gs_n')
                        next = await next.query_selector('[align="left"]')
                        son = await next.query_selector('xpath=./div')
                        if await son.get_attribute("href"):
                            move_to_element(next)
                            await next.click()
                        else:
                            # end here!
                            print("Year " + str(cur_year) + " of " + journal + "is completed.")
                            with open(filename + "-log", "w") as file:
                                file.writelines([journal, str(cur_year)])
                            break
                    except:
                        print("Year " + str(cur_year) + " of " + journal + "is completed.")
                        with open(filename + "-log", "w") as file:
                            file.writelines([journal, str(cur_year)])
                        break

                cur_year += 1

    # flush.
    with open(str(file_idx) + '.pickle', 'wb') as file:
        pickle.dump(paper_store, file)

    paper_store = []
    file_idx += 1

# Run the main function
asyncio.run(main())
