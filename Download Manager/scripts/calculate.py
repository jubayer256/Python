def file_size_string(size):
    if size < 1024 * 1024:
        return str(round(size/1024, 2)) + " KB"
    if size < 1024 * 1024 * 1024:
        return str(round(size/(1024*1024), 2)) + " MB"
    else:
        return str(round(size/(1024*1024*1024), 2)) + " GB"


def downloaded_size(downloaded, file_size):
    percentage = round((downloaded/file_size)*100, 2)
    if downloaded < 1024*1024:
        return str(round(downloaded/1024, 2)) + " KB ({} %)".format(percentage)
    if downloaded < 1024*1024*1024:
        return str(round(downloaded/(1024*1024), 2)) + " MB ({} %)".format(percentage)
    else:
        return str(round(downloaded/(1024*1024*1024), 2)) + " GB ({} %)".format(percentage)


def download_speed(c, t):
    if c/t < 1024*1024:
        return str(round((c/t)/1024, 2)) + " KB/sec"
    if c/t < 1024*1024*1024:
        return str(round((c/t)/(1024*1024), 2)) + " MB/sec"
    else:
        return str(round((c/t)/(1024*1024*1024), 2)) + " GB/sec"

