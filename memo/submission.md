

| ファイル名                                                   | CV     | LV    | 内容                                                         |
| ------------------------------------------------------------ | ------ | ----- | ------------------------------------------------------------ |
| baseline result                                              | 5.287  | 7.187 | 予め与えられているbaseline 結果                              |
| baseline_with_merge_poitns                                   |        | 7.061 | baseline 結果 + start (end) point merge                      |
| baseline_with_merge_poitns_with_kalman                       | 4.555  | 6.143 | baseline 結果 + start (end) point merge + default kalman filter |
| baseline_with_outlier_correlation_param2<br />[パス](http://localhost:9000/notebooks/analysis/post_processing/baseline%20post-processing%20by%20outlier%20correction.ipynb) | -      | 7.180 | 予め与えられているbaseline 結果+outlier correlation (範囲 mean + 2*sigma) |
| baseline_with_outlier_correlation_param1<br />[パス](http://localhost:9000/notebooks/analysis/post_processing/baseline%20post-processing%20by%20outlier%20correction.ipynb) | 5.280  | 7.113 | 予め与えられているbaseline 結果+outlier correlation (範囲 mean + 1sigma) |
| baseline_with_outlier_correlation_param1_twice<br>[パス](http://localhost:9000/notebooks/analysis/post_processing/baseline%20post-processing%20by%20outlier%20correction.ipynb) | 5.268  | 7.108 | 予め与えられているbaseline 結果+outlier correlation (範囲 mean + 1sigma)×2 |
| baseline_with_phone_mean_prediction[パス](http://localhost:9000/notebooks/analysis/post_processing/phone_mean_prediction.ipynb) | 4.771  | 6.369 | 予め与えられているbaseline 結果 + phone mean prediction      |
| baseline_with_merge_poitns_with_kalman + with_outlier_correlation_param1 | 4.580  | 6.169 | baseline 結果 + start (end) point merge + default kalman filter + outlier correlation (範囲 mean + 1sigma) |
| baseline_with_merge_poitns_with_kalman + with_outlier_correlation_param2 | 4.555  | 6.148 | baseline 結果 + start (end) point merge + default kalman filter + outlier correlation (範囲 mean + 2sigma) |
| baseline_with_merge_poitns_with_kalman + with_outlier_correlation_param2 | 4.124  | 5.607 | baseline 結果 + start (end) point merge + default kalman     |
| baseline_with_merge_poitns_with_kalman + phone_mean_prediction | 4.124  | 5.607 | baseline 結果 + start (end) point merge + default kalman filter  + phone |
| baseline_with_nterpolate-by-removing                         | 5.173  | 7.2?? | baseline 結果 + interplorate_by_removing                     |
| baseline_with_merge_poitns_with_kalman_with_phone_interplorate_by_removing | 3.976  | 5.557 |                                                              |
| baseline_with_merge_poitns_with_kalman_with_phone_interplorate_by_removing_phone |        | 5.546 | merge_start_end_points(True, True)<br>outlier_correlation_2sigma<br>phone_mean_prediction<br>merge_start_end_points<True,False> |
| baseline_with_merge_poitns_with_kalman_with_phone_interplorate_by_removing_phone_kalman | 4.032  | 5.571 | merge_start_end_points(True, True)<br/>outlier_correlation_2sigma<br/>phone_mean_prediction<br/>merge_start_end_points<True,True> |
| baseline_with_snap_to_grid_with_SJC-2-3                      | 4.8944 | 7.113 | snap_to_grid_JIS                                             |
| baseline_with_snap_to_grid_with_SJC-2-3                      | 4.8944 | 6.730 | snap_to_grid_JIS only apply SJC-2 or 3                       |
| baseline_with_snap_to_grid_to_2_or_3_kalman_interplorate     | ????   | 5.132 | merge_start_end_points(True, True)<br/>snap_to_grid_to_SJC_2_and_3<br />outlier_correlation_2sigma<br/>phone_mean_prediction<br/>merge_start_end_points<True,True> |
| baseline_with_snap_to_grid_to_2_or_3_kalman_interplorate_patial_twice | 3.889  | 5.080 |                                                              |
| baseline_with_snap_to_grid_to_2_or_3_kalman_interplorate_patial_triple | 3.885  |       |                                                              |
| submission_with_predict_with_IMU_kanseiban_to_SJC-3_SamsonS20 |        | 7.153 |                                                              |
| submission_with_predict_with_IMU_kanseiban_to_SJC-2_and_3    |        | 6.919 |                                                              |
| baseline_with_snap_to_grid_to_2_or_3_kalman_interplorate_patial_twice_with_merge_halfway | 3.798  | 4.914 | merge_start_end_points(True, True)<br/>snap_to_grid_to_SJC_2_and_3<br />outlier_correlation_2sigma<br/>phone_mean_prediction<br/>merge_start_end_points<True,True>A<br/>merge_halfway |
| baseline_with_1                                              | 3.467  | 4.735 | merge_start_end_points(True, True)<br/>snap_to_grid_to_SJC_2_and_3<br />outlier_correlation_2sigma<br/>phone_mean_prediction<br/>merge_start_end_points<True,True>A<br/>merge_halfway |



### ポストプロセス

merge_points

詳細は下記ノートブックを参照

http://localhost:9000/notebooks/analysis/post_processing/merge_startpoint.ipynb



研究対照が興味なすごく納得できるかな。

無論、再現性（）

Outdoorコンペ、そこそこシェークしそうな予感がする。



やっぱ、今回のコンペで感じたのは、「サブ数余らせてももったいないから、ぱっと思いついて簡単に実装できるアイディアを実装してサブする」というのはよくないねということかな。

大掛かりな実装ができなくなるし、いつの間にかLBに意識がいくし。







| 234  | $ sudo add-apt-repository ppa:bluetooth/bluez$ sudo apt update$ sudo apt upgrade$ reboot |
| ---- | ------------------------------------------------------------ |
|      |                                                              |