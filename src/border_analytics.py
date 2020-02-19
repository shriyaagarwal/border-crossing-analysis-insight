from datetime import datetime


class Record:
    """
    Class for records - Used to standard implementation which can be reused
    
    """
    def __init__(self, port_name, state, port_code, border, date, measure, value):
        self.port_name = port_name
        self.state = state
        self.port_code = port_code
        self.border = border
        self.date = date
        self.measure = measure
        self.value = int(value)

    def __str__(self):
        return ", ".join([str(val) for val in self.__dict__.values()])


def read_file(file_path):
    """
    Read the given file
    Returns 
    - header : The headers for the table
    - data : Nested dictionary of record objects
    """
    input_file = open(file_path)
    headers = input_file.readline().strip().split(",")
    lines = input_file.readlines()
    data = {}
    for line in lines:
        record_raw = line.strip().split(",")
        record = Record(record_raw[0], record_raw[1], record_raw[2], record_raw[3], record_raw[4], record_raw[5],
                        record_raw[6])
        if record.border not in data:
            data[record.border] = {}
        if record.measure not in data[record.border]:
            data[record.border][record.measure] = {}
        data[record.border][record.measure][record.date] = data[record.border][record.measure].get(record.date, []) + [record]
    return headers, data


if __name__ == '__main__':
    """
    Main function with aggregations used
    """
    headers, data = read_file("../input/Border_Crossing_Entry_Data.csv")
    out_file = open("../output/report.csv", "w")

    ### Aggregate and write to file
    for border in data.keys():
        for type_ in data[border].keys():
            dates = data[border][type_].keys()
            dates = [datetime.strptime(date, "%m/%d/%Y %H:%M:%S %p") for date in dates]
            dates.sort()
            running_avg = 0
            n = 1
            for date in dates:
                records = data[border][type_][date.strftime("%m/%d/%Y %H:%M:%S") + " AM"]
                sum_ = 0
                for record in records:
                    sum_ += record.value
                out_file.write(border + "," + date.strftime("%m/%d/%Y %H:%M:%S") + " AM" + "," + type_ + "," + str(sum_) + "," + str(running_avg) + "\n")
                running_avg = (running_avg*(n-1) + sum_)//n
                n += 1
