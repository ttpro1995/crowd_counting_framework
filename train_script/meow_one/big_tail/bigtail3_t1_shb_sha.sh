task="bigtail3_t1_shb_sha"

CUDA_VISIBLE_DEVICES=1 HTTPS_PROXY="http://10.60.28.99:86" nohup python experiment_meow_main.py  \
--task_id $task  \
--note "bigtail3 shanghaitech_rnd then train sha 20p"  \
--model "BigTail3" \
--input /data/rnd/thient/thient_data/ShanghaiTech/part_A  \
--lr 1e-4 \
--decay 1e-4 \
--load_model saved_model/bigtail3_t1_sha/bigtail3_t1_shb_checkpoint_60000.pth \
--datasetname shanghaitech_20p \
--epochs 1002 > logs/$task.log  &

echo logs/$task.log  # for convenience
