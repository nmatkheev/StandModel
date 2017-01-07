import logging


class DelegateFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if "submit" in msg.lower() or "extract" in msg.lower():
            return True
        else:
            return False


class RestOfFilter(logging.Filter):
    def filter(self, record):
        msg = record.getMessage()
        if not ("submit" in msg.lower() or "extract" in msg.lower()):
            return True
        else:
            return False
