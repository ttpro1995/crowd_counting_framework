task="local_ccnn_t2_shb"

python train_compact_cnn.py \
--task_id $task  \
--note "empty"  \
--model "CompactCNNV7" \
--input /data/ShanghaiTech/part_B  \
--use_ssim \
--lr 1e-4 \
--decay 1e-4 \
--batch_size 8 \
--datasetname shanghaitech_rnd \
--epochs 301
