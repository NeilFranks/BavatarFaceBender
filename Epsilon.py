from FluctuatingValueControl import FluctuatingValueControl


class epsilon(object):
    def __init__(self, root, row, column):
        self.value = FluctuatingValueControl(root, row=row, column=column+1)

    def to_dict(self):
        return {
            "value": self.value.to_dict(),
        }

    def from_dict(self, data_object):
        self.value.from_dict(data_object["value"])
