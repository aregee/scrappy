import string
import os
import enchant
import nltk
import requests
from operator import itemgetter

'''
    Ready-to-go NER Algorithm for tweets that somewhat works for now
    Pipeline:
        1. Clean Tweet: Extract mentions, hashtags, links and remaining text
        2. Tokenize, Tag, and run ne_chunk on text
        3. Create frequency dicts for all entites and sort it

    Remaining challenges:
        1. Multiple retweets of the same tweet, thus freq of entites increase
        2. Tweets comprise of news topics (all initials are capitalized),
            thus ne_chunk produces a lot of False Positives in this case
        3. Tweets don't necessarily have correct grammar, thus more FPs
'''


class Ner(object):

    def __init__(self, tweets_list):
        self.tweets_list = tweets_list

    def getCleanTweet(self, text):
        # cleaning tweet text
        cleaned_tweet = {
                'text' : [],
                'mentions' : [],
                'hashtags' : [],
                'links' : []
                }

        twitter_entities = ['#', '@', 'http', 'www']
        for word in text.split():
            clean_word = True
            if word == 'RT':
                continue
            elif word.startswith('@') and word != '@':
                if word.endswith(':'):
                    word = word[:-1]
                cleaned_tweet['mentions'].append(word)
            elif word.startswith('#') and word != '#':
                cleaned_tweet['hashtags'].append(word)
            elif word.startswith('http') or word.startswith('www'):
                cleaned_tweet['links'].append(word)
            else:
                cleaned_tweet['text'].append(word)

        cleaned_tweet['text'] = ' '.join(cleaned_tweet['text'])
        return cleaned_tweet

    def createNeDict(self, named_entities, ner_tweet_ids):

        ne_dict = {}
        classes = ['LOCATION', 'PERSON', 'FACILITY', 'GSP', 'ORGANIZATION', 'GPE']
        for c in classes:
            ne_dict[c] = {}

        for entity in named_entities:
            if entity != 'ner':
                named_entities[entity] = {i : named_entities[entity].count(i) for i in named_entities[entity]}
                named_entities[entity] = sorted(named_entities[entity].items(), key=itemgetter(1), reverse=True)
            else:

                for en in named_entities[entity]:
                    if en[1] not in ne_dict[en[0]]:
                        ne_dict[en[0]][en[1]] = {
                                    "count": len(ner_tweet_ids[en[1]]),
                                    "tweet_ids" : ner_tweet_ids[en[1]]
                                    }
                    '''
                    else:
                        prev_tweet_obj = ne_dict[en[0]][en[1]]
                        ne_dict[en[0]][en[1]] = {
                                "count": prev_tweet_obj['count'] + len(ner_tweet_ids[en[1]]),
                                "tweet_ids": prev_tweet_obj['tweet_ids'].extend(ner_tweet_ids[en[1]])
                                }
                    '''
                ne_dict = {key: ne_dict[key] for key in ne_dict if ne_dict[key]} 
                named_entities[entity] = ne_dict

                #TODO sorting
                #named_entities[entity] = {n_e: sorted(ne_dict[n_e].items(), key=itemgetter(1), reverse = True) for n_e in ne_dict}
        return named_entities

    def get_entity_value(self, text):

        inputlist = []
        try:
            sentence_parts = (str(nltk.Tree.fromstring(str(text)))).split('\n')
        except:
            return []

        for each in sentence_parts:
            each = each.lstrip()
            if each.startswith('('):
                each = each[1:]
            if each.endswith(')'):
                each = each[:-1]
            inputlist.append(each.lstrip())

        outputlist =[]
        entitydict={}
        classes_types = ['LOCATION', 'PERSON', 'FACILITY', 'GSP', 'ORGANIZATION', 'GPE']

        for i, entity in enumerate(inputlist):
            if len(entitydict)==0:
                if entity.split()[0] in classes_types:
                    entitylist = entity.split()
                    entitydict[entity.split()[0]] = ""
                    if len(entitylist)>1:
                        for en in entitylist:
                            entitydict[entity.split()[0]] += " "+en.split("/")[0]
            else:
                for key in entitydict:
                    if key in entity.split()[0]:
                        entitylist = entity.split()
                        flag = True
                        if entitylist>1:

                            for en in entitylist:
                                if flag== True:
                                    flag= False
                                    continue
                                entitydict[key] += " "+en.split("/")[0]
                    else:
                        if len(entitydict[key][len(key)+2:]) >0:
                            outputlist.append([key, entitydict[key][len(key)+2:]])
                        entitydict={}
                        if entity.split()[0] in classes_types:
                            entitylist = entity.split()
                            entitydict[entity.split()[0]] = ""
                            if len(entitylist) > 0:
                                for en in entitylist:
                                    entitydict[entity.split()[0]] += " "+en.split("/")[0]

                        break
        if len(entitydict) > 0:
            for key in entitydict:
                if len(entitydict[key][len(key)+2:]) > 0:
                    outputlist.append([key, entitydict[key][len(key)+2:]])

        return outputlist

    def getNodes(self, parent, ne):
        try:
            for node in parent:
                if type(node) is nltk.Tree:
                    ne.append([node.label(), ' '.join([i[0] for i in node.leaves()])])
                    self.getNodes(node, ne)

            return ne
        except:
            return []

    def ne_chunk(self, tweet_id, tweet_text):

        sent_ner = []
        ner_tweets = {}
        sents = nltk.sent_tokenize(tweet_text)

        for text in sents:
            text = nltk.word_tokenize(text)
            text = nltk.pos_tag(text)
            text = nltk.ne_chunk(text)


            ner_list = self.getNodes(text, [])
            if ner_list:
                sent_ner.extend(ner_list)

            #ner_list = self.get_entity_value(text)
            #sent_ner.extend(ner_list)

            for each_ner in ner_list:
                if each_ner[1] in ner_tweets and tweet_id not in ner_tweets[each_ner[1]]:
                    ner_tweets[each_ner[1]].append(tweet_id)
                else:
                    ner_tweets[each_ner[1]] = [tweet_id]
        return sent_ner, ner_tweets

    def extractEntities(self, tweet_data):

        entities = {
                'ner': [],
                'mentions': [],
                'hashtags': [],
                'links': []
                }
        ner_tweets = {}

        ner_tweet_ids = {}
        for tweet in tweet_data:
            text_entities = self.getCleanTweet(unicode(tweet['text']))
            for key in entities:
                if key == 'ner':
                    ner_entities, ner_tweet_id = self.ne_chunk(tweet['id'], text_entities['text'])
                    entities['ner'].extend(ner_entities)

                    for entity in ner_tweet_id:
                        if entity in ner_tweet_ids:
                            ner_tweet_ids[entity].extend(ner_tweet_id[entity])
                        else:
                            ner_tweet_ids[entity] = ner_tweet_id[entity]
                else:
                    entities[key].extend(text_entities[key])


        entities = self.createNeDict(entities, ner_tweet_ids)


        return entities

    '''
        Resolves conflict between token occuring in 2 different categories by
        chossing the one with the higher count
        TODO use later
    '''
    def bucket_management(self, ner_dict):

        all_keys = []
        for each in ner_dict:
            part_list = ner_dict[each]
            for each in part_list:
                if each[0] not in all_keys:
                    all_keys.append(each[0])

        final_dict = {}

        for each_key in all_keys:
            val = 0
            main_key = ''
            sub_key = ''
            for each in ner_dict:
                for each_element in ner_dict[each]:
                    if each_element[0] == each_key:
                        if each_element[1] >= val:
                            val = each_element[1]
                            sub_key = each_element[0]
                            main_key = each

            if main_key in final_dict:
                temp_dict = final_dict[main_key]
                temp_dict[sub_key] = val
            else:
                final_dict[main_key]= {sub_key: val}
        return final_dict

    # NOTE ner sorting giver here
    def process_ner(self, extractedEntitiesDict):
        #unsorted_dict = self.bucket_management(extractedEntitiesDict['ner'])
        unsorted_dict = extractedEntitiesDict['ner']
        sorted_dict = {}
        for each in unsorted_dict:
            sorted_dict[each] = {_[0]:_[1] for _ in sorted(unsorted_dict[each].items(), key=itemgetter(1), reverse=True)}

        extractedEntitiesDict['ner'] = sorted_dict
        return extractedEntitiesDict

    def get_entities(self):
        extractedEntitiesDict = self.extractEntities(self.tweets_list)
        #return extractedEntitiesDict
        return self.process_ner(extractedEntitiesDict)
