# Pranavkumar Mallela
# 2020CSB1112
# import required libraries
import bz2
import re
import random
import pickle
import time


# function to construct the wiki graph
def construct_wiki_graph():
    # openthe file pointer to the wiki dump
    file = bz2.BZ2File("data.bz2")
    # open the binary file where the adjacency list will be stored
    bfile = open('binfile.dat', mode='wb')

    # regex to identify titles and links in the bz2 file
    # titles are in the form <title>TITLE</title>
    # links are in the form [[LINK]]
    title_regex = re.compile(r'(?<=<title>)[\w+ ]+')
    link_regex = re.compile(r'(?<=\[\[)[\w+ ]+(?=\]\])')

    titles = []
    # while the first title is not read, keep searching
    while (len(titles)==0):
        titles = title_regex.findall(str(file.readline()))
    # convert titles to lowercase for uniformity
    title1 = titles[0].lower()
    title2 = title1
    # list to store the links for a particular title
    links=[]
    # offsets will store the line offsets of the binary file for a particular title
    offsets = {}
    # read the file line by line
    for line in file:
        line_links = link_regex.findall(str(line))
        # format the links for uniformity
        line_links = [x.lower().split('|')[0] for x in line_links]
        links += line_links
        title2 = title_regex.search(str(line))
        # enter if a new title is found
        if(title2 and title2.group().lower()!=title1):
            # do not choose titles with less than 10 outgoing links
            if(len(links)<10):
                continue
            # set the line offset for the previous title, and store it using pickle dump
            offsets[title1] = bfile.tell()
            pickle.dump(links, bfile)
            # reset the links list
            links=[]
            title1 = title2.group().lower()
    bfile.close()
    # return the dict containing the line offsets, essentially the adjacency list
    return offsets


#function to perform random walk given the adjacency list as argument
def random_walk(offsets):
    # open the binary file written to in construct_wiki_graph()
    rfile = open('binfile.dat', mode='rb')
    # set starting point as 'the new york times'
    u = 'the new york times'
    # visited will store the number of visits to each page
    visited = {}
    visited[u]=1
    # set probability of teleporting = 0.2
    p=0.2
    # perform 100 million steps in the random walk
    for i in range(100000000):
        # choose a random neighbour
        if(random.random() > 0.2 and u in offsets):
            rfile.seek(offsets[u])
            # load the correct links list using the offset
            rand_list = pickle.load(rfile)
            v = random.choice(rand_list)
        # teleport to any random node with p = 0.2 to avoid getting stuck
        else:
            random_u = random.choice(list(offsets.keys()))
            rfile.seek(offsets[random_u])
            # load the correct links list using the offset
            rand_list = pickle.load(rfile)
            v = random.choice(rand_list)
        # increment the number of visits of node v
        if(v in visited):
            visited[v]+=1
        else:
            visited[v]=1
        u=v
    rfile.close()
    # return the record of number of visits
    return visited

# main function to determine top k wiki pages, takes the argument 'k'
def k_top_pages(k):
    offsets = construct_wiki_graph()
    visited = random_walk(offsets)
    # sort the tuples in visited by value and take the top k elements
    most_visited = sorted(visited.items(), key = lambda x:x[1], reverse=True)[:k]
    # open the file to write the top 25 pages to
    visited_out = open("visited_out.txt", "w")
    for node in most_visited:
        visited_out.write(str(node)+"\n")

# use time library to find total excecution time
start = time.time()
k=25
k_top_pages(k)
end = time.time()
print("Execution time = ", (end-start), "s")
