from DoubleEntry import double_entry
from IntEntry import int_entry
from FluctuateCheck import fluctuate_check
from Function import function

from settings import MIN_FREQ, MAX_FREQ, MIN_LEVEL, MAX_LEVEL


class FluctuatingValueControl(object):
    def __init__(self, root, row, column):
        self.row = row

        # video
        self.initial_value = int_entry(root, low=0, high=255, row=row, column=column)
        self.low_value = int_entry(root, low=0, high=255, row=row, column=column+1)
        self.high_value = int_entry(root, low=0, high=255, row=row, column=column+2)

        # audio
        self.min_freq_entry = int_entry(root, low=MIN_FREQ, high=MAX_FREQ, row=row, column=column+3)
        self.max_freq_entry = int_entry(root, low=MIN_FREQ, high=MAX_FREQ, row=row, column=column+4)
        self.min_level_entry = double_entry(root, low=MIN_LEVEL, high=MAX_LEVEL, row=row, column=column+5)
        self.max_level_entry = double_entry(root, low=MIN_LEVEL, high=MAX_LEVEL, row=row, column=column+6)

        # activation
        self.function = function(root, row=row, column=column+7)
        self.fluctuate = fluctuate_check(root, row=row, column=column+8)

    def to_dict(self):
        return {
            "initial value": self.initial_value.get_value(),
            "low value": self.low_value.get_value(),
            "high value": self.high_value.get_value(),
            "min freq": self.min_freq_entry.get_value(),
            "max freq": self.max_freq_entry.get_value(),
            "min level": self.min_level_entry.get_value(),
            "max level": self.max_level_entry.get_value(),
            "function": self.function.get_key(),
            "fluctuate": self.fluctuate.get_value(),
        }

    def from_dict(self, data_object):
        self.initial_value.set_value(data_object["initial value"])
        self.low_value.set_value(data_object["low value"])
        self.high_value.set_value(data_object["high value"])
        self.min_freq_entry.set_value(data_object["min freq"])
        self.max_freq_entry.set_value(data_object["max freq"])
        self.min_level_entry.set_value(data_object["min level"])
        self.max_level_entry.set_value(data_object["max level"])
        self.function.set_value(data_object["function"])
        self.fluctuate.set_value(int(data_object["fluctuate"]))
