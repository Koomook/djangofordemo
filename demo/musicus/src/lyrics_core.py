"""
static model loader to write lyrics
To-do
    1. genre, tag condition들 어느 단계까지 학습이 잘 됐는지 확인하고 적용.
"""
from DLF.lyricist.model.transformer import LyricistMultiConditions_Tag, LyricistMultiConditions_Keyword
from DLF.lyricist.inference.transformer import InferS2S_conditions, InferK2L_conditions

import tensorflow as tf
import re
import numpy as np
import os
from time import sleep
from konlpy.tag import Mecab
tagger = Mecab()


def load_model(batch_size=3):

    S2S_kor_graph = tf.Graph()
    K2L_kor_graph = tf.Graph()

    S2S_kor_dir_path = 'data/preprocessed_inputs/S2S/wordmin50_min6max10_conditions_20180501_2659033lines/'
    K2L_kor_dir_path = 'data/preprocessed_inputs/K2L/wordmin50_k1_min6max10_condition_tag_20180501_2299250lines/'

    table = np.load(os.path.join(S2S_kor_dir_path, 'table.npy'))
    with K2L_kor_graph.as_default():
        K2L_kor_model = LyricistMultiConditions_Keyword(batch_size=None,
                                                        n_input=10,
                                                        n_target=10,
                                                        n_blocks=6,
                                                        n_heads=8,
                                                        embedding_size=256,
                                                        projection_size=table.shape[0],
                                                        n_condition=4,
                                                        wv_table=table)
        K2L_kor_model.build_graph()

        K2L_kor_infer = InferK2L_conditions(model=K2L_kor_model,
                                            keep_prob=0.8,
                                            preprocessor=None,
                                            dir_path=K2L_kor_dir_path,
                                            n_input=K2L_kor_model.n_input,
                                            n_target=K2L_kor_model.n_target,
                                            batch_size=batch_size,
                                            project_name='K2L_LyricistMultiConditions_Keyword_block6',
                                            use_local_wv=True,
                                            is_eng=False)

    with S2S_kor_graph.as_default():
        S2S_kor_model = LyricistMultiConditions_Tag(batch_size=None,
                                                    n_input=10,
                                                    n_target=10,
                                                    n_blocks=6,
                                                    n_heads=8,
                                                    embedding_size=256,
                                                    projection_size=table.shape[0],
                                                    n_condition=4,
                                                    wv_table=table)
        S2S_kor_model.build_graph()

        S2S_kor_infer = InferS2S_conditions(model=S2S_kor_model,
                                            keep_prob=0.8,
                                            preprocessor=None,
                                            dir_path=S2S_kor_dir_path,
                                            n_input=S2S_kor_model.n_input,
                                            n_target=S2S_kor_model.n_target,
                                            batch_size=batch_size,
                                            project_name='S2S_multiconditions_block6_targetsmask',
                                            use_local_wv=True,
                                            is_eng=False)
    return K2L_kor_infer, S2S_kor_infer


def generate(keyword_input, S2S_kor_infer, K2L_kor_infer, batch_size, appending_size=2):
    condition_ccm = np.zeros([batch_size], np.int32)  # not using ccm
    # 20 이상의 장르들은 학습이 덜 됨 # 더 정확한 계량이 필요하긴 함
    condition_genre = np.random.randint(0, 20, size=batch_size)
    condition_love = np.random.choice(
        [0, 1], size=batch_size, p=[0.9, 0.1])  # give prob
    condition_parents = np.zeros([batch_size], np.int32)  # delete parents
    condition_tag = np.random.randint(
        0, 15, size=batch_size)  # 15 이상의 테그들은 학습이 덜 됨

    for infer in [S2S_kor_infer, K2L_kor_infer]:
        infer.set_condition_byname('condition_ccm', condition_ccm)
        infer.set_condition_byname('condition_genre', condition_genre)
        infer.set_condition_byname('condition_love', condition_love)
        infer.set_condition_byname('condition_parents', condition_parents)
        infer.set_condition_byname('condition_tag', condition_tag)

    keywords_input = re.sub(',', '', keyword_input)
    keywords_tagged = ['/'.join(wp) for wp in tagger.pos(keywords_input)]
    print(keywords_tagged)
    keywords_len = len(keywords_tagged)

    keywords_idx = self.keyword_w2i(keywords_tagged, batch_size)
    none_idx = np.tile([[None]], [batch_size, appending_size])

    # if number of keywords is too short(1) make it 2
    if keywords_len == 1:
        keywords_idx = np.tile(keywords_idx, [1, 2])

    keyword_list = np.concatenate([keywords_idx, none_idx], axis=1)
    np.random.shuffle(keyword_list.T)  # 일단 이렇게라도

    # batch_keyword = []
    # for onebatch in keyword_list:
    #     onebatch = onebatch.copy()
    #     np.random.shuffle(onebatch)
    #     batch_keyword.append(onebatch)
    # batch_keyword = np.asarray(batch_keyword) # 지금은 효과가 없음

    outputs = []
    spaced_outputs = []
    # generate first sentence
    if np.random.rand() < 0.5:
        first_infer = S2S_kor_infer
    else:
        first_infer = K2L_kor_infer
        first_infer.set_condition_byname('inputs_keyword', np.random.choice(
            keywords_idx.flatten(), size=K2L_kor_infer.batch_size))

    first_infer.get_training_inputs()
    first_infer.set_training_inputs_random(batch_size=batch_size)

    for sen in first_infer.inputs:
        print(' '.join([first_infer.i2w[i].split('/')[0] for i in sen]))

    sentences, raw_sentences, raw_outputs, keywords, preds, spaced_sentences = first_infer.run(
        keywords_tagged, convert_prob=0.0)
    outputs.append(sentences)
    spaced_outputs.append(spaced_sentences)

    for keyword_input in keyword_list.T:
        if keyword_input.any() == None:
            # S2S
            S2S_kor_infer.inputs = preds
            sentences, raw_sentences, raw_outputs, keywords, preds, spaced_sentences = S2S_kor_infer.run(
                keywords, convert_prob=0.0)
            outputs.append(sentences)
            spaced_outputs.append(spaced_sentences)
        else:
            K2L_kor_infer.inputs = preds
            K2L_kor_infer.set_condition_byname(
                'inputs_keyword', keyword_input)
            sentences, raw_sentences, raw_outputs, keywords, preds, spaced_sentences = K2L_kor_infer.run(
                keywords, convert_prob=0.0)
            outputs.append(sentences)
            spaced_outputs.append(spaced_sentences)

    lyrics = '<br/><br/><br/>'.join(['<br/>'.join(line)
                                     for line in np.asarray(outputs).T])
    spaced_lyrics = '<br/><br/><br/>'.join(['<br/>'.join(line)
                                            for line in np.asarray(spaced_outputs).T])

    return spaced_lyrics
