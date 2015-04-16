class Strategy:
    def prepare(self):
        raise NotImplementedError()

    def choose_action(self):
        raise NotImplementedError()
