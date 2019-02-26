import praw
import re
import time
import math

errors = 0;


def main():
    reddit = praw.Reddit(client_id='ZIkkm7m7ePhpHQ',
                         client_secret='Q-zbPbonLkm4vl-bHYSpPLVOMfQ',
                         user_agent='<console:the_one_true_red:0.0.1 (by /u/the_one_true_red)>',
                         username='the_one_true_red',
                         password='maroon')
    subreddit_title = 'Showerthoughts'

    subreddit = reddit.subreddit(subreddit_title)
    #for submission in subreddit.new():
        #process_submission(submission, reddit)
    for submission in subreddit.stream.submissions():
        print("new submission")
        process_submission(submission, reddit, subreddit_title)


def process_submission(submission, reddit, subreddit_title):
    if not postedBefore(submission):
        for post in reddit.subreddit(subreddit_title).search(submission.title):
            print("searching...")
            try:
                words_in_title = len(re.sub("[^\w]", " ", submission.title).split())
                if post.id != submission.id and \
                        len(post.comments) > 0 and \
                        words_in_title > 2 and \
                        checkRelevant(submission.title, post.title) > words_in_title-math.log10(math.log10(words_in_title)^2)*1.5 and \
                        post.comments[0].author.name != 'AutoModerator' and \
                        post.created_utc != submission.created_utc:
                    comment = post.comments[0].body

                    print("attempting to post comment")

                    postComment(submission, comment, reddit)

                    break
            except:
                continue




def checkRelevant(newPost, otherPost):
    counter = 0;
    newList = re.sub("[^\w]", " ", newPost).split()
    otherList = re.sub("[^\w]", " ", otherPost).split()

    for word in newList:
        if word in otherList:
            counter = counter+1

    return counter

def postComment(post, comment, reddit):
    global errors
    try:
        edit = comment.lower().find('edit:')
        if(edit != -1):
            comment = comment[:edit]

        post.reply(comment)
        post.upvote()
        print("replying to post: \"", post.title, "\"\n", sep="")
        print(comment)

    except praw.exceptions.APIException as e:
        if (e.error_type == "RATELIMIT"):
            delay = re.search("(\d+) minutes?", e.message)

            if delay:
                delay_seconds = float(int(delay.group(1)) * 60)
                print("waiting", delay_seconds, "seconds...", sep=" ")
                time.sleep(delay_seconds)
                postComment(post, comment, reddit)
            else:
                delay = re.search("(\d+) seconds", e.message)
                delay_seconds = float(int(delay.group(1)))
                print("waiting", delay_seconds, "seconds...", sep=" ")
                time.sleep(delay_seconds)
                postComment(post, comment, reddit)


    except praw.exceptions.ClientException as e:
        print(e.message)
        errors = errors + 1
        if (errors > 5):
            print("crashed")
            exit(1)

    except praw.exceptions.PRAWException as e:
        print(e.message)
        errors = errors + 1
        if (errors > 5):
            print("crashed")
            exit(1)

    except:
        print("other error")
        errors = errors + 1
        if (errors > 5):
            print("crashed")
            exit(1)

def postedBefore(post):
    all_comments = post.comments.list()
    for comment in all_comments:
        try:
            if comment.author.name == 'the_one_true_red':
                return True
        except:
            continue
    return False


def post():
    global subreddits
    global pos
    global errors

    try:
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title, url=url)

        pos = pos+1
        if(pos <= len(subreddits) - 1):
            post()
        else:
            print("Done")
    except praw.exceptions.APIException as e:
        if(e.error_type == "RATELIMIT"):
            delay = re.search("(\d+) minutes?", e.message)

            if delay:
                delay_seconds = float(int(delay.group(1)) * 60)
                time.sleep(delay_seconds)
                post()
            else:
                delay = re.search("(\d+) seconds", e.message)
                delay_seconds = float(int(delay.group(1)))
                time.sleep(delay_seconds)
                post()

    except:
        errors = errors + 1
        if(errors > 5):
            print("crashed")
            exit(1)


main()