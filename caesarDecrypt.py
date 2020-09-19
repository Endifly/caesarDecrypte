#pip install pyenchant
import enchant
#from nltk.corpus import words
alphabets = [chr(e) for e in range(ord("a"),ord("z")+1)]
enc_dicts = {}
d = enchant.Dict("en_US")
#d.check("hello")

def valid_word(word) :
    result = ""
    for letter in word :
        if letter in alphabets :
            result += letter
    return result

def init_decrypt_dict(str1):
    dict = {}
    for n in str1:
        keys = dict.keys()
        if n not in alphabets :
            continue
        if n not in keys:
            dict[n] = "-"
    return dict

def subsitute(char,current_map) :
    if char not in alphabets :
        return []
    elif enc_dicts[char] != "-" :
        return enc_dicts[char]
    elif current_map[char] != "-" :
        return current_map[char]
    else :
        return alphabets

def permute(origin,result,current_map) :
    current_map = current_map.copy()
    if len(origin) == len(result) :
        if d.check(result) :
            yield result
            return
        return
    char = origin[len(result)]
    subList = subsitute(char,current_map)
    for sub in subList :
        concatResult = result+sub
        current_map[char] = sub
        yield from permute(origin,concatResult,current_map)

def encrypte_with_enc_dicts(word) :
    result = ""
    for i in word :
        #print(i)
        if i not in enc_dicts.keys() :
            result += i
        elif i not in alphabets :
            result += i
        else :
            result += enc_dicts[i]
    return result

def update_enc_dicts(real_word,cipherd) :
    if len(real_word) == len(cipherd) :
        for i in range(len(real_word)) :
            if enc_dicts[cipherd[i]] == "-" or enc_dicts[cipherd[i]] == real_word[i] or real_word[i] == "-":
                enc_dicts[cipherd[i]] = real_word[i]
                #print(enc_dicts)
            else :
                print("conflict word,pls select candidate againt")
                print("old candidate : ",enc_dicts[cipherd[i]])
                print("new candidate : ",real_word[i])
                sel_again = input("selected candidate from above : ")
                enc_dicts[cipherd[i]] = sel_again

word = input("enter ciphered text >> ").strip().lower()
word_list = [valid_word(x) for x in word.strip().split()]
enc_dicts = init_decrypt_dict(word)
current_map = init_decrypt_dict(word)
while True :
    choice = {}
    print("ori word : ",word)
    print("enc word : ",encrypte_with_enc_dicts(word))
    print("pls choose word that need to brute force")
    for i in range(len(word_list)) :
        choice[str(i)] = word_list[i]
        print(i,word_list[i])
    input_choice = input("num >> ")
    sovling = choice[input_choice]
    solve = permute(sovling,"",current_map)
    print("------ candidate of",sovling,"------")
    for i in solve :
        print(i)
    print("------------------------------")
    print("""choose candidate or type a number to cancle""")
    real_word = input(str("add candidate for "+sovling+" : ")).strip()
    if real_word[0].isnumeric() :
        continue
    update_enc_dicts(real_word,sovling)

