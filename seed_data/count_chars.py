def url_counts(path):
    
    file = open(path)

    for line in file:
        line = line.rstrip()
        item = line.split('|')
        url = len(item[4])
        title = len(item[1])
        print("{}: url, {}: title.".format(url, title))

       
    file.close()


url_counts("u.item")  


