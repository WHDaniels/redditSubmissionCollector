import praw.models

# get credentials from ini
reddit = praw.Reddit()
authUser = reddit.user.me()


def upvotedPostPopulate():
    """
    Populates a list of the most recent 1000 upvoted posts from the user.
    :return: A formatted list posts.
    """
    upvoted = authUser.upvoted(limit=None)

    upvotedList = list()
    print("-- Upvoted posts --")

    for post in upvoted:
        detailsList = [str(post.subreddit), str(post.title), str(post.link_flair_text), str(post.url),
                       "reddit.com" + str(post.permalink)]
        postDetails = " | ".join(detailsList)
        print(post.subreddit, post.title, post.link_flair_text, post.url)

        upvotedList.append(postDetails)
    return upvotedList


def savePostPopulate():
    """
    Populates a list of the most recent 1000 saved posts and comments from the user.
    :return: A formatted list posts and comments, respectively.
    """
    saved = authUser.saved(limit=None)

    savedList = list()
    savedCommentList = list()
    print("-- Saved posts --")

    for post in saved:

        if isinstance(post, praw.models.Submission):
            detailsList = [str(post.subreddit), str(post.title), str(post.url), "reddit.com" + str(post.permalink)]
            postDetails = " | ".join(detailsList)
            print(post.subreddit, post.title, post.url)

            savedList.append(postDetails)

        if isinstance(post, praw.models.Comment):
            detailsList = [str(post.subreddit), "reddit.com" + str(post.permalink)]
            postDetails = " | ".join(detailsList)
            print(post.subreddit, post.permalink)

            savedCommentList.append(postDetails)

    return savedList, savedCommentList


def appendToFile(prevList, writeFile):
    """
    Appends a list of formatted post details to the top of a specific file.
    :param prevList: List of formatted posts details.
    :param writeFile: File one wants to append to.
    :return: 
    """
    newUpvotes = list()

    with open(writeFile, 'r', encoding='utf-8') as rTarget:
        readTarget = rTarget.readlines()

        firstEntry = readTarget[0]

        # Lets select only the upvoted post which I haven't saved yet
        for n, line in enumerate(prevList):
            if line != firstEntry.strip("\n"):
                print("New post found! Appending...")
                newUpvotes.append(line)
            else:
                print("This post has already been downloaded: ", firstEntry)
                # If the old post list and the new one start to match, stop the method
                secondCheck, thirdCheck = readTarget[1].strip("\n"), readTarget[2].strip("\n")
                if secondCheck == prevList[n + 1] and thirdCheck == prevList[n + 2]:
                    print("3 consecutive similar posts, breaking")
                    break

    with open(writeFile, 'r+', encoding='utf-8') as aTarget:
        readTarget = aTarget.read()
        aTarget.seek(0)

        for entry in newUpvotes:
            aTarget.write(entry + "\n")
        aTarget.write(readTarget)


if __name__ == "__main__":
    appendToFile(upvotedPostPopulate(), "data\\upvoted.txt")
    appendToFile(savePostPopulate()[0], 'data\\savedPosts.txt')
    appendToFile(savePostPopulate()[1], 'data\\savedComments.txt')
