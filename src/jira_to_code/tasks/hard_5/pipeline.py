def process_logs(file_obj):
    lines = file_obj.readlines()
    return [l.strip() for l in lines]
