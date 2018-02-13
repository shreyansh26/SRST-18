from __future__ import print_function
import pickle
import sys, codecs, os, string, getopt
from functools import wraps
import re

def has_num(inputString):
    return bool(re.search(r'\d', inputString))

def hamming(s,t):
    return sum(1 for x,y in zip(s,t) if x != y)    

def halign(s,t):
    """Align two strings by Hamming distance."""
    slen = len(s)
    tlen = len(t)    
    minscore = len(s) + len(t) + 1
    for upad in xrange(0, len(t)+1):
        upper = '_' * upad + s + (len(t) - upad) * '_'
        lower = len(s) * '_' + t
        score = hamming(upper, lower)
        if score < minscore:
            bu = upper
            bl = lower
            minscore = score

    for lpad in xrange(0, len(s)+1):
        upper = len(t) * '_' + s
        lower = (len(s) - lpad) * '_' + t + '_' * lpad
        score = hamming(upper, lower)
        if score < minscore:
            bu = upper
            bl = lower
            minscore = score

    zipped = zip(bu,bl)
    newin  = ''.join(i for i,o in zipped if i != '_' or o != '_')
    newout = ''.join(o for i,o in zipped if i != '_' or o != '_')
    return newin, newout

def levenshtein(s, t, inscost = 1.0, delcost = 1.0, substcost = 1.0):
    """Recursive implementation of Levenshtein, with alignments returned."""
    @memolrec
    def lrec(spast, tpast, srem, trem, cost):
        if len(srem) == 0:
            return spast + len(trem) * '_', tpast + trem, '', '', cost + len(trem)
        if len(trem) == 0:
            return spast + srem, tpast + len(srem) * '_', '', '', cost + len(srem)

        addcost = 0
        if srem[0] != trem[0]:
            addcost = substcost
            
        return min((lrec(spast + srem[0], tpast + trem[0], srem[1:], trem[1:], cost + addcost),
                   lrec(spast + '_', tpast + trem[0], srem, trem[1:], cost + inscost),
                   lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
                   key = lambda x: x[4])

    answer = lrec('', '', s, t, 0)
    return answer[0],answer[1],answer[4]

def memolrec(func):
    """Memoizer for Levenshtein."""
    cache = {}
    @wraps(func)
    def wrap(sp, tp, sr, tr, cost):
        if (sr,tr) not in cache:
            res = func(sp, tp, sr, tr, cost)
            cache[(sr,tr)] = (res[0][len(sp):], res[1][len(tp):], res[4] - cost)
        return sp + cache[(sr,tr)][0], tp + cache[(sr,tr)][1], '', '', cost + cache[(sr,tr)][2]
    return wrap
    
def alignprs(lemma, form):
    """Break lemma/form into three parts:
    IN:  1 | 2 | 3
    OUT: 4 | 5 | 6
    1/4 are assumed to be prefixes, 2/5 the stem, and 3/6 a suffix.
    1/4 and 3/6 may be empty.
    """
    
    al = levenshtein(lemma, form, substcost = 1.1) # Force preference of 0:x or x:0 by 1.1 cost
    alemma, aform = al[0], al[1]
    # leading spaces
    lspace = max(len(alemma) - len(string.lstrip(alemma, '_')), len(aform) - len(string.lstrip(aform,'_')))
    # trailing spaces
    tspace = max(len(alemma[::-1]) - len(string.lstrip(alemma[::-1],'_')), len(aform[::-1]) - len(string.lstrip(aform[::-1],'_')))
    return alemma[0:lspace], alemma[lspace:len(alemma)-tspace], alemma[len(alemma)-tspace:], aform[0:lspace], aform[lspace:len(alemma)-tspace], aform[len(alemma)-tspace:]

def prefix_suffix_rules_get(lemma, form):
    """Extract a number of suffix-change and prefix-change rules
    based on a given example lemma+inflected form."""
    lp,lr,ls,fp,fr,fs = alignprs(lemma, form) # Get six parts, three for in three for out

    # Suffix rules
    ins  = lr + ls + ">"
    outs = fr + fs + ">"    
    srules = set()
    for i in xrange(min(len(ins), len(outs))):
        srules.add((ins[i:], outs[i:]))
    srules = {(string.replace(x[0], '_',''), string.replace(x[1],'_','')) for x in srules}

    # Prefix rules
    prules = set()
    if len(lp) >= 0 or len(fp) >= 0:
        inp = "<" + lp
        outp = "<" + fp
        for i in xrange(0,len(fr)):
            prules.add((inp + fr[:i],outp + fr[:i]))
            prules = {(string.replace(x[0],'_',''), string.replace(x[1], '_','')) for x in prules}

    return prules, srules

def apply_best_rule(lemma, msd, allprules, allsrules):
    """Applies the longest-matching suffix-changing rule given an input
    form and the MSD. Length ties in suffix rules are broken by frequency.
    For prefix-changing rules, only the most frequent rule is chosen."""
    
    bestrulelen = 0
    base = "<" + lemma + ">"
    if msd not in allprules and msd not in allsrules:
        return lemma # Haven't seen this inflection, so bail out

    if msd in allsrules:
        applicablerules = [(x[0],x[1],y) for x,y in allsrules[msd].iteritems() if x[0] in base]
        if applicablerules:
            bestrule = max(applicablerules, key = lambda x: (len(x[0]), x[2], len(x[1])))           
            base = string.replace(base, bestrule[0], bestrule[1])
        
    if msd in allprules:
        applicablerules = [(x[0],x[1],y) for x,y in allprules[msd].iteritems() if x[0] in base]
        if applicablerules:
            bestrule = max(applicablerules, key = lambda x: (x[2]))
            base = string.replace(base, bestrule[0], bestrule[1])
                
    base = string.replace(base, '<', '')
    base = string.replace(base, '>', '')
    return base

def numleadingsyms(s, symbol):
    return len(s) - len(s.lstrip(symbol))
    
def numtrailingsyms(s, symbol):
    return len(s) - len(s.rstrip(symbol))

###############################################################################

def main(argv):
    options, remainder = getopt.gnu_getopt(argv[1:], 'ohp:', ['output','help', 'path='])
    OUTPUT, HELP, PATH = False, False, './dataset/'
    for opt, arg in options:
        if opt in ('-o', '--output'):
            OUTPUT = True
        elif opt in ('-h', '--help'):
            HELP = True
        elif opt in ('-p', '--path'):
            PATH = arg
            
    if HELP:
            print("\n*** Baseline for the CoNLL-SIGMORPHON 2017 shared task ***\n")
            print("By default, the program only evaluates accuracy.")
            print("To create output files, use -o")
            print("The training and dev-data are assumed to live in ./dataset/ \n")
            print("Options:")
            print(" -o         create output files with guesses (and don't just evaluate)")           
            quit()
    
    ## Load model
    with open('models/allsrules.pkl', 'rb') as f:
        allsrules = pickle.load(f)

    with open('models/allprules.pkl', 'rb') as f:
        allprules = pickle.load(f)

    with open('models/prefbias.pkl', 'rb') as f:
        prefbias = pickle.load(f)

    with open('models/suffbias.pkl', 'rb') as f:
        suffbias = pickle.load(f)

    # Run eval on dev
    devlines = [line.strip() for line in codecs.open(PATH + 'unimorph_tags2.txt', "r", encoding="utf-8")]

    if OUTPUT:
        outfile = codecs.open(PATH + "jumbled_sentence", "w", encoding="utf-8")

    sentence = []

    for l in devlines:
        #print(l)
        if not l.strip():
            outfile.write(' '.join(sentence))
            outfile.write('\n')
            sentence = []
            continue
        else:
            lemma, msd, pos_tag = l.split(u'\t')
            lemmaorig = lemma
            if prefbias > suffbias:
                lemma = lemma[::-1]
            if pos_tag in ['PRON', 'PUNCT', 'PROPN'] or has_num(lemma):
                outform = lemma
            else:
                outform = apply_best_rule(lemma, msd, allprules, allsrules)
                if prefbias > suffbias:
                    outform = outform[::-1]
            sentence.append(outform)

    if OUTPUT:
        outfile.close()                   
    print("----------------DONE--------------------\n")

if __name__ == "__main__":
    main(sys.argv)
