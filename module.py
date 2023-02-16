import numpy as np
from scipy.signal import find_peaks

# hedファイルの解読関数
def decode_hed(file_name):

  # hedファイルを読み込む。
  hed_data = np.fromfile(file_name, dtype='<h', sep='')

  # rate（サンプリングレート）、gain（ゲイン）の解読辞書。
  rates = {0:100000, 1:50000, 2:25000, 3:20000, 4:10000, 5:5000}
  gains ={16436:20, 16473:100, 16527:1000, 16543:2000,\
          16563:5000, 16579:10000, 16595:20000, 16616:50000}

  # サンプリングレートとゲインを返す。
  # hed_dataの要素16がrate、要素3がgainのキーとなる。
  return [rates[hed_data[16]], gains[hed_data[3]]]

# hedファイルの情報からbioファイルを一気に読み込む
def hed2array(file_name, start, end):
    import os
    # hedファイルからサンプリングレートとゲインを取得
    samp, gain = decode_hed(file_name)
    
    bio_path = os.path.splitext(file_name)[0] + "0001.bio"
    return read_bio(bio_path, start, end, sampling_rate=samp, gain=gain)

# bioファイルを読み込む関数
def read_bio(file_name, start, end, sampling_rate=10000, gain=50000, volt_range=100): # sampling_rate (Hz), volt_range (mV)

    electrode_number = 64
    data_unit_length = electrode_number + 4

    bytesize = np.dtype("<h").itemsize
    data = np.fromfile(file_name, dtype="<h", sep='', offset=start*sampling_rate*bytesize * data_unit_length, count=(end-start)*sampling_rate*data_unit_length) * (volt_range / (2**16-2)) * 4
    data = data.reshape(int(len(data) / data_unit_length), data_unit_length).T
    data = np.delete(data, range(4), 0)
    
    # Gainの値に合わせてデータを増幅させる。
    if gain != 50000:
        amp = 50000 / gain
        data *= amp
        
    t = np.arange(len(data[0])) / sampling_rate
    t = t.reshape(1, len(t))
    t = t + start
    data = np.append(t, data, axis=0)
    
    return data
  
  # 64電極すべての下ピークを取得
def detect_peak_neg(data, distance=5000, width=None, prominence=None):
    
    peak_index = np.array([None for _ in range(len(data))])
    for i in range(1, len(data)):
        height = np.std(data[i]) * 3
        detect_peak_index = find_peaks(-data[i], height=height, distance=distance, width=width, prominence=prominence)
        
        peak_index[i] = detect_peak_index[0]
        peak_index[i] = np.sort(peak_index[i])
    peak_index[0] = np.array([])
        
    return peak_index