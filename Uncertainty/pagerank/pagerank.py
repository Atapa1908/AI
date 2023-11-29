import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    total_pages = len(corpus.keys())
    links_at_page = len(corpus[page])

    transition_dict = dict()
    for linked_page in corpus:
        if linked_page in corpus[page]:
            probability = damping_factor * (1/links_at_page) + (1 - damping_factor) / total_pages
            transition_dict[linked_page] = probability
        else:
            probability = (1 - damping_factor) / total_pages
            transition_dict[linked_page] = probability

    return transition_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_dict = {key: 0 for key in corpus.keys()}
    state = random.choice(list(corpus.keys()))
    pagerank_dict[state] += 1
    count = 1

    while count < n:
        pages = list(transition_model(corpus, state, damping_factor).keys())
        transition_prob = list(transition_model(corpus, state, damping_factor).values())
        state = random.choices(pages, weights=transition_prob)[0]
        pagerank_dict[state] += 1
        count += 1

    pagerank_dict = {key: value / n for key, value in pagerank_dict.items()}

    return pagerank_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    for key in corpus:
        if corpus[key] == set():
            corpus[key] = set(corpus.keys())

    corpus_i = {key: set() for key in corpus.keys()}
    pagerank_dict = {key: 1 / len(corpus.keys()) for key in corpus.keys()}

    for key in corpus.keys():
        for page in corpus_i:
            if page in corpus[key]:
                corpus_i[page].add(key)

    while True:
        temp_pagerank_dict = dict()
        for page in corpus.keys():
            left_side = (1 - damping_factor) * (1/len(corpus.keys()))
            right_side = 0
            for linkers in corpus_i[page]:
                right_side += damping_factor * (pagerank_dict[linkers] / len(corpus[linkers]))
                
            temp_pagerank_dict[page] = left_side + right_side

        probs = [abs(pagerank_dict[page] - temp_pagerank_dict[page]) for page in corpus.keys()]
        
        if all(x <= 0.001 for x in probs):
            pagerank_dict = temp_pagerank_dict
            break

        pagerank_dict = temp_pagerank_dict

    return pagerank_dict

if __name__ == "__main__":
    main()
