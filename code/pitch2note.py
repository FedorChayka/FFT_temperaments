import numpy

# factorizes `n`
def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

# turns a fraction `n`/`d` into a monzo with limit `limit`
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
def get_monzo(limit, n, d):
    # limit primes by limit
    avail_primes = [p for p in PRIMES if p <= limit]

    monzo = [0] * len(avail_primes)

    for p in prime_factors(n):
        try:
            idx = avail_primes.index(p)
        except ValueError:
            raise ValueError(f"can't make monzo for {n}/{d} with limit {limit}")
        
        monzo[idx] = monzo[idx] + 1
    
    for p in prime_factors(d):
        try:
            idx = avail_primes.index(p)
        except ValueError:
            raise ValueError(f"can't make monzo for {n}/{d} with limit {limit}")
        
        monzo[idx] = monzo[idx] - 1
    
    return monzo

# map an interval `n`/`d` using prime-limit `limit`, `projection`, and `tuning_map`
def map_interval(projection, tuning_map, limit, n, d):
    interval = get_monzo(limit, n, d)
    projected_interval = projection.dot(interval)
    cents = projected_interval.dot(tuning_map)
    return cents

OCTAVE_INTERVALS = [
    [1, 1], # unison
    [16, 15], # minor second
    [9, 8],   # major second
    [6, 5],   # minor third
    [5, 4],   # major third
    [4, 3],   # perfect fourth
    [64, 45], # tritone
    [3, 2],   # perfect fifth
    [8, 5],   # minor sixth
    [5, 3],   # major sixth
    [16, 9],  # minor seventh
    [15, 8],  # major seventh
    # [2, 1],   # octave
]
# return an octave of notes starting from A_{octave}
#   using the given frequency for A, projection, tuning map, and prime limit
# ie if octave=2, returns A2, B2, C3, D3, ...
def map_octave(octave, a_freq, projection, tuning_map, limit):
    note_names = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

    notes = []
    for (i, (name, interval)) in enumerate(zip(note_names, OCTAVE_INTERVALS)):
        note_octave = octave if i < 3 else octave + 1
        interval_cents = map_interval(projection, tuning_map, limit, interval[0], interval[1])
        notes.append((name + str(note_octave), change_freq_by_cents(a_freq, interval_cents)))
    
    return notes

# change a frequency `freq` by `cents` cents
def change_freq_by_cents(freq, cents):
    return freq * (2**(cents/1200))

# 1/4 comma meantone
# takes tuning_standard to be the frequency for A4
def temperament_quarter_comma_meantone(tuning_standard):
    limit = 7
    projection = numpy.array([
        [1,   1, 0,  -3],
        [0,   0, 0,   0],
        [0, 1/4, 1, 5/2],
        [0,   0, 0,   0],
    ])
    tuning_map = numpy.array([1200, 1896.5784, 2786.3137, 3365.7843])
    
    a4 = tuning_standard
    octaves = sum([
        map_octave(0, a4 * 0.5 * 0.5 * 0.5 * 0.5, projection, tuning_map, limit),
        map_octave(1, a4 * 0.5 * 0.5 * 0.5, projection, tuning_map, limit),
        map_octave(2, a4 * 0.5 * 0.5, projection, tuning_map, limit),
        map_octave(3, a4 * 0.5, projection, tuning_map, limit),
        map_octave(4, a4, projection, tuning_map, limit),
        map_octave(5, a4 * 2, projection, tuning_map, limit),
        map_octave(6, a4 * 2 * 2, projection, tuning_map, limit),
        map_octave(7, a4 * 2 * 2 * 2, projection, tuning_map, limit)
    ], [])

    # temp
    for n in octaves:
        print(n)

    return octaves

def temperament_12edo():
    # TODO
    pass
