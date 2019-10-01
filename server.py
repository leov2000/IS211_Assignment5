class Server:
    def __init__(self, host_name=None):
        self.current_req = None
        self.time_remaining = 0
        self.host_name = host_name

    def tick(self):
        if self.current_req != None:
            self.time_remaining = self.time_remaining - 1

        if self.time_remaining <= 0:
            self.current_req = None

    def busy(self):
        if self.current_req != None:
            return True

        else:
            return False


    def start_next(self, new_req):
        self.current_req = new_req
        self.time_remaining = new_req.get_request()
        