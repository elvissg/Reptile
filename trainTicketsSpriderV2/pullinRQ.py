# /bin/env python
# -*- coding:utf-8 -*-
from redis import Redis
from rq import Queue
import sys
from trainTicketsSprider import getandsend
from ConfigParser import ConfigParser

class pullinRQ:
    def __init__(self):
        self.r = Redis(host="127.0.0.1", port=6379, db=0)
        self.parse = ConfigParser()
        self.parse.read('email.conf')

    def append_rq_que(self, func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject): 
        q = Queue(connection=Redis()) 
        result = q.enqueue( 
          func, purpose_codes, querydate, from_station, to_station, smtpserver, sender, receiver, username, password, subject 
        )

    def getandpullin(self,times):
        res = self.r.zrange('email_que_set_' + times, 0 , -1)
        reslist = []
        for y in res:
            reslist.append(eval(y))

        for args in reslist:
            purpose_codes = args['purpose_codes']
            querydate = args['querydate']
            from_station = args['from_station']
            to_station = args['to_station']
            receiver =  args['receiver']
            self.append_rq_que(getandsend, purpose_codes, querydate, from_station, to_station , self.parse.get("email", "smtpserver"), self.parse.get("email", "sender"), receiver, self.parse.get("email", "username"), self.parse.get("email", "password"), self.parse.get("email", "subject"))

cron = pullinRQ()
cron.getandpullin(sys.argv[1])