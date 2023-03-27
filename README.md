# CS522-PageRank

construct_wiki_graph():
> This function constructs the wiki graph from the wiki dump file
> I used 'pickle' to store the huge graph efficiently
> for each title, I stored the line offset in the pickle file, instead of the entire list of outgoing links
> I did not allow titles with less than 10 outgoing links
> Return value is the dict containing the line offsets

random_walk(offsets):
> This function performs a random walk on the above constructed graph
> The one argument is the dict of offsets obtained from the above function
> The starting point was taken as 'the new york times' as it was observed to be the top page in the 200MB wiki dump file
> Random walk is performed over 100 million steps
> Teleportation is possible with p = 0.2
> In order to choose a random outgoing link, the binary file containing the lists of links is loaded into memory
> Each title only loads its corresponding list, which makes the operations efficient
> Return value is the dict containing the number of visits of each title

k_top_pages(k):
> This is the main function that computes the top k wiki pages
> Calls the above 2 functions to compute the visited dictionary
> Uses a simple lambda function to sort the items by number of visits
> Top k pages are written to a file 'visited_out.txt'

Note: The time library was used to find the total execution time in seconds.

Result: (took 9560s or 159 minutes)
These are the top 25 pages:
1.'the new york times'
2.'united states'
3.'world war ii'
4.'julian calendar'
5.'list of sovereign states'
6.'telecommunication'
7.'rome'
8.'oxford university press'
9.'catholic church'
10.'anno domini'
11.'calendar era'
12.'latin'
13.'the guardian'
14.'world war i'
15.'cambridge university press'
16.'france'
17.'automated alice'
18.'soviet union'
19.'japan'
20.'wikidata'
21.'italy'
22.'european union'
23.'united nations'
24.'london'
25.'india'

Observations:
> Even after running a random walk multiple times, the top pages remained almost constant, thus enforcing that random walk can be used to find page rank.
> Working on the wiki dump without 'pickle' will cause one's computer to crash. Pickle is necessary to work on very huge graphs.
