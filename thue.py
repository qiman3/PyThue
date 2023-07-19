import random
import argparse

class EndOfProgramException(Exception):
    pass

def format_raw_thue(raw_thue):
    seperator = raw_thue.index("::=")
    instructions = tuple(tuple(rule.split("::=")) for rule in raw_thue[:seperator] if rule != "")
    start_state = "".join(raw_thue[seperator+1:]) # Might be worth looking into other data structures i.e. linked list
    return instructions, start_state

def find_next_rule(rules, current_state, is_random, is_left):
    valid_rules = []
    for i, rule in enumerate(rules):
        if rule[0] in current_state:
            valid_rules.append(i)
    
    if len(valid_rules) == 0:
        raise EndOfProgramException()
    
    next_rule = None
    if is_random:
        next_rule = random.choice(valid_rules)
    elif is_left:
        next_rule = min(valid_rules)
    else:
        next_rule = max(valid_rules)

    return rules[next_rule]

def resolve_single_step(rules, curr_state, args):
    next_rule = find_next_rule(rules, curr_state, ~(args.left | args.right), args.left)
    if args.verbose:
        print(f"Using rule {next_rule[0]} => {next_rule[1]}")
    if next_rule[1] == "":
        next_state = curr_state.replace(next_rule[0],"")
    elif next_rule[1][0] == "~":
        print(next_rule[1][1:].replace("\\n","\n"), end= "\n" if args.nl__newline else "")
        next_state = curr_state.replace(next_rule[0],"")
    elif next_rule[1] == ":::":
        user_input = input(">").strip()
        next_state = curr_state.replace(next_rule[0], user_input)
    else:
        next_state = curr_state.replace(next_rule[0], next_rule[1])
    if args.verbose:
        print(f"{curr_state} => {next_state} \n")
    return next_state


def run_thue_program(rules, start_state, args):
    current_state = start_state
    step_counter = 0
    while True:
        if args.Maxiteration is not None:
            if step_counter > args.Maxiteration:
                break
        try:
            current_state = resolve_single_step(rules, current_state, args)
            step_counter += 1
        except EndOfProgramException:
            return current_state
    
    return f"Max iterations reached! Last program state was {current_state}"

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("source", help="Location of Thue code")
    parser.add_argument("-v","--verbose", help="shows state after each instruciton", action="store_true")
    group.add_argument("-l","--left", help="executes first matching instruction from the left", action="store_true")
    group.add_argument("-r","--right", help="executes first matching instruction from the right", action="store_true")
    parser.add_argument("-M", "--Maxiteration", type=int, help="maximum number of steps the Thue program can for")
    parser.add_argument("-e", "--endstate", help="show last state before finishing", action="store_true")
    parser.add_argument("-nl" "--newline", help="adds newline after each ~", action="store_true")
    args = parser.parse_args()
    with open(args.source) as f:
        readlines = f.readlines()
        raw_program = [l[:-1] if i != len(readlines)-1 else l for i,l in enumerate(readlines)]
    
    rules, start_state = format_raw_thue(raw_program)
    end_state = run_thue_program(rules, start_state, args)
    if args.endstate:
        print(end_state)

if __name__ == "__main__":
    main()