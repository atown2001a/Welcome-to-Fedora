import time
import datetime
import dateutil.relativedelta
import configparser
import requests
from fedora.client.fas2 import AccountSystem
import sys

configfile = 'myconfig.cfg'

config = configparser.ConfigParser()
config.read(configfile)
options = config.options('FAS')
userdata = {}

for opt in options:
    userdata[opt] = config.get('FAS', opt)

user = userdata['user']
password = userdata['pass']

fas = AccountSystem(username=user, password=password)
fas.timeout = 600
fas.retries = 3

activity_baseurl = 'https://apps.fedoraproject.org/datagrepper/raw'


def getactivitycount(username,days):
    days = int(days)
    today = datetime.date.today()
    d = datetime.datetime.strptime(today.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    d = d - dateutil.relativedelta.relativedelta(days=days)
    start = time.mktime(datetime.datetime.strptime(str(d), "%Y-%m-%d %H:%M:%S").timetuple())

    activity_params = {'rows_per_page': 100, 'size': 'small', 'start': start, 'user': username}

    activity_results = requests.get(activity_baseurl, params=activity_params).json()

    pages = activity_results['pages']

    for i in range(0, pages):
        # print("aaaaaaaaaaaaaaaaaa",i)
        activity_params2 = {'page': 1, 'rows_per_page': 100, 'size': 'small', 'start': start, 'user': username}
        activity_results2 = requests.get(activity_baseurl, params=activity_params2).json()

        for j in range(0, len(activity_results2['raw_messages'])):
            # print(j,len(activity_results2['raw_messages']))
            msgdate = datetime.datetime.fromtimestamp(int(activity_results2['raw_messages'][j]['timestamp']))
            topic = activity_results2['raw_messages'][j]['topic']

            print("\t", msgdate, topic)

    return [activity_results['total'], d]


class Groups:

    def __init__(self, groups):
        self.count = 0
        self.role_status = "na"
        for group in groups:

            # self.role_status = groups[group]['role_status']
            # self.approval = groups[group]['approval']
            print("\t", group, groups[group]['role_status'], groups[group]['approval'])
            self.count += 1

    def count_groups(self):
        return self.count


def main(username,days):

    print("Username:", username)
    fas_user = fas.person_by_username(username)
    print("Human name:", fas_user['human_name'])
    last_seen = datetime.datetime.strptime(fas_user['last_seen'], "%Y-%m-%d %H:%M:%S.%f%z").strftime(
        "%Y-%m-%d %H:%M:%S")
    print("Last seen:", last_seen)
    print("Groups:")
    count_groups = Groups(fas_user['group_roles']).count_groups()
    print("Total groups:", count_groups)
    print("Activities:")
    activities = getactivitycount(username, days)
    date = datetime.datetime.strptime(str(activities[1]), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    print("Total activities since {}: {}".format(date, activities[0]))


if __name__ == '__main__':
    usernametocheck = sys.argv[1]
    lastactivitiessincedays = sys.argv[2]
    main(usernametocheck, lastactivitiessincedays)
    print("End")