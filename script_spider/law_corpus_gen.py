#!/usr/bin/env python3
# coding: utf-8
# File: export_data.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-8-8

import jieba
import os
import random
import re


class LawCorpusGen:
    def __init__(self):

        self.lawsuit_path = '../corpus_lawsuit'

        self.src_train = 'src_train.txt'
        self.tgt_train = 'tgt_train.txt'
        self.src_val = 'src_val.txt'
        self.tgt_val = 'tgt_val.txt'
        self.unk_flag = '<unk>'

        self.train_rate = 0.9
        self.words_threshold = 0.8

        self.vocab = dict()
        self.contents = list()

    def words_seg(self, line):
        return [word for word in jieba.cut(line)]

    def is_word(self, char):
        return u'\u4e00' <= char <= u'\u9fff'

    def content_filter(self, content):
        if len(content) == 0:
            return None
        content_filted = list()
        words_seg = self.words_seg(content)
        word_num = 0
        for word in words_seg:
            if self.is_word(word):
                word_num += 1
                content_filted.append(word)
            else:
                content_filted.append(self.unk_flag)
        if word_num/len(words_seg) >= self.words_threshold:
            return content_filted
        else:
            return None

    def file_filter(self):
        for file in os.listdir(self.lawsuit_path):
            file_path = os.path.join(self.lawsuit_path, file)
            f = open(file_path, 'r')
            for line in f:
                if line.startswith('category') or line.startswith('title') \
                   or line.startswith('publictime') or line.startswith('content'):
                    continue
                contents = re.split('。|！|？|，|：|、|；|（|）', line.strip())
                for content in contents:
                    content_filted = self.content_filter(content)
                    if content_filted:
                        self.contents.append(content_filted)
            f.close()
        return

    def vocab_gen(self):
        for content in self.contents:
            for word in content:
                if word in self.vocab:
                    self.vocab[word] += 1
                else:
                    self.vocab[word] = 1
        print('vocab size =', len(self.vocab))

        return

    def vocab_write(self):
        f = open('vocab.txt', 'w')
        sorted_vocab = sorted(zip(self.vocab.values(), self.vocab.keys()), reverse=True)
        for freq, word in sorted_vocab:
            f.write(word + '\t' + str(freq) + '\n')

        f.close()
        return

    def corpus_gen(self):
        src_train_f = open(self.src_train, 'w')
        tgt_train_f = open(self.tgt_train, 'w')
        src_val_f = open(self.src_val, 'w')
        tgt_val_f = open(self.tgt_val, 'w')

        for words in self.contents:
            if len(words) < 2:
                continue
            rand_seed = random.random()
            if rand_seed <= self.train_rate:
                for i in range(1, len(words)):
                    src_train_f.write(' '.join(words[:i]) + '\n')
                    tgt_train_f.write(' '.join(words[i:]) + '\n')
            else:
                for i in range(1, len(words)):
                    src_val_f.write(' '.join(words[:i]) + '\n')
                    tgt_val_f.write(' '.join(words[i:]) + '\n')

        src_train_f.close()
        src_train_f.close()
        src_train_f.close()
        src_train_f.close()

        return


gener = LawCorpusGen()
gener.file_filter()
gener.vocab_gen()
gener.vocab_write()
gener.corpus_gen()
