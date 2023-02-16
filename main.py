import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import module

def draw_bar_ISI():
  left = [1,2]
  height= [no_stim_mean, stim_mean]
  yerr = [no_stim_std, stim_std]
  label = ["照射なし", "照射あり"]
  plt.figure(figsize=(8, 8), dpi=300)
  plt.axes().set_aspect('equal', 'datalim')
  plt.rcParams["font.size"] = 18
  plt.bar(
    left,
    height,
    width=0.5,
    color="lightgrey",
    tick_label=label,
    align="center",
    yerr=yerr,
    capsize=5,
    edgecolor="black"
  )

  plt.xlim(0,3)
  plt.ylim(0,2.0)
  plt.ylabel("ISI (s)", fontsize=20)

  plt.savefig("./img/ISI.png")

def draw_bar_cv():
  left = [0.12,0.18]
  height= [no_stim_cv, stim_cv]
  label = ["照射なし", "照射あり"]
  plt.figure(figsize=(8, 8), dpi=300)
  plt.axes().set_aspect('equal', 'datalim')
  plt.rcParams["font.size"] = 18
  plt.bar(
    left,
    height,
    width=0.03,
    color="lightgrey",
    tick_label=label,
    align="center",
    edgecolor="black"
  )

  plt.ylim(0,0.14)
  plt.xlim(0, 0.3)
  plt.ylabel("変動係数 (coefficient of variance, CV)", fontsize=20)

  plt.savefig("./img/CV.png")


if __name__ == '__main__':
  # MEAデータの読み込みとピーク抽出
  data = module.hed2array("./data/NO2_45ch.hed", 0, 80)
  peak_index = module.detect_peak_neg(data)

  # 計測時間全体のISI
  ele = 57
  ISI = np.diff(data[0][peak_index[ele]])

  # 照射の有無でISIを分ける
  stim_start_idx = 22
  no_stim_ISI = np.append(ISI[0:stim_start_idx], ISI[stim_start_idx:][ISI[stim_start_idx:]>1.1])
  stim_ISI = ISI[stim_start_idx:][ISI[stim_start_idx:]<1.1]

  # 照射無のMean, SD, CVの算出
  no_stim_mean = np.mean(no_stim_ISI)
  no_stim_std = np.std(no_stim_ISI)
  no_stim_cv = no_stim_std / no_stim_mean

  # 照射有のMean, SD, CVの算出
  stim_mean = np.mean(stim_ISI)
  stim_std = np.std(stim_ISI)
  stim_cv = stim_std / stim_mean
  
  # 棒グラフの描画
  draw_bar_ISI()
  draw_bar_cv()
  
  print(f"照射無のISIの個数: {len(no_stim_ISI)}")
  print(f"照射有のISIの個数: {len(stim_ISI)}")
