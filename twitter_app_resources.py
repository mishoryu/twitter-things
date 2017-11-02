""" twitter api app resources using tweepy wrapper. """

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import argparse
import tweepy
import prettytable

def get_app_resources(tweepy_api):
    try:
        api_rate_limits = tweepy_api.rate_limit_status()

    except tweepy.TweepError as err:
        print "tweepy_api.rate_limit_status error: " + str(err.message)
        sys.exit()

    return api_rate_limits

def format_resource_row(resource_name, reset_time, resource_limit, resource_remaining):
    utc_time = datetime.datetime.utcfromtimestamp(reset_time)
    reset_time = utc_time.strftime("%Y-%m-%d %H:%M:%S UTC")

    return [str(resource_name), reset_time, str(resource_limit), str(resource_remaining)]

def print_app_resources(tweepy_api, all_resources=False):
    """ prints a table of app resource information. """

    api_rate_limits = get_app_resources(tweepy_api)

    rate_limits_table = prettytable.PrettyTable(["twitter api resource", "reset", "limit", "remaining"])
    rate_limits_table.align = "l"

    for attr, value in api_rate_limits['resources'].iteritems():
        for sattr, svalue in api_rate_limits['resources'][attr].iteritems():

            if not all_resources:
                # only print resources that have been used (not full)
                if svalue['limit'] != svalue['remaining']:
                    rate_limits_table.add_row(format_resource_row(sattr, svalue['reset'], svalue['limit'],
                                                                  svalue['remaining']))
            else:
                rate_limits_table.add_row(format_resource_row(sattr, svalue['reset'], svalue['limit'],
                                                              svalue['remaining']))

    print rate_limits_table

def get_arguments():
    parser = argparse.ArgumentParser(description='print twitter app api resource usage.')
    parser.add_argument('-a', '--all', help="print list of all resources even if unused", \
                         required=False, action='store_true')

    args = parser.parse_args()

    return args

def main():
    app_consumer_key = os.environ.get('TWITTER_CONSUMER_KEY', 'None')
    app_consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET', 'None')
    app_access_key = os.environ.get('TWITTER_ACCESS_KEY', 'None')
    app_access_secret = os.environ.get('TWITTER_ACCESS_SECRET', 'None')

    user_args = get_arguments()

    try:
        auth = tweepy.OAuthHandler(app_consumer_key, app_consumer_secret)
        auth.set_access_token(app_access_key, app_access_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,
                         compression=True)

    except tweepy.TweepError as err:
        print "tweepy.get_user error: " + str(err.message)
        sys.exit()

    print_app_resources(api, user_args.all)

if __name__ == '__main__':
    main()
