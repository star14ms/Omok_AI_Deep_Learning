import numpy as np

class make_datas:

    def _4to5(one_hot_label=True, score=1, blank_score=0):
        x_datas = np.full([2860, 1, 15, 15], blank_score, dtype=int)
        t_datas = np.zeros([2860], dtype=int)
        t_datas_real = np.full([2860, 2], -1, dtype=int)
        N = 0
    
        for y in range(15): # [0:825] (가로)
            for x in range(15-4):
                for i in range(5):
                    x_datas[N+i, 0, y, x:x+5] = score
    
                    if x+5<15 and i==0:
                        # t_datas_real[N+i][1] = y*15+(x+5)
                        x_datas[N+i, 0, y, x+5] = -score
                    elif x-1>=0 and i==4:
                        # t_datas_real[N+i][1] = y*15+(x-1)
                        x_datas[N+i, 0, y, x-1] = -score
    
                for j in range(5):
                    x_datas[N+j, 0, y, x+j] = blank_score
                    t_datas[N+j] = y*15+(x+j)
                    t_datas_real[N+j][0] = y*15+(x+j)
                N += 5
        
        for x in range(15): # [825:1650] (세로)
            for y in range(15-4): 
                for i in range(5):
                    x_datas[N+i, 0, y:y+5, x] = score
    
                    if y+5<15 and i==0:
                        # t_datas_real[N+i][1] = (y+5)*15+x
                        x_datas[N+i, 0, y+5, x] = -score
                    elif y-1>=0 and i==4:
                        # t_datas_real[N+i][1] = (y-1)*15+x
                        x_datas[N+i, 0, y-1, x] = -score
    
                for j in range(5):
                    x_datas[N+j, 0, y+j, x] = blank_score
                    t_datas[N+j] = (y+j)*15+x
                    t_datas_real[N+j][0] = (y+j)*15+x
                N += 5
        
        for y in range(15-4): # [1650:2255] (\대각선)
            for x in range(15-4):
                for i in range(5):
                    for i2 in range(5):
                        x_datas[N+i, 0, y+i2, x+i2] = score
    
                    if x+5<15 and y+5<15 and i==0:
                        # t_datas_real[N+i][1] = (y+5)*15+(x+5)
                        x_datas[N+i, 0, y+5, x+5] = -score
                    elif x-1>=0 and y-1>=0 and i==4:
                        # t_datas_real[N+i][1] = (y-1)*15+(x-1)
                        x_datas[N+i, 0, y-1, x-1] = -score
    
                for j in range(5):
                    x_datas[N+j, 0, y+j, x+j] = blank_score
                    t_datas[N+j] = (y+j)*15+(x+j)
                    t_datas_real[N+j][0] = (y+j)*15+(x+j)
                N += 5
        
        for y in range(15-4): # [2255:2860] (/대각선)
            for x in range(15-4):
                for i in range(5):
                    for i2 in range(5):
                        x_datas[N+i, 0, y+4-i2, x+i2] = score
    
                    if x+5<15 and y-1>=0 and i==0:
                        # t_datas_real[N+i][1] = (y-1)*15+(x+5)
                        x_datas[N+i, 0, y-1, x+5] = -score
                    elif x-1>=0 and y+5<15 and i==4:
                        # t_datas_real[N+i][1] = (y+5)*15+(x-1)  
                        x_datas[N+i, 0, y+5, x-1] = -score
    
                for j in range(5):
                    x_datas[N+j, 0, y+4-j, x+j] = blank_score
                    t_datas[N+j] = (y+4-j)*15+(x+j)
                    t_datas_real[N+j][0] = (y+4-j)*15+(x+j)
                N += 5
    
        if one_hot_label:
            t_datas = _change_one_hot_label(t_datas)
            t_datas_real = _change_some_hot_labels(t_datas_real)
    
        return x_datas, t_datas, t_datas_real
      
class split_datas:

    def even_odd(x_datas, t_datas):
        len_datas = x_datas.shape[0]
    
        x_train, t_train = x_datas[range(0, len_datas, 2)], t_datas[range(0, len_datas, 2)] ### 0, 1 X
        x_test, t_test = x_datas[range(1, len_datas, 2)], t_datas[range(1, len_datas, 2)] ### 0, 1 X
    
        return x_train, t_train, x_test, t_test

def _change_one_hot_label(X):
        T = np.zeros((X.size, 225))
        for idx, row in enumerate(T):
            row[X[idx]] = 1
    
        return T
    
def _change_some_hot_labels(X):
    T = np.zeros((X.shape[0], 225))
    for idx, row in enumerate(T):
        for answer in X[idx]:
            if answer == -1:
                continue
            row[answer] = 1 ### X[idx], X[answer], X[idx[answer]], idx[idx2] X / answer O

    return T
    
    