def initialize_game():
    state = {}
    for i in range(1, 13):
        state[i] = i
    return state

def compute_earnings(N):
    earnings = 0
    state = initialize_game()
    curr_pos = N
    curr_seeds = state[curr_pos]
    state[curr_pos] = 0
    earnings += 1
    curr_seeds -= 1

    # update the states until the current hand gets to zero... 
    # then pick up more from the next until the state that you reach has zero in it and add one to it
    while state[curr_pos] != 0 or curr_seeds > 0:
        if (curr_seeds) > 0:
            curr_pos = (curr_pos + 1) % 13
            curr_pos = 1 if curr_pos == 0 else curr_pos
            state[curr_pos] += 1
            curr_seeds -= 1
        else:
            curr_seeds = state[curr_pos]
            state[curr_pos] = 0
            earnings += 1
            curr_seeds -= 1

    return earnings

print(compute_earnings(5))

max_earnings = 0
max_earnings_spot = -1
for i in range(1, 13):
    earnings = compute_earnings(i)
    if (earnings > max_earnings):
        max_earnings = earnings
        max_earnings_spot = i

print(f'Max Earnings: {max_earnings}, Loc: {max_earnings_spot}')