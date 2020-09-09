from random import choices

STATES = [
'airport', 'air', 'crashed'
]

def mcmc(i, P):
    """runs a Monte-Carlo Markov-Chain simulation of a plane. Returns a list of states passed."""
    history = [i]
    state = i
    while state !='crashed':
        probs = P[s]
        s = choices(STATES, probs) [0]
        list.append(s)
        if list[-1] == 'crashed':
            return list

P = {
    'airport': [0.4, 0.6, 0.0],
    'air': [0.8, 0.19999, 0.00001],
}
print(f"crashed after {len(mcmc('airport', P))} days of service")
