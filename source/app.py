import random
import os 
import tweepy
from secrets import *
from time import gmtime, strftime

# ====== Individual bot configuration ==========================
bot_username = 'pinegrove_bot'
logfile_name = bot_username + ".log"
# ==============================================================

def compose_tweet():
    """Create the text of the tweet to be sent"""
    # pick a random song
    song_name = get_song()
    
    # build list of lists with verses from song 
    lyrics = []
    with open ("lyrics/" + song_name, "r") as song:
        verse = []
        read_lines = song.readlines()
        for line in read_lines:
            if line != "\n":
                verse.append(line.strip("\n")) 
            else:
                lyrics.append(verse)
                verse = []

  
    if lyrics == []:
        print ("Error occured, lyrics is empty. This is song name")
        print (song_name)
 
    
    '''
    The lyrics array is a list of lists where each 
    individual list is a verse 
    We want to select a random verse, and then random sequential 
    lines for which the total length is less than 140 char
    ''' 
    compose = ""
    char_lim = 140
    num_verse = random.randrange(len(lyrics))
    selected_verse = lyrics[num_verse]
   
    line_count = 0
    while (len(compose)+len(selected_verse[line_count]) < char_lim)\
            and line_count < len(selected_verse):
        if line_count != 0:
            compose += ", "
       compose += selected_verse[line_count]
 
        line_count += 1
   return compose  

def get_song():
    song_names = os.listdir("lyrics/")
    select_song = random.choice(song_names)
    return select_song

def tweet(text):
    """Send out the text as a tweet."""
    # Twitter authentication 
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Send the tweet and log success or failure
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted " + text)
    
def log(message):
    """Log message to logfile"""
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + message)

if __name__ == "__main__":
    tweet_text = compose_tweet()
    tweet(tweet_text)
