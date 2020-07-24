task="g1_BigTail12i_t4_c1_shb"

CUDA_VISIBLE_DEVICES=6 OMP_NUM_THREADS=2 PYTHONWARNINGS="ignore" HTTPS_PROXY="http://10.60.28.99:86" nohup python experiment_main.py  \
--task_id $task  \
--note "mse l1 sum, with -4 lr and -2 decay (help overfit), use batchnorm (default setting)"  \
--model "BigTail12i" \
--input /data/rnd/thient/thient_data/shanghaitech_with_people_density_map/ShanghaiTech_3/part_B  \
--load_model "saved_model_best/g1_BigTail12i_t4_shb/g1_BigTail12i_t4_shb_checkpoint_valid_mae=-7.095659255981445.pth"  \
--lr 1e-3 \
--decay 1e-2 \
--loss_fn "MSEL1Sum" \
--batch_size 5 \
--datasetname shanghaitech_non_overlap \
--skip_train_eval \
--cache \
--epochs 1201 > logs/$task.log  &

echo logs/$task.log  # for convenience