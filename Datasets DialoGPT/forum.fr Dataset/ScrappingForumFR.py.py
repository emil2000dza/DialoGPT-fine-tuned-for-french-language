import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


def extracting_text(link_of_the_page):
    driver = webdriver.Firefox(executable_path=r'C:\Users\emili\OneDrive\Documents\geckodriver-v0.29.1-win64/geckodriver')
    driver.get(link_of_the_page)
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    elements=soup.findAll(class_= "cPost_contentWrap")
    posts=[]

    for element in elements:
        posts.append(element.get_text())

    posts2=[]
    for text in posts:
        if len(text) > 0 and text[:15] != '................' not in text:
            text = text.replace("\n","")
            text=text.replace("[/Justifier]","")
            text=text.replace("[Justifier]","")
            text=text.replace(":blush","")
            text=text.replace('‼','!')
            text=text.replace("CiterSignalerPartager","")
            text=text.replace("\'","")
            text=text.replace("\xa0'", " ")
            text=text.replace('\U0001f914'," ")
            text=text.replace('\U0001f601',"")
            text=text.replace('\U0001f62c','')
            text=text.replace('\U0001f937', " ")
            text=text.replace('\U0001f43a',"")
            text=text.replace('\u25ba','')
            text=text.replace("\u2009"," ")
            text=text.replace('\U0001f913','')
            text=text.replace('\u0113','')
            posts2.append(text)
            #print(text)
    for i in range(len(posts2[0])-30):
        if posts2[0][i] in ['0','1','2','3','4','5','6','7','8','9'] and posts2[0][i+1] in ['0','1','2','3','4','5','6','7','8','9'] and posts2[0][i+2] == ':' and posts2[0][i+3] in ['0','1','2','3','4','5','6','7','8','9'] and posts2[0][i+4] in ['0','1','2','3','4','5','6','7','8','9']:
            premierpost=posts2[0][i+5:]
            posts2[0]=premierpost
            break
    if len(posts2[0]) > 20:
        for i in range(len(posts2[0])-7,len(posts2[0])-30,-1):
            if posts2[0][i] =='M' and posts2[0][i+1] == 'o' and posts2[0][i+2] == 'd' and posts2[0][i+3] == 'i' and posts2[0][i+4] =='f' and posts2[0][i+5] =='i' and posts2[0][i+6] =="é":
                posts2[0]=posts2[0][:i]
    print(posts2)
    postsfiltered=[]

    for message in posts2:
        if "a dit\xa0:" not in message and message != '':
            print(message)
            postsfiltered.append(message)
            #print(message)
    print(postsfiltered)
    return [link_of_the_page,postsfiltered]

## Obtaining other pages

def pages(link_of_the_page,already_consulted):
    driver = webdriver.Firefox(
        executable_path=r'C:\Users\emili\OneDrive\Documents\geckodriver-v0.29.1-win64/geckodriver')
    driver.get(link_of_the_page)
    content = driver.page_source
    page_links=[]
    soup = BeautifulSoup(content, 'html.parser')
    elements2=soup.findAll('a')
    for element in elements2:
        if element.get('href') != None and "page=" in element.get('href') and element.get('href') not in page_links and element.get('href') not in already_consulted:
            page_links.append(element.get('href'))
    return page_links

def all_messages_from_1_topic(link):
    messages_topic=[]
    already_consulted=[]
    text=extracting_text(link)
    already_consulted.append(link)
    messages_topic.append(text[0])
    for i in text[1]:
        messages_topic.append(i)
    page_list=pages(link,already_consulted)
    for i in range(len(page_list)):
        text=extracting_text(page_list[i])[1]
        already_consulted.append(page_list[i])
        for i in text:
            messages_topic.append(i)
    return messages_topic

def liste_topic(forum_link):
    driver = webdriver.Firefox(
        executable_path=r'C:\Users\emili\OneDrive\Documents\geckodriver-v0.29.1-win64/geckodriver')
    driver.get(forum_link)

    results = []
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')
    elements = soup.findAll('a')
    topics = []

    for element in elements:
        # print(element.get('href'))
        if 'https://www.forumfr.com/sujet' in element.get('href') and 'comments' not in element.get(
                'href') and 'LastComment' not in element.get('href'):
            print(element.get('href'))
            topics.append(element.get('href'))
    return topics

def all_messages_forum(topics):
    all_messages=[]
    for link in topics:
        messages_topic=all_messages_from_1_topic(link)
        all_messages.append(messages_topic)
        fichier = open(r"C:\Users\emili\OneDrive\Documents/Datasets DialoGPT/ForumQuotidien.txt", "a")
        fichier.write('\n')
        fichier.write(str(messages_topic[0] + '\n'))
        for i in range(1, len(messages_topic)):
            fichier.write(str(messages_topic[i]) + '\n')
        fichier.write('\n')
        fichier.close()
    return all_messages


topics=liste_topic('https://www.forumfr.com/f189-actu-et-d%C3%A9bats.html')
print(topics)

all_messages_a_topic=all_messages_from_1_topic(topics[3])

print(all_messages_a_topic)
print(len(all_messages_a_topic))


fichier = open(r"C:\Users\emili\OneDrive\Documents/Datasets DialoGPT/ForumQuotidien.txt", "a")
fichier.write('\n')
fichier.write(str(all_messages_a_topic[0] + '\n'))
for i in range (1,len(all_messages_a_topic)):
    fichier.write(str(all_messages_a_topic[i]) + '\n')
fichier.write('\n')
fichier.close()