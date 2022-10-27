import streamlit as st

import re
from collections import Counter
from pprint import pprint

#from functools import filter

def words(text): # 類似split，依照空格切出一個一個字
    return re.findall(r'\w+', text.lower())
word_count = Counter(words(open('data/big 2.txt').read()))
# word_count['the']: 這篇文章總共有幾個the
# word_count.values(): 取出counts of each word as list
N = sum(word_count.values()) # N = 這篇文章總共有幾個字
def P(word): 
    return word_count[word] / N # float

#Run the function:

# print( list(map(lambda x: (x, P(x)), words('speling spelling speeling'))) )

letters    = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)
    
#Run the function:
#pprint( list(edits1('speling'))[:3])
#pprint( list(map(lambda x: (x, P(x)), edits1('speling'))) )
#print( list(filter(lambda x: P(x) != 0.0, edits1('speling'))) )
#print( max(edits1('speling'), key=P) )

def correction(word): 
    return max(candidates(word), key=P)

def candidates(word): 
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words):# 有很多進行編輯後的字，放進word_count檢查有沒有這個字
    return set(w for w in words if w in word_count)

def edits2(word): 
    return (e2 for e1 in (edits1(word)) for e2 in (edits1(e1)))
 
# print('speling -->', correction('speling'))


# streamlit
st.title('Spellchecker Demo')
option_selectbox = st.selectbox('Choose a word or...',('', 'apple', 'lamon', 'speling', 'hapy', 'language', 'greay'))
option_textinput = st.text_input('type your own!!')
show = st.sidebar.checkbox('Show original word')
if option_selectbox:
    if show:
        st.write('Original word:', option_selectbox)
    answer = correction(option_selectbox)
    if option_selectbox == answer:
        st.success(answer+' is the correct spelling!')
    else:
        st.error('Correction: '+answer)
elif option_textinput:
    if show:
        st.write('Original word:', option_textinput)
    answer = correction(option_textinput)
    if option_textinput == answer:
        st.success(answer+' is the correct spelling!')
    else:
        st.error('Correction: '+answer)
