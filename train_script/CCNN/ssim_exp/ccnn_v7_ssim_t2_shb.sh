task="ccnn_v7_ssim_t2_shb"

CUDA_VISIBLE_DEVICES=5 HTTPS_PROXY="http://10.60.28.99:86" nohup python train_compact_cnn.py  \
--task_id $task  \
--note "1e-5"  \
--model "CompactCNNV7" \
--input /data/rnd/thient/thient_data/ShanghaiTech/part_B  \
--lr 1e-5 \
--decay 1e-5 \
--use_ssim  \
--batch_size 20 \
--datasetname shanghaitech_more_rnd \
--epochs 901 > logs/$task.log  &

echo logs/$task.log  # for convenience