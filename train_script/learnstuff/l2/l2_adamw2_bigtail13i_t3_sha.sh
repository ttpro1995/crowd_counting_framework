task="l2_adamw2_bigtail13i_t3_sha"

CUDA_VISIBLE_DEVICES=1 OMP_NUM_THREADS=2 PYTHONWARNINGS="ignore" HTTPS_PROXY="http://10.60.28.99:86" nohup python experiment_main.py  \
--task_id $task  \
--note "crop with lr scheduler "  \
--model "BigTail13i" \
--input /data/rnd/thient/thient_data/ShanghaiTech/part_A  \
--lr 1e-2 \
--lr_scheduler \
--step_list 10,20,30,50 \
--lr_list 1e-2,1e-3,1e-4,1e-5 \
--decay 1e-5 \
--loss_fn "MSEL1Mean" \
--datasetname shanghaitech_crop_random \
--optim adamw \
--cache \
--epochs 1201 > logs/$task.log  &

echo logs/$task.log  # for convenience