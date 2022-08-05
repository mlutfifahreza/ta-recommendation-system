from nltk.corpus import wordnet
from nltk.corpus import wordnet_ic
ic = wordnet_ic.ic('ic-brown.dat')
# ic = wordnet_ic.ic('ic-semcor.dat')

tokens = ['happy', 'good', 'nice', 'bad', 'sad']
for i in range(len(tokens)):
    token_1 = tokens[i]
    print('==============================')
    print(token_1)
    print('token2\tpath\tlch\twup\tres\tjcn\tlin')
    similarities = []
    # synsets for token 1
    token_1_synset = {}
    try: token_1_synset['n'] = wordnet.synset(token_1 + '.' + 'n' + '.01')
    except: token_1_synset['n'] = None
    try: token_1_synset['a'] = wordnet.synset(token_1 + '.' + 'a' + '.01')
    except: token_1_synset['a'] = None
    try: token_1_synset['v'] = wordnet.synset(token_1 + '.' + 'v' + '.01')
    except: token_1_synset['v'] = None
    
    # start comparing
    for token_2 in tokens[:i]+tokens[i+1:]:
        sim_result_list = {}
        # synsets for token 2
        token_2_synset = {}
        try: token_2_synset['n'] = wordnet.synset(token_2 + '.' + 'n' + '.01')
        except: token_2_synset['n'] = None
        try: token_2_synset['a'] = wordnet.synset(token_2 + '.' + 'a' + '.01')
        except: token_2_synset['a'] = None
        try: token_2_synset['v'] = wordnet.synset(token_2 + '.' + 'v' + '.01')
        except: token_2_synset['v'] = None

        temp_similarities = []
        
        # path_similarity
        for type1 in ['n', 'a', 'v']:
            for type2 in ['n', 'a', 'v']:
                if ((token_1_synset[type1] is not None) and (token_2_synset[type2] is not None)):
                    try: temp_similarities.append(token_1_synset[type1].path_similarity(token_2_synset[type2]))
                    except: pass
        if len(temp_similarities) > 0: sim_result_list['path_similarity'] = sum(temp_similarities) / len(temp_similarities)
        else: sim_result_list['path_similarity'] = 0
        temp_similarities = []
        
        # lch_similarity
        for type1 in ['n', 'a', 'v']:
            for type2 in ['n', 'a', 'v']:
                if ((token_1_synset[type1] is not None) and (token_2_synset[type2] is not None)):
                    try: temp_similarities.append(token_1_synset[type1].lch_similarity(token_2_synset[type2]))
                    except: pass
        if len(temp_similarities) > 0: sim_result_list['lch_similarity'] = sum(temp_similarities) / len(temp_similarities)
        else: sim_result_list['lch_similarity'] = 0
        temp_similarities = []
        
        # wup_similarity
        for type1 in ['n', 'a', 'v']:
            for type2 in ['n', 'a', 'v']:
                if ((token_1_synset[type1] is not None) and (token_2_synset[type2] is not None)):
                    try: temp_similarities.append(token_1_synset[type1].wup_similarity(token_2_synset[type2]))
                    except: pass
        if len(temp_similarities) > 0: sim_result_list['wup_similarity'] = sum(temp_similarities) / len(temp_similarities)
        else: sim_result_list['wup_similarity'] = 0
        temp_similarities = []
        
        # res_similarity
        for type in ['n', 'a', 'v']:
            if ((token_1_synset[type] is not None) and (token_2_synset[type] is not None)):
                try: temp_similarities.append( token_1_synset[type].res_similarity(token_2_synset[type], ic))
                except: pass
        if len(temp_similarities) > 0: sim_result_list['res_similarity'] = sum(temp_similarities) / len(temp_similarities)
        else: sim_result_list['res_similarity'] = 0
        temp_similarities = []
        
        # jcn_similarity
        for type in ['n', 'a', 'v']:
            if ((token_1_synset[type] is not None) and (token_2_synset[type] is not None)):
                try: temp_similarities.append( token_1_synset[type].jcn_similarity(token_2_synset[type], ic))
                except: pass
        if len(temp_similarities) > 0: sim_result_list['jcn_similarity'] = sum(temp_similarities) / len(temp_similarities)
        else: sim_result_list['jcn_similarity'] = 0
        temp_similarities = []
        
        # lin_similarity
        for type in ['n', 'a', 'v']:
            if ((token_1_synset[type] is not None) and (token_2_synset[type] is not None)):
                try: temp_similarities.append( token_1_synset[type].lin_similarity(token_2_synset[type], ic))
                except: pass
        if len(temp_similarities) > 0: sim_result_list['lin_similarity'] = sum(temp_similarities) / len(temp_similarities)
        else: sim_result_list['lin_similarity'] = 0
        temp_similarities = []
        
        # print result
        print(token_2, end='\t')
        # for key, value in sim_result_list.items():
        #     print(key, end = '\t')
        # print()
        for key, value in sim_result_list.items():
            if value > 10000: print('BIG', end = '\t')
            else: print('{:.2f}'.format(value), end = '\t')
        print()
    print()