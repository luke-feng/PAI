import random

def generate_seq(n):
    seq = []
    for i in range(n):
        seq.append(random.randint(0, 10))
    return seq

def beam_search():
    sequences = [[[],1]]
    max_len = 10
    num_beams = 4
    n = 10

    for i in range(max_len):
        all_candidates = []
        for i in range(len(sequences)):
            seq, score = sequences[i]
            
            for m in range(len(sequences)):
                seqs = generate_seq(n)
                for j in range(n):
                    candidate = [seq + [j], score + seqs[j]]
                    all_candidates.append(candidate)
        
        ordered = sorted(all_candidates, key= lambda top: top[1], reverse= True)
        sequences = ordered[:num_beams]
    return sequences

seq = beam_search()
for i in seq:
    print(i)
