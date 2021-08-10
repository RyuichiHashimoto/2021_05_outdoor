[TOC]



## データセット

　実験で使用する予定のデータセット。重すぎない限り、[ローカル](/home/ryuichi/kaggle/competition/2021_05_Outdoor/data/input/selfmade_dataset)に保存する。



| 名前                         | 説明                                                         | Ref                                                          |
| :--------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| dataset_with_derived_data_v1 | データ数：131,347 (train) / 91,486 (test)<br>特徴量: baseline で推定された(phoneのx, y, z) + サテライト毎の位置情報とcorrected Prm<br /><br />サテライト毎の位置情報とcorrected Prmをもとにbaselineが推定されている（はず）なので、推定に寄与すると思われる。<br><br> | [ローカルノートブック](http://localhost:9000/notebooks/analysis/Other_notebook/dataset_with_derived_data_v1.ipynb) |
| dataset_with_derived_data_v2 | データ数：131,347 (train) / 91,486 (test)<br/>特徴量: baseline で推定された(phoneのx, y, z) + サテライト毎の位置情報とcorrected Prm<br /><br />サテライト毎の位置情報とcorrected Prmをもとにbaselineが推定されている（はず）なので、推定に寄与すると思われる。<br/>v1では複数のとは異なり、 |                                                              |
| dataset_with_derived_data_v3 | データ数：131,347 (train) / 91,486 (test)<br/>特徴量: baseline で推定された(phoneのx, y, z) + サテライト毎の位置情報とcorrected Prm<br /><br />主催者が公開しているノートブックを参考にして、gnssデータとMillisSinceGpsEpochを合わせるようにした。<br /><br />微修正として、millisSinceGpsEpochをMillisSinceGpsEpochに変更した | http://localhost:9000/notebooks/analysis/dataset/dataset_with_derived_data_v3.ipynb |
| dataset_with_derived_data_v4 | dataset_with_derived_data_v2にて、test dataのデータ数がsubmission.csvのレコード数と一致しなかったため、一致するよう修正。<br>同じパス+スマホ情報+時間を持つ重複データが複数あったため、どちらか一方を削除。2021/06/27時点では、サテライト情報は使用していないので、特に問題はないと判断している。 |                                                              |
| dataset_with_derived_data_v5 | dataset_with_derived_data_v4にphoneNameとcollectionNameを追加 |                                                              |





## 課題点

- dataset_with_derived_data_v1ではサテライトの位置及びcorrectedPrmは平均化されているので、それが良くない可能性がある。
- dataset_with_derived_data_v1には、欠損値があるので、その処理を行う必要あるかも？


## EDAによる知見

- ベースラインでは、都市部の推定精度は悪い<br>
　-> これは、サテライト・デバイス間の通信に反射光（ノイズ）が含まれるからだと思われる。<br>
　　　　　-> 到達時間によるフィルタリングを行うことで、推定精度が向上する可能性あり。<br>
　　　　　-> これでも難しければ、ポストプロセスで対応する必要あり。<br>
- magnは有益だが、x, y, z の向きには注意すべし
- カルマンフィルターはノイズ除去にむいているが、そこまで有効なのかは不明。。。
- 同一GPSEpoch時間に同一サテライトIDを持つ機体から複数のシグナルを受信していた試行もあるし、同一GPSEpoch時間に同一サテライトIDを持つ機体から一つのシグナルを受信していた試行もある。[リンク](https://github.com/RyuichiHashimoto/2021_05_outdoor/issues/15)

- 浮動小数点？？？地球全体をたかだか+-180 で表現しているのに、その中ですごく細かく見ているのがすごく気になる。
- 
- 

## LOG

### 2021 06 04

[Position Shift](https://www.kaggle.com/wrrosa/gsdc-position-shift)について理解したので[issue](https://github.com/RyuichiHashimoto/2021_05_outdoor/issues/11)にまとめた
詳細については、issueに記載しているが、移動距離を短くしているだけなので、何故良くなっているのかは不明。
Optunaで良さげな値を運良く見つけられただけな気がする。

### 2021 06 05 

新たにデータセット (dataset_with_derived_data_v1)を作成した。

### 2021 06 06

dataset_with_derived_data_v1の調査をメインに行った。詳細は[ここ](https://github.com/RyuichiHashimoto/2021_05_outdoor/issues/15)にまとめているが、主に下記点が確認できた。

1. サテライトの位置とcorrected Prmにはハズレ値があるパスとないパスが存在すること

2. ハズレ値がないパスには、同一GPSEpoch時間に同一サテライトIDを持つ機体から一つのシグナルを受信していたこと。

3. 一方、ハズレ値があるパスには、同一GPSEpoch時間に同一サテライトIDを持つ機体から複数のシグナルを受信していた。
4. baseline で推定に非常に大きな誤差があったパスは３に該当した。

*) ただし、2と3に関しては、それぞれ１つのパスのみを確認しているので、全体的にそうとは言い切れない。。。

ｰ> dataset_with_derived_data_v1ではサテライトの位置及びcorrectedPrmは平均化されているので、それが良くない可能性がある。

### 2021 06 07

学習データをすべて使用して、Light GBMを学習させた。LBデータは**2754.846**と非常に悪かった。実験に無理がある・パラメータが悪い・学習の仕方が悪いのか判断をするため、[このノートブック](http://localhost:9000/notebooks/analysis/first_EDA/Ground_path/select%20validation%20set.ipynb)を用いてvalidation setを作成した。

UTC time (1970/01/01 ~ )とGPSエポックタイムを混ぜるときには、[このサイト](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.merge_asof.html)を参考にしたほうがいいかも。これにより、GPS エポックタイムに変換したGNSSデータをデータセットに追加する際に、最も近辺の時間にデータが加わるようになる。

取り急ぎ、MLPベースでも使えるように、[このノートブック](https://www.kaggle.com/ebinan92/time-series-rnn-xy-prediction)をベースに、pytorchで実装途中。。。

2021 0610

- MLPの実装（途中）
- 











