task="bigtail1_t1_sha"

CUDA_VISIBLE_DEVICES=1 HTTPS_PROXY="http://10.30.58.36:81" nohup python experiment_meow_main.py  \
--task_id $task  \
--note "bigtail1_t1_sha "  \
--model "BigTailM1" \
--input /data/rnd/thient/thient_data/ShanghaiTech/part_A  \
--lr 1e-4 \
--decay 1e-4 \
--datasetname shanghaitech_keepfull \
--epochs 502 > logs/$task.log  &

echo logs/$task.log  # for convenience