import sys
from collections import defaultdict

def normalize_symbol(symbol):
    return symbol.replace('’', "'")  # Replace right single quotation mark with apostrophe

def tokenize_rhs(rhs):
    tokens = []
    i = 0
    while i < len(rhs):
        c = rhs[i]
        if c == ' ':
            i += 1
            continue
        elif c.isupper() or c == 'S':
            # Nonterminal symbol (handle S’ or S')
            if i+1 < len(rhs) and rhs[i+1] in ["'", "’"]:
                token = c + rhs[i+1]
                tokens.append(normalize_symbol(token))
                i += 2
            else:
                tokens.append(c)
                i += 1
        elif c.islower():
            tokens.append(c)
            i += 1
        elif c == '$':
            if i+1 < len(rhs) and rhs[i+1] == '$':
                tokens.append('$$')
                i += 2
            else:
                tokens.append('$')
                i += 1
        else:
            i += 1
    return tokens

def read_grammar(filename):
    grammar = defaultdict(list)
    nonterminals = set()
    terminals = set()
    start_symbol = None
    START_SYMBOL = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if '->' not in line:
                continue
            lhs, rhs = line.split('->')
            lhs = normalize_symbol(lhs.strip())
            rhs = normalize_symbol(rhs.strip())
            if start_symbol is None:
                start_symbol = lhs
                START_SYMBOL = lhs
            nonterminals.add(lhs)
            if rhs == '':
                grammar[lhs].append([])
            else:
                tokens = tokenize_rhs(rhs)
                grammar[lhs].append(tokens)
                for token in tokens:
                    if token.isupper() or token in nonterminals or (len(token) > 1 and token[-1] == "'"):
                        nonterminals.add(token)
                    elif token == '$$':
                        terminals.add('$$')
                    else:
                        terminals.add(token)
    return grammar, nonterminals, terminals, START_SYMBOL

def compute_first_sets(grammar, terminals, nonterminals):
    first = {symbol: set() for symbol in nonterminals.union(terminals)}
    for terminal in terminals:
        first[terminal].add(terminal)
    changed = True
    while changed:
        changed = False
        for lhs in grammar:
            for rhs in grammar[lhs]:
                if not rhs:
                    # Epsilon production
                    if '' not in first[lhs]:
                        first[lhs].add('')
                        changed = True
                    continue
                before_change = len(first[lhs])
                i = 0
                while i < len(rhs):
                    symbol = rhs[i]
                    first_symbol = first[symbol]
                    first[lhs].update(first_symbol - set(['']))
                    if '' in first_symbol:
                        i += 1
                    else:
                        break
                else:
                    first[lhs].add('')
                if len(first[lhs]) != before_change:
                    changed = True
    return first

def compute_first_of_string(symbols, first):
    result = set()
    for symbol in symbols:
        result.update(first[symbol] - set(['']))
        if '' in first[symbol]:
            continue
        else:
            break
    else:
        result.add('')
    return result

def compute_follow_sets(grammar, terminals, nonterminals, first, start_symbol):
    follow = {symbol: set() for symbol in nonterminals}
    changed = True
    while changed:
        changed = False
        for lhs in grammar:
            for rhs in grammar[lhs]:
                trailer = follow[lhs]
                for i in range(len(rhs)):
                    symbol = rhs[i]
                    if symbol in nonterminals:
                        before_change = len(follow[symbol])
                        beta = rhs[i+1:]
                        if beta:
                            first_beta = compute_first_of_string(beta, first)
                            follow[symbol].update(first_beta - set(['']))
                            if '' in first_beta:
                                follow[symbol].update(trailer)
                        else:
                            follow[symbol].update(trailer)
                        if len(follow[symbol]) != before_change:
                            changed = True
    return follow

def sort_symbols(symbols):
    def sort_key(s):
        return (s == '$$', s)
    return sorted(symbols, key=sort_key)

def main():
    if len(sys.argv) != 3:
        print("Usage: python ff_compute.py g.txt ff.txt")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    grammar, nonterminals, terminals, START_SYMBOL = read_grammar(input_file)
    first = compute_first_sets(grammar, terminals, nonterminals)
    follow = compute_follow_sets(grammar, terminals, nonterminals, first, START_SYMBOL)

    # Prepare nonterminals in order, with the start symbol first
    nonterminals_ordered = sorted(nonterminals - set([START_SYMBOL]))
    if START_SYMBOL in nonterminals:
        nonterminals_ordered = [START_SYMBOL] + nonterminals_ordered

    with open(output_file, 'w') as f:
        for nt in nonterminals_ordered:
            f.write(nt + '\n')
            # Prepare FIRST set
            first_set = first[nt]
            if '' in first_set:
                first_set.remove('')
            first_list = sort_symbols(first_set)
            f.write(', '.join(first_list))
            f.write('\n')
            # Prepare FOLLOW set
            follow_set = follow[nt]
            follow_list = sort_symbols(follow_set)
            f.write(', '.join(follow_list))
            f.write('\n')

if __name__ == "__main__":
    main()