import logging


class DelegateFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "type" in msg.lower():
            return True
        else:
            return False


class RestOfFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if not ("type" in msg.lower()):
            return True
        else:
            return False
