import time, datetime, tweepy

from pymongo import Connection
from random import choice

db = Connection()['crowdwoo']

# user queries

def get_all_people():
    return list(db.users.find())


def select_winners(users):
    
    winners = list()
    
    for x in range(0, 3):
        winner = choice(users)
        winners.append(winner)
        users.remove(winner)
        
    return winners


def follow_winners(losers, winners):
    
    while losers:
        
        # next in line
        loser = losers.pop()
        
        text_file = open('already_done', "r")
        lines = [line.rstrip() for line in text_file.readlines()]
        text_file.close()
        
        # just in case we have to run this multiple times, skip people already modified
        if loser['twitter_handle'] in lines:
            print 'skipping %s' % (loser['twitter_handle'])
        
        else:
        
            # make note of using this person
            with open('already_done', 'a') as f:
                f.write('%s\n' % (loser['twitter_handle']))
            
            print 'Requesting that %s follow %s, %s and %s.' % (loser['twitter_handle'], winners[0]['twitter_handle'], winners[1]['twitter_handle'], winners[2]['twitter_handle'])
            print '%d losers left, at %s.' % (len(losers), datetime.datetime.now())
            
            try:
                # auth as this user
                auth = tweepy.OAuthHandler('foo', 'bar')
                auth.set_access_token(loser['oauth_token'], loser['oauth_token_secret'])
                api = tweepy.API(auth_handler=auth)
                
                # follow the winners
                for x in range(0, 3):
                    
                    followed = api.create_friendship(user_id=winners[x]['twitter_id'], follow=False)
                    
                    if followed:
                        print '%s now follows %s.' % (loser['twitter_handle'], winners[x]['twitter_handle'])
                        followed = None
                    else:
                        print 'error: %s cant follow %s.' % (loser['twitter_handle'], winners[x]['twitter_handle'])
                        
            except Exception as e:
                print e
            
            # sleep just because twitter dislikes spam it looks like
            time.sleep(7)

# get all of the people in the lottery
all_people = get_all_people()

# select the three winners
winners = select_winners(all_people)

# losers follow the winners
follow_winners(all_people, winners)

print 'done'