import json


def separateJson():
    redditJson = open("data\\json1.json", 'r', encoding='utf-8')
    data = redditJson.readlines()

    for n, jFile in enumerate(data):
        with open('data\\' + str(n) + '.json', 'w', encoding='utf-8') as target:
            target.write(jFile)


def parseJson(upvoteList, jsonFile):
    readJson = open("data\\" + jsonFile, 'r', encoding='utf-8')
    jFile = json.load(readJson)

    for post in jFile['data']['children']:

        subreddit = post['data']['subreddit']
        title = post['data']['title']
        flair = post['data']['link_flair_css_class']
        try:
            url = post['data']['url_overridden_by_dest']
        except KeyError:
            url = post['data']['url']
        permalink = post['data']['permalink']

        if flair != type(str):
            flair = 'null'

        detailsList = [subreddit, title, flair, url, permalink]
        postDetails = " | ".join(detailsList)

        print(detailsList)
        upvoteList.append(postDetails)


# separateJson()
"""
upvotedList = list()
for x in range(34):
    parseJson(upvotedList, str(x) + '.json')

with open('data\\oldUpvotes.txt', 'w', encoding='utf-8') as target:
    for entry in upvotedList:
        target.write(entry + "\n")
"""

with open('data\\fullUpvoted.txt', 'r', encoding='utf-8') as file, \
        open('data\\fullUpvoted2.txt', 'w', encoding='utf-8') as target:
    readFile = file.readlines()
    for line in readFile:
        newLine = line.replace('|', ' | ')
        target.write(newLine)
