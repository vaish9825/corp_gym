def get_page_bounds(page, size):
    start = (page - 1) * size
    end = start + size - 1 # BUG: Off by one
    return start, end
