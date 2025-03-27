def read_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def append_to_csv(file_path, row):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        writer.writerow(row)