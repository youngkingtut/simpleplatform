__author__ = 'Robert P. Cope; Tristan Q. Storz; Charles A. Parker'

from game import StateHandler
import logging
root_logger = logging.getLogger('')
ch = logging.StreamHandler()
root_logger.addHandler(ch)
root_logger.setLevel(logging.INFO)

#TODO: Should write up a design document or graph or something to 
#      help guide further development.

#TODO: Do we need argparse?  Yes. Yes, we need argparse.  Maybe
#      use it to pass in the mode of execution... maybe just use
#      it to select which GameConfig we want to execute with?

g = StateHandler()
try:
    g.setup()
    g.run_game()
except Exception as e:
    root_logger.exception('Faulted during game execution.')
    raise e
finally:
    g.teardown()