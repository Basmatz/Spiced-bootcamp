"""run an mcmc simulation"""

from random import choices

STATES = ['airport', 'air', 'crashed']

def mcmc(i, transition_probs):
    """ runs a monte-carlo markov-chain simulation."""
    history = [i]
    state = i
    while state != 'crashed':
        probs = transition_probs[state]
        state = choices(STATES, probs)[0]
        history.append(state)
        if history[-1] == 'crashed':
            return history

P = {
    'airport': [0.4, 0.6, 0.0],
    'air': [0.8, 0.19999, 0.00001],
}
print(f"crashed after {len(mcmc('airport', P))} days of service")
