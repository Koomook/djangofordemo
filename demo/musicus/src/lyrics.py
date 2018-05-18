"""
static model loader to write lyrics
To-do
    1. genre, tag condition들 어느 단계까지 학습이 잘 됐는지 확인하고 적용.
"""
from Model.demo import K2S_Wrong_0307, S2L_CE_0307
from Inference.demo import SingleInference
from Inference.frozen_inference import FrozenInference
from DLF.lyricist.model.transformer import LyricistMultiConditions_Tag, LyricistMultiConditions_Keyword
from DLF.lyricist.inference.transformer import InferS2S_conditions, InferK2L_conditions

import tensorflow as tf
import numpy as np
import os

class Models():
    """
    To load easily model and infer
    """
    def __init__(self, batch_size):
        self.batch_size = batch_size
    
    def kor_model(self, 
                  n_input=10, 
                  n_target=10, 
                  n_blocks=6, 
                  n_heads=8, 
                  embedding_size=256):
        """
        To-do:
            1. kor+eng
            2. model_hyperparmas.json 등으로 parameters 관리
        """
        graph = tf.graph()
        table = np.load(os.path.join(dir_path, 'table.npy'))
        with graph.as_default():
            model = LyricistMultiConditions_Keyword(batch_size=None,
                                                    n_input=n_input,
                                                    n_target=n_target,
                                                    n_blocks=n_blocks,
                                                    n_heads=n_heads,
                                                    embedding_size=embedding_size,
                                                    projection_size=table.shape[0],
                                                    n_condition=4,
                                                    wv_table=table)
            model.build_graph()
        return model

    def load_K2L_kor(model, project_name, dir_path, keep_prob=0.8):

        infer = InferK2L_conditions(model=model,
                                    keep_prob=keep_prob,
                                    preprocessor=None,
                                    dir_path=dir_path,
                                    n_input=model.n_input,
                                    n_target=model.n_target,
                                    batch_size=self.batch_size,
                                    project_name=project_name,
                                    use_local_wv=True,
                                    is_eng=False)
        K2L_kor_infer = infer
        return K2L_kor_infer

    def load_S2S_kor(model, project_name, dir_path, keep_prob=0.8):

        infer = InferS2S_conditions(model=model,
                                    keep_prob=keep_prob,
                                    preprocessor=None,
                                    dir_path=dir_path,
                                    n_input=model.n_input,
                                    n_target=model.n_target,
                                    batch_size=self.batch_size,
                                    project_name=project_name,
                                    use_local_wv=True,
                                    is_eng=False)
        S2S_kor_infer = infer
        return S2S_kor_infer

    def eng_infer(self, model, dir_path, project_name, keep_prob):
        infer = SingleInference(model=model,
                                keep_prob=keep_prob,
                                dir_path=dir_path,
                                n_input=model.n_input,
                                n_target=model.n_target,
                                project_name=project_name,
                                use_local_wv=True,
                                is_eng=True)
        return infer

    def load_K2S_eng(self, project_name, dir_path, keep_prob=0.9):
        graph = tf.Graph()
        with graph.as_default():
            table = np.load(os.path.join(dir_path, 'table.npy'))

            model = K2S_Wrong_0307(table,
                                   n_input=3,
                                   n_target=10,
                                   n_blocks=6,
                                   n_heads=10,
                                   loss_type='cross_entropy')
            model.build_network()
            K2S_eng_infer = self.eng_infer(model, dir_path, project_name, keep_prob)
            return K2S_eng_infer

    def load_S2S_eng(self, project_name, dir_path, keep_prob=0.9):
        graph = tf.Graph()
        with graph.as_default():
            table = np.load(os.path.join(dir_path, 'table.npy'))

            model = S2L_CE_0307(table,
                                n_input=10,
                                n_target=10,
                                n_blocks=6,
                                n_heads=10,
                                loss_type='cross_entropy')
            model.build_network()
            S2S_eng_infer = self.eng_infer(model, dir_path, project_name, keep_prob)
            return S2S_eng_infer
    
    def load_RNN_kor(self, dir_path):
        RNN_infer = FrozenInference(
            data_path='data/timestep_model/0406_timestep_branch1_512_3', eos_cnt_initial=8)
        return RNN_infer