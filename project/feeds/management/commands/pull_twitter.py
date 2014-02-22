import pprint
import datetime
import dateutil.parser
import logging

from TwitterAPI import TwitterAPI

from django.db.models import Q
from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
import django_settings

from feeds.models import TwitterStream, Tweet

# Log everything, and send it to stderr.
logging.basicConfig(level=logging.DEBUG)

class Command(BaseCommand):

    def handle(self, *args, **options):
        '''For each Team object check their sponsorship
        page and update their record in the database
        '''
        # connect to the API
        if not settings.TWITTER_CONSUMER_KEY:
            raise Exception("There are no Twitter user credentials")

        api = TwitterAPI(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN_KEY,
            settings.TWITTER_ACCESS_TOKEN_SECRET
        )

        streams = TwitterStream.objects.all().filter(
            Q(type=TwitterStream.TWITTER) | Q(type=TwitterStream.TWITTER_LIST)
        )

        for stream in streams:
            logging.debug("Now working on %s" % stream)

            # look up the settings in the database to see where 
            # were we the last time we asked for tweets from Twitter
            since_id = django_settings.get('TWITTER_SINCE_ID_%s' % stream.stream_id, default=1)
            new_since_id = since_id

            print "SINCE:::::: ", since_id

            # make APiI request and check HTTP response
            r = api.request('lists/statuses', 
                    {
                        'list_id': stream.stream_id, 
                        'include_rts': stream.include_rts,
                        'since_id': since_id,
                        'count': 20
                    }
                )
            if r.status_code != 200:
                logging.exception("API Call Failed")
                print dir(r)
                raise Exception("API Call Failed")

            # prcoess tweets
            for tweet in r.get_iterator():

                try:
                    try:
                        tweet['retweeted_status'] # this key is only set on retweets
                        # this is a retweet by our accounts
                        # we care about the original tweet maker not ourselves
                        tweet = tweet['retweeted_status']

                    except KeyError:
                        pass

                    # extract out the media from the entities
                    try:
                        media_url = tweet['entities']['media']['media_url']
                    except:
                        media_url = None

                    # strip the timezone off the timestamp
                    time_tz = dateutil.parser.parse(tweet['created_at'])
                    time = datetime.datetime(time_tz.year, time_tz.month, time_tz.day, time_tz.hour, time_tz.minute, time_tz.second)

                    new_tweet = Tweet.objects.create(
                            tweet_id=tweet['id'],
                            media_url=media_url,
                            message=_html_for_tweet(tweet),
                            time=time,
                            in_reply_to_user_name=tweet['in_reply_to_screen_name'],
                            retweeted=True,
                            user_id=tweet['user']['id'],
                            user_name=tweet['user']['screen_name'],
                            user_photo=tweet['user']['profile_image_url'],
                            team=None
                        )
                    
                    # update the since id so we don't get the same
                    # tweets mutliple times from twitter
                    if new_tweet.tweet_id < new_since_id:
                        new_since_id = new_tweet.tweet_id

                    logging.debug("Created tweet %i" % new_tweet.tweet_id)

                except Exception as e:
                    logging.exception("Failed to process tweet %d" % tweet['id'])

            # update settings datastore with highest tweet id
            django_settings.set('Integer', 'TWITTER_SINCE_ID_%s' % stream.stream_id, new_since_id)

def _html_for_tweet(tweet, use_display_url=True, use_expanded_url=False):
    if 'retweeted_status' in tweet:
            tweet = tweet['retweeted_status']

    if 'entities' in tweet:
        text = tweet['text'].encode("utf-8")
        entities = tweet['entities']

        # Mentions
        for entity in entities['user_mentions']:
            start, end = entity['indices'][0], entity['indices'][1]

            mention_html = '<a href="https://twitter.com/%s" target="_blank">@%s</a>' % (entity['screen_name'], entity['screen_name'])
            text = text.replace(tweet['text'][start:end], mention_html)

        # Hashtags
        for entity in entities['hashtags']:
            start, end = entity['indices'][0], entity['indices'][1]

            hashtag_html = '<a href="https://twitter.com/search?q=%%23%(hashtag)s" target="_blank">#%(hashtag)s</a>'
            text = text.replace(tweet['text'][start:end], hashtag_html % {'hashtag': entity['text']})

        # Urls
        for entity in entities['urls']:
            start, end = entity['indices'][0], entity['indices'][1]
            if use_display_url and entity.get('display_url'):
                shown_url = entity['display_url']
            elif use_expanded_url and entity.get('expanded_url'):
                shown_url = entity['expanded_url']
            else:
                shown_url = entity['url']

            url_html = '<a href="%s" target="_blank">%s</a>'
            text = text.replace(tweet['text'][start:end], url_html % (entity['url'], shown_url))

    return text
