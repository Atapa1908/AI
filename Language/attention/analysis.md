# Analysis

## Layer 4, Head 6

Similar to Layer 3, Head 10, in which tokens pay attention to the tokens that follow them,
tokens in this attention head seem to pay attention to tokens that preceed them.

Example Sentences:
- [MASK] wore my blue shirt.
- I won't [MASK] stop until my goal is achieved.

## Layer 4, Head 1

This attention head is interesting, as its tokens seem to pay attention to words that have occurrences
in orther places of the sentence. For example, the token 'was' is paying attention to the woken 'was'
at the end of the sentence; likewise with the word 'a' and 'I' in the second example sentence.

Example Sentences:
- He was a lazy man and [MASK] was a crazy lady.
- [MASK] I said I'd do, I did.

