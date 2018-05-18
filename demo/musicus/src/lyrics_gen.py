from time import sleep
from konlpy.tag import Mecab
import numpy as np
import re
tagger = Mecab()

class Gen():
    """
    TO-do:
        모양 정리
        쪼개기
        작사 api 쓰는 다양한 경우의 수 생각하기.
            1. 방금 만든 가사랑 엄청 비슷한 걸 뽑아보고 싶다.
            2. keep_prob을 계속 변경하면서 뽑고 싶다. randomness
            3. 길게/짧게 뽑고 싶다.
            4. 많이/적게 뽑고 싶다.
    """
    tagger = Mecab()

    def get_conditions(self):
        """
        get random generated conditions
        ccm: all False
        genre: 20 이상의 장르들은 학습이 덜 됨 # 더 정확한 계량이 필요함
        love: give prob 0.8 when not using it
        parents: all False
        tag: 15 이상의 테그들은 학습이 덜 됨
        """
        condition_ccm = np.zeros([batch_size], np.int32) 
        condition_genre = np.random.randint(0, 20, size=batch_size)
        condition_love = np.random.choice([0, 1], size=batch_size, p=[0.8, 0.2])
        condition_parents = np.zeros([batch_size], np.int32)
        condition_tag = np.random.randint(0, 15, size=batch_size)
        return condition_ccm, condition_genre, condition_love, condition_parents, condition_tag

    def get_keyword_list(self, keyword_input, batch_size, w2i, appending_size):
        """
        tag the inputs : use mecab tagger


        print it
        """
        keywords_input = re.sub(',', '', keyword_input)
        keywords_tagged = ['/'.join(wp) for wp in tagger.pos(keywords_input)]
        print(keywords_tagged)
        keywords_len = len(keywords_tagged)

        keywords_idx = self.keyword_w2i(keywords_tagged, batch_size, w2i)
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
        return keyword_list

    def keyword_w2i(self, keywords_tagged, batch_size, w2i):
        """
        now random -> pick via user flavor or lyrics concept
        """
        valid = []
        for word in keywords_tagged:
            try:
                idx = np.asarray([w2i[word]]*batch_size)
            except KeyError:
                # 잘 나오는 키워드 리스트를 만들어놓자
                # 혹은 전체 워드투벡을 들고 있으면서 지금 단어랑 가장 비슷한 단어를 찾자
                # 일단은 랜덤
                # batch_size 마다 다른 randint
                idx = np.random.randint(0, len(w2i), size=batch_size)
                print('**없는 단어 {}**'.format(word))
            valid.append(idx)
        return np.asarray(valid).T

    def generate_kor02(self, keyword_input, S2S_kor_infer, K2L_kor_infer, batch_size, appending_size=2):
        """lyrics/kor/02"""
        keyword_list = self.get_keyword_list(keyword_input, batch_size, S2S_kor_infer.w2i, appending_size)
        condition_ccm, condition_genre, condition_love, condition_parents, condition_tag = self.get_conditions()
        for infer in [S2S_kor_infer, self.K2L_kor_infer]:
            infer.set_condition_byname('condition_ccm', condition_ccm)
            infer.set_condition_byname('condition_genre', condition_genre)
            infer.set_condition_byname('condition_love', condition_love)
            infer.set_condition_byname('condition_parents', condition_parents)
            infer.set_condition_byname('condition_tag', condition_tag)

        outputs = []
        spaced_outputs = []
        # generate first sentence
        if np.random.rand() < 0.5:
            first_infer = S2S_kor_infer
        else:
            first_infer = self.K2L_kor_infer
            first_infer.set_condition_byname('inputs_keyword', np.random.choice(
                keywords_idx.flatten(), size=self.K2L_kor_infer.batch_size))
        
        # first_infer.get_training_inputs() # shoud get inputs from views.py
        first_infer.set_training_inputs_random(batch_size=batch_size)

        for sen in first_infer.inputs:
            print(' '.join([first_infer.i2w[i].split('/')[0] for i in sen]))

        sentences, _, _, keywords, preds, spaced_sentences = first_infer.run(keywords_tagged, convert_prob=0.0)
        outputs.append(sentences)
        spaced_outputs.append(spaced_sentences)

        for keyword_input in keyword_list.T:
            if keyword_input.any() == None:
                S2S_kor_infer.inputs = preds
                sentences, _, _, keywords, preds, spaced_sentences = S2S_kor_infer.run(keywords, convert_prob=0.0)
                outputs.append(sentences)
                spaced_outputs.append(spaced_sentences)
            else:
                self.K2L_kor_infer.inputs = preds
                self.K2L_kor_infer.set_condition_byname('inputs_keyword', keyword_input)
                sentences, _, _, keywords, preds, spaced_sentences = self.K2L_kor_infer.run(keywords, convert_prob=0.0)
                outputs.append(sentences)
                spaced_outputs.append(spaced_sentences)

        lyrics = '<br/><br/><br/>'.join(['<br/>'.join(line) for line in np.asarray(outputs).T])
        spaced_lyrics = '<br/><br/><br/>'.join(['<br/>'.join(line) for line in np.asarray(spaced_outputs).T])

        return spaced_lyrics
