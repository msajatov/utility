class Sample:

    def __init__(self, name, source_file_name, cut, target, event_weight, weight):
        self.name = name
        self.source_file_name = source_file_name
        self.full_path = ""
        self.cut = cut
        self.target = target
        self.event_weight = event_weight
        self.eff_weight = weight

    def get_name(self):
        return self.name

    def __str__(self):
        result = ""
        result += "[Sample: " + "\n"
        result += "Name: " + self.name + "\n"
        result += "Source: " + self.source_file_name + "\n"
        result += "Source Path: " + self.source_file_name + "\n"
        result += "Cut Alias: " + self.cut.original + "\n"
        result += "Cut: " + self.cut.get() + "\n"
        result += "Target: " + str(self.target) + "\n"
        result += "Event Weight: " + str(self.event_weight) + "]" + "\n"
        result += "Effective Weight: " + str(self.eff_weight) + "]" + "\n"
        return result
