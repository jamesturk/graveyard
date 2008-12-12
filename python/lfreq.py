from collections import defaultdict

languages = {'de': {'E':.16693, 'N':.09905, 'I':.07812, 'S':.06765, 'T':.06742,
'R':.06539, 'A':.06506, 'D':.05414, 'H':.04064, 'U':.03703, 'G':.03647,
'M':.03005, 'C':.02837, 'L':.02825, 'B':.02566, 'O':.02285, 'F':.02044,
'K':.01879, 'W':.01396, 'V':.01069, 'Z':.01002, 'P':.00944, 'J':.00191,
'Q':.00055, 'Y':.00032, 'X':.00022},

'es': { 'E':.13676, 'A':.12529, 'O':.08684, 'S':.07980, 'R':.06873, 'N':.06712,
'I':.06249, 'D':.05856, 'L':.04971, 'C':.04679, 'T':.04629, 'U':.03934,
'M':.03150, 'P':.02505, 'B':.01420, 'G':.01006, 'Y':.00895, 'V':.00895,
'Q':.00875, 'H':.00704, 'F':.00694, 'Z':.00523, 'J':.00443, 'X':.00221,
'W':.00023, 'K':.00004},

'fr': { 'E':.17564, 'A':.08147, 'S':.08013, 'I':.07559, 'T':.07353, 'N':.07322,
'R':.06291, 'U':.05991, 'L':.05783, 'O':.05289, 'D':.04125, 'C':.03063,
'M':.02990, 'P':.02980, 'V':.01557, 'Q':.01361, 'G':.01051, 'F':.00959,
'B':.00876, 'H':.00721, 'J':.00598, 'X':.00350, 'Y':.00116, 'Z':.00072,
'K':.00041, 'W':.00020 },

'en': {'E':.13105, 'T':.10468, 'A':.08151, 'O':.07995, 'N':.07098, 'R':.06832,
'I':.06345, 'S':.06101, 'H':.05259, 'D':.03788, 'L':.03389, 'F':.02924,
'C':.02758, 'M':.02536, 'U':.02459, 'G':.01994, 'Y':.01982, 'P':.01982,
'W':.01539, 'B':.01440, 'V':.00919, 'K':.00420, 'X':.00166, 'J':.00132,
'Q':.00121, 'Z':.00077} }


def guess_language(corpus):
    min_diff = 9999999
    min_lang = 'xx'
    table = defaultdict(float)
    corpus_size = 0
    
    # calculate counts
    for c in corpus:
        if c.isalpha():
            table[c.upper()] += 1
            corpus_size += 1
            
    # normalize
    for x in table:
        table[x] /= corpus_size

    # compare to languages
    for lang, langtable in languages.iteritems():
        diff = {}
        for letter,letter_freq in langtable.iteritems():
            diff[letter] = abs(letter_freq-table[letter])
        total_diff = sum(diff.values())
        print lang, total_diff
        if total_diff < min_diff:
            min_diff = total_diff
            min_lang = lang
    return min_lang, min_diff
    
