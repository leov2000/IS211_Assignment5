class Request:

    def __init__(self, request_item):
        [time_stamp, _, seconds_to_process] = request_item

        self.timestamp = time_stamp
        self.seconds_to_process = seconds_to_process

    def get_stamp(self):
        return self.timestamp

    def get_request(self):
        return self.seconds_to_process

    def wait_time(self, current_time):
        return current_time - self.seconds_to_process
