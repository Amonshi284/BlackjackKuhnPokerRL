def get_optimal_action(obs, start, alpha, random):
    # obs[0] -> 0 = Jack, 1 = Queen, 2 = King
    # obs[1] -> 0 = no action, 1 = check/fold, 2 = bet/call
    if obs[1] == 0:
        if obs[0] == 0:
            if random.random() < alpha:
                return 2
            else:
                return 1
        elif obs[0] == 1:
            return 1
        else:
            if random.random() < 3 * alpha:
                return 2
            else:
                return 1
    elif obs[1] == 1:
        if obs[0] == 0:
            if random.random() < 1.0 / 3:
                return 2
            else:
                return 1
        elif obs[0] == 1:
            return 1
        else:
            return 2
    else:
        if obs[0] == 0:
            return 1
        elif obs[0] == 1:
            if start == "opponent":
                if random.random() < 1.0 / 3 + alpha:
                    return 2
                else:
                    return 1
            else:
                if random.random() < 1.0 / 3:
                    return 2
                else:
                    return 1
        else:
            return 2
