import csv


def to_csv(out_file, data, fieldnames=None):
    if fieldnames is None:
        sample = data[0]
        if not isinstance(sample, dict):
            raise Exception("fieldnames cannot be None if data is not a dict.")
        else:
            fieldnames = sample.keys()

    out_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
    out_writer.writeheader()
    out_writer.writerows(data)
