class FileError(Exception):
    def __init__(self, reason):
        super(FileError, self).__init__(reason)
        self.reason = reason


class FileShouldBeEnglishOnly(Exception):
    def __init__(self, reason):
        super(FileShouldBeEnglishOnly, self).__init__(reason)
        self.reason = reason


class WrongChannelCount(Exception):
    def __init__(self, reason):
        super(WrongChannelCount, self).__init__(reason)
        self.reason = reason
