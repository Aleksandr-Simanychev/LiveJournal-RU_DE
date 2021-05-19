import csv
from bs4 import BeautifulSoup
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
Previous_Post = 'https://ru-de.livejournal.com/64938.html'
while True:
    print(Previous_Post)
    browser = webdriver.Chrome(options=options, executable_path=r'/Users/aleksandrsimanychev/Downloads/chromedriver')
    browser.get(url = Previous_Post)
    soup = BeautifulSoup(browser.page_source, 'lxml')
    with open('LJ.csv', 'a') as csvfile:
        fieldnames = ['post', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if '<a class="_w9" href="' in str(soup):
            posts = soup.find_all('div', class_='aentry-post__text aentry-post__text--view')
            comments = soup.find_all('div', class_='mdspost-comment__body')
            Year_Of_Post = str(soup).partition('<time>')[2].partition('</time>')[0]
            Year_Of_Post = '20' + Year_Of_Post.partition('20')[2].partition(', ')[0]
            Previous_Post = str(soup).partition('<a class="_w9" href="')[2].partition('" target')[0]
        else:
            posts = soup.find_all('div', class_='asset-body')
            comments = soup.find_all('div', class_='comment-body j-c-resize-images')
            Year_Of_Post = str(soup).partition('<li class="item"><span><abbr class="datetime">')[2].partition('</abbr></span></li>')[0]
            Year_Of_Post = Year_Of_Post.partition(', ')[2].partition(' ')[0]
            Previous_Post = str(soup).partition('<p class="prevnext"><a href="')[2].partition('" target="_self')[0]
        for post in posts:
            writer.writerow({'post':str(post.text), 'date':Year_Of_Post})
            print(post.text)
        for comment in comments:
            writer.writerow({'post':comment.text, 'date':Year_Of_Post})
            print(comment.text)
        print(Year_Of_Post)
        print(Previous_Post)
        browser.quit()
        if Previous_Post == 'https://ru-de.livejournal.com/260.html':
            break