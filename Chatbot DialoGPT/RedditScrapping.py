import praw
from praw.models import MoreComments
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


reddit = praw.Reddit(
    client_id="Ij3g665KjrZLew",
    client_secret="aWEtDM8Y855CGkm34NqGWvBedpGdnQ",
    user_agent="android:com.Example.myredditapp:v1.2.3 (by u/Key_Bench_3896)",
)

subs = reddit.subreddit("Frenchbulldogs").hot(limit=5) # name of the sub used for the scrapping and number of recent topics
final=[]
results=[]
ids=[]
parent_ids=[]

for submission in subs :
    submission.comments.replace_more(limit=None)
    comment_queue = submission.comments[:]  # Seed with top-level
    while comment_queue:
        comment = comment_queue.pop(0)
        results.append([comment.body,comment.id,comment.parent_id[3:],comment.score,submission.title]) # small selection of useful data for the processing
        comment_queue.extend(comment.replies)
    final.append(results)
    results=[]

print(final) # all the comments from the top-5 subs are displayed but are organized with top comments first and comments to comments then

ids=[]
delet=[]

for k in range (len(final)):
    for i, e in reversed(list(enumerate(final[k]))):
        for j in range(len(final[k])-1):
            if final[k][i][2] == final[k][j][1]: # if parent_id of j is equal to comment id of i we update the final list
                final[k][i].append(final[k][j])
                delet.append(final[k][j]) # we store the parent of the message in a list to delete it after in order to have one version of each message in the final file, we want to focus on the discussions in the thread

    print(final)
    print(delet)

    for i in delet:
        if i in final[k]:
            indice=final[k].index(i)
            del final[k][indice] # deletion of messages which have children and appear already in the file

print(final)
#final=[final[i][j][0] for i in range(len(final)) for j in range(len(final[0]))]

def depthCount(x):
    return 1 + max(map(depthCount, x)) if x and isinstance(x, list) else 0 # since we append the children on the parent we want to know the number of children of a message, thus we compute it by the depth of the list

# here we compute the number of replies + 1 of every stored comments
number_of_replies_for_the_subs=[]
number_of_replies_for_a_sub=[]
for k in range(len(final)):
    for i in range(len(final[k])):
        number_of_replies_for_a_sub.append(depthCount(final[k][i]))
    number_of_replies_for_the_subs.append(number_of_replies_for_a_sub)
    number_of_replies_for_a_sub=[]

print(number_of_replies_for_the_subs)

topics_dict = {"title": [], "score": [], "comment": [], "context1": [], \
               "context2": [], "context3": [], "context4": [], "context5": []}
# we store the parents as the context of every message
for k in range(len(final)):
    for i in range(len(final[k])):
        if number_of_replies_for_the_subs[k][i] == 1:
            topics_dict["title"].append(final[k][i][4])
            topics_dict["score"].append(final[k][i][3])
            topics_dict["comment"].append(final[k][i][0])
            for i in range(1,6):
                topics_dict["context" + str(i)].append(None)
        elif number_of_replies_for_the_subs[k][i] == 2:
            topics_dict["title"].append(final[k][i][4])
            topics_dict["score"].append(final[k][i][3])
            topics_dict["comment"].append(final[k][i][0])
            topics_dict["context1"].append(final[k][i][5][0])
            for i in range(2, 6):
                topics_dict["context" + str(i)].append(None)
        elif number_of_replies_for_the_subs[k][i] == 3:
            topics_dict["title"].append(final[k][i][4])
            topics_dict["score"].append(final[k][i][3])
            topics_dict["comment"].append(final[k][i][0])
            topics_dict["context1"].append(final[k][i][5][0])
            topics_dict["context2"].append(final[k][i][5][5][0])
            for i in range(3, 6):
                topics_dict["context" + str(i)].append(None)
        elif number_of_replies_for_the_subs[k][i] == 4:
            topics_dict["title"].append(final[k][i][4])
            topics_dict["score"].append(final[k][i][3])
            topics_dict["comment"].append(final[k][i][0])
            topics_dict["context1"].append(final[k][i][5][0])
            topics_dict["context2"].append(final[k][i][5][5][0])
            topics_dict["context3"].append(final[k][i][5][5][5][0])
            for i in range(4, 6):
                topics_dict["context" + str(i)].append(None)
        elif number_of_replies_for_the_subs[k][i] == 5:
            topics_dict["title"].append(final[k][i][4])
            topics_dict["score"].append(final[k][i][3])
            topics_dict["comment"].append(final[k][i][0])
            topics_dict["context1"].append(final[k][i][5][0])
            topics_dict["context2"].append(final[k][i][5][5][0])
            topics_dict["context3"].append(final[k][i][5][5][5][0])
            topics_dict["context4"].append(final[k][i][5][5][5][5][0])
            topics_dict["context5"].append(None)
        elif number_of_replies_for_the_subs[k][i] == 6:
            topics_dict["title"].append(final[k][i][4])
            topics_dict["score"].append(final[k][i][3])
            topics_dict["comment"].append(final[k][i][0])
            topics_dict["context1"].append(final[k][i][5][0])
            topics_dict["context2"].append(final[k][i][5][5][0])
            topics_dict["context3"].append(final[k][i][5][5][5][0])
            topics_dict["context4"].append(final[k][i][5][5][5][5][0])
            topics_dict["context5"].append(final[k][i][5][5][5][5][5][0])
        else:
            topics_dict["title"].append(None)
            topics_dict["score"].append(None)
            topics_dict["comment"].append(None)
            topics_dict["context1"].append(None)
            topics_dict["context2"].append(None)
            topics_dict["context3"].append(None)
            topics_dict["context4"].append(None)
            topics_dict["context5"].append(None)

topics_data = pd.DataFrame(topics_dict)
topics_data.head(10)
topics_data.to_csv('Test1.csv', index=False)