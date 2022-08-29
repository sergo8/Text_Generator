from nltk.tokenize import WhitespaceTokenizer
from nltk import trigrams
from collections import Counter
from random import choices, choice
from nltk import regexp_tokenize

f = open(input(), "r", encoding="utf-8")
raw_text = f.read()
text = WhitespaceTokenizer().tokenize(raw_text)

trigrm = list(trigrams(text))  # list of all tri_grams
raw_freq_list = Counter(trigrm).most_common()  # count how many repetitions of trigrams


# Make a list of single elements where each has a head, tail and number of repetitions(freq)
freq_list = []
for i in raw_freq_list:
    head = i[0][0] + ' ' + i[0][1]
    tail = i[0][-1]
    freq = i[-1]
    single_item = [head, tail, freq]
    freq_list.append(single_item)


# Function to create a list from which a beginning word is selected
def make_begin_word():
    begin_list = []
    begin_list_sorted = []
    for k in freq_list:
        begin_list.append(k[0])

    # Create a list with words what begin sentence
    for j in begin_list:
        if regexp_tokenize(j[0], r"[A-Z]+[a-z']*\b\S*"):
            begin_list_sorted.append(j)

    return begin_list_sorted


# Function where the first word is selected in a random choice
def select_fist_word():
    while True:
        text_head = choice(make_begin_word())

        if text_head.split()[0].endswith('.'):
            continue
        elif text_head.split()[0].endswith('!'):
            continue
        elif text_head.split()[0].endswith('?'):
            continue
        else:
            break

    return text_head


# Function where a tail word is selected based on the head word
def select_tail(head_selected):
    next_word_prob_dict = {}
    head_list = [n[0] for n in freq_list]

    if head_selected in head_list:

        for j in freq_list:
            if j[0] == head_selected:
                next_word_prob_dict[j[1]] = j[-1]

        tail_list = [n for n in next_word_prob_dict.keys()]
        tail_probability_list = [m for m in next_word_prob_dict.values()]
        tail_selected = choices(tail_list, tail_probability_list)[-1]

        # print(next_word_prob_dict)

        return tail_selected


# Function to select the last two tokens and use for further text prediction
def select_next_word():

    if len(text_output_list[-2].split(' ')) == 2:
        last_two_tokens = (text_output_list[-2].split(' ')[1] + ' ' + text_output_list[-1])
    else:
        last_two_tokens = (text_output_list[-2] + ' ' + text_output_list[-1])

    return last_two_tokens


def loop_execution():
    global text_output_string, text_output_list

    for j in range(0, 10, 1):
        text_output_list = []
        text_output_string = ''

        start_words = select_fist_word()  # randomly selects the first sentence from corpus
        text_output_list.append(start_words)  # assign first word of the output list
        tail_words = select_tail(start_words)
        text_output_list.append(tail_words)

        while True:

            next_word_selection = select_tail(select_next_word())
            text_output_list.append(next_word_selection)

            if (len(text_output_list) >= 4) and (text_output_list[-1][-1] in '!?.'):
                break

        text_output_string = ' '.join(text_output_list)
        print(f'{text_output_string}')


loop_execution()
f.close()
