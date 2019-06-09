#!/usr/bin/python
__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2019 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"

import time
import logging
import os
from beem import Steem
from beem.account import Account
from beem.rc import RC
import time


MINIMUN_MANA_IN_G_RC = 80000
CREATOR_ACCOUNT = "cervantes"

def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO
):
    """Setup logging configuration

    """
    path = default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def claim_account(steemd_instance, logger):

        account = Account(CREATOR_ACCOUNT, steem_instance = steemd_instance)
        rc_mana_old = account.get_rc_manabar()
        rc_mana_old_grc = rc_mana_old["current_mana"] / 1e9
        logger.info("Current_mana: %f" % rc_mana_old_grc)
        if(rc_mana_old_grc>MINIMUN_MANA_IN_G_RC):
            #print("rc_mana_old: %f G RC" % (rc_mana_old["current_mana"] / 1e9))
            steemd_instance.claim_account(creator=CREATOR_ACCOUNT, fee=None)      
            time.sleep(5)
            rc_mana_new = account.get_rc_manabar()
            logger.info("rc_mana_new: %f G RC" % (rc_mana_new["current_mana"] / 1e9))
            rc_costs = rc_mana_old["current_mana"] - rc_mana_new["current_mana"]
            logger.info("RC costs: %f G RC" % (rc_costs / 1e9))
            steemd_instance.claim_account(creator=CREATOR_ACCOUNT, fee=None)
        else:
            logger.info("Skiping claiming account, current manana of %f lower than the set limit of %f" % (rc_mana_old_grc, MINIMUN_MANA_IN_G_RC))
            time.sleep(5)

def create_claimed_account(steemd_instance, account_name, password):

    steemd_instance.create_claimed_account(account_name, creator = CREATOR_ACCOUNT, password = password)
    time.sleep(10)
    new_account = Account(account_name)
    new_account.print_info()

def claim_account_deamon(steemd_instance, logger):

    while True:
        logger.info("Claiming Account...")
        claim_account(steemd_instance, logger)

if __name__ == '__main__':

    setup_logging("./logging.json")
    logger = logging.getLogger()
    stm = Steem("https://api.steemit.com")
    claim_account_deamon(stm, logger)

