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

# TODO: Optimize transition model


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_pages = len(corpus)
    distribution = {}

    if corpus[page]:  # If the current page has outgoing links
        prob_links = damping_factor / len(corpus[page])
        prob_random = (1 - damping_factor) / num_pages

        for p in corpus:
            if p in corpus[page]:
                distribution[p] = prob_links
            else:
                distribution[p] = prob_random
    else:  # If the current page has no outgoing links
        prob_random = 1 / num_pages
        for p in corpus:
            distribution[p] = prob_random

    # print(distribution)
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to the transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pagerank_estimate = {page: 0 for page in corpus}

    # Start with a random page for the first sample
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        pagerank_estimate[current_page] += 1 / n
        transition_probs = transition_model(
            corpus, current_page, damping_factor)
        next_page = random.choices(
            list(transition_probs.keys()), weights=transition_probs.values())[0]
        current_page = next_page

    return pagerank_estimate


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    initial_rank = 1 / num_pages

    # Initialize page ranks with initial values
    page_ranks = {page_name: initial_rank for page_name in corpus}

    while True:
        new_page_ranks = {}

        # Calculate new ranks based on the PageRank formula
        for page_name in corpus:
            new_rank = (1 - damping_factor) / num_pages

            for linking_page, linked_pages in corpus.items():
                if page_name in linked_pages:
                    num_links = len(linked_pages)
                    new_rank += damping_factor * \
                        (page_ranks[linking_page] / num_links)

            new_page_ranks[page_name] = new_rank

        # Check if the maximum change is below the threshold
        max_change = max(
            abs(new_page_ranks[page_name] - page_ranks[page_name]) for page_name in corpus)
        if max_change < 0.001:
            break

        page_ranks = new_page_ranks

    # Normalize page ranks so they sum to 1
    total_rank = sum(page_ranks.values())
    normalized_ranks = {page_name: rank /
                        total_rank for page_name, rank in page_ranks.items()}

    return normalized_ranks


if __name__ == "__main__":
    main()
