#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 13:23:48 2021

@author: Pablo Calleja
"""



import json
import nltk






def tokenize(txt):
    res= nltk.word_tokenize(txt)
    return res

def get_entities_in_offset(entities,text, start, end):
    result=[]
    #print('---'+str(start)+' '+str(end))
    for entity in entities:
        start_e= entity[0]
        end_e= entity[1]
        #print(str(start_e)+' '+str(end_e))
        if start_e >= start and end_e <= end:
            ent=entity
            ent.append(text[start_e:end_e])
            result.append(ent)
    return result


def annotate_entities(tokens, entities):
    labels=[]
    
    for token in tokens:
        labels.append('O')
    for entity in entities:
        
        ent_tokens= tokenize(entity[3])
        labels= annotate_entity(tokens,labels,ent_tokens,entity[2])
    
    return labels     
        
def annotate_entity(tokens, labels, entity_tokens,tag):
    
    
    
    entity_len= len(entity_tokens)
    
    begginings = [i for i, x in enumerate(tokens) if x == entity_tokens[0]]
    for beggining in begginings:
        first_pos=beggining
        others=[]
        if entity_len > 1:
            rest_entity_tokens= entity_tokens[1:]
            rest_tokens =tokens[first_pos+1:first_pos+entity_len]
            counter=first_pos+1
            for token,ent_tok in zip(rest_tokens,rest_entity_tokens):
                
                if token == ent_tok or ent_tok in token:
                    others.append(counter)
                    counter+=1
                else:
                    print('something wrong')
                    print(tokens)
                    print(entity_tokens)
                    continue
          
        labels[first_pos]='B-'+tag
        
        for other in others:
            labels[other]='I-'+tag
       #annotate     
    return labels


def read_file(file):
  sentences=[]
  with open(file, 'r',encoding='utf8') as f:
    for line in f:
      line= line.replace('\n','')
     
      
      sentences.append(json.loads(line))
    f.close()
    return sentences  


def write_file(filename, sentences):
    with open(filename, 'w', encoding='utf8') as f:
        for s in sentences:
            f.write(s)
            f.write('\n')

    f.close()

def convert_jsonl_to_conll(file,outputfile):
    

    datafile =read_file(file)
    
    
    token_list=[]
    label_list=[]
    
    for data in datafile:
        
        labels= data['label']
        text =data['data']
        
        
        sentences= text.split('\n')
        
        listofentities= labels
        
        
        offset_total=0
        for sentence in sentences:
            offset_plus= len(sentence) 
            
            tokens=tokenize(sentence)
            if len(tokens)==0:
                continue
            entities2= get_entities_in_offset(listofentities, text, offset_total, offset_total+ offset_plus)
            
            lab=annotate_entities(tokens, entities2)    
            
            offset_total=offset_total+offset_plus
            
            token_list.append(tokens)
            label_list.append(lab)
            
    lines=[]
    for tokens,labels in zip(token_list,label_list):
        
        for token,label in zip(tokens,labels):
            lines.append(token+' '+label)

        lines.append('\n')
    write_file(outputfile,lines)
    


convert_jsonl_to_conll('mytest.jsonl','mytest.conll')







