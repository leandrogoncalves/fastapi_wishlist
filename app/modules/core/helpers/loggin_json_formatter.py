import logging
import json


class LoggingJsonFormatter(logging.Formatter):
    DEFAULT_PARAMS = {
        "level": "levelname",
        "message": "message",
        "loggerName": "name",
        "processName": "processName",
        "processID": "process",
        "threadName": "threadName",
        "threadID": "thread",
        "timestamp": "asctime"
    }
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict fmt_dict: Key: logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string. Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting. Appended at the end. Default: "%s.%03dZ"
    """
    def __init__(
            self,
            fmt_dict: dict = None,
            time_format: str = "%Y-%m-%dT%H:%M:%S",
            msec_format: str = "%s.%03dZ"
    ):
        self.fmt_dict = fmt_dict if fmt_dict is not None else self.DEFAULT_PARAMS
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None

    def usesTime(self) -> bool:
        return "asctime" in self.fmt_dict.values()

    def formatMessage(self,record) -> dict:
        return {fmt_key:record.__dict__[fmt_val] for fmt_key, fmt_val in self.fmt_dict.items()}

    def format(self,record) -> str:
        record.message =record.getMessage()

        if self.usesTime():
            record.asctime =self.formatTime(record,self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        if "extra" in record.__dict__:
            message_dict["extra"] = record.__dict__["extra"]

        output_log = {
            "timestamp_app": message_dict["timestamp"],
            "message": message_dict["message"],
            "log_level": message_dict["level"],
            "log_type": "Application" if not "log_type" in message_dict else message_dict["log_type"],
            "event": {
                "pathname":record.pathname,
                "line_number":record.lineno,
                "filename":record.filename,
                "context": message_dict
            },
        }


        return json.dumps(output_log, default=str)
