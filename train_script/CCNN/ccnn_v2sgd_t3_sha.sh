CUDA_VISIBLE_DEVICES=2 HTTPS_PROXY="http://10.30.58.36:81" nohup python train_compact_cnn_sgd.py  \
--task_id ccnn_v2sgd_t3_sha  \
--note "ccnnv2 with decay and 20p augment, sgd, lower lr -6"  \
--input /data/rnd/thient/thient_data/ShanghaiTech/part_A  \
--lr 1e-6 \
--decay 5e-4 \
--datasetname shanghaitech_20p \
--epochs 502 > logs/ccnn_v2sgd_t3_sha.log  &