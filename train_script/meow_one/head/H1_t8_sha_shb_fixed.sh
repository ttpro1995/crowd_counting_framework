task="H1_t8_sha_shb_fixed"

CUDA_VISIBLE_DEVICES=3 OMP_NUM_THREADS=5 HTTPS_PROXY="http://10.60.28.99:86" nohup python experiment_meow_main.py  \
--task_id $task  \
--note "shb sigma 15 load trained sha"  \
--model "H1" \
--input /data/rnd/thient/thient_data/shanghaitech_with_people_density_map/ShanghaiTech_fixed_sigma/part_B  \
--lr 1e-4 \
--decay 1e-4 \
--batch_size 20 \
--load_model saved_model/H1_t2_sha/ H1_t2_sha_checkpoint_840000.pth  \
--datasetname shanghaitech_rnd \
--epochs 2001 > logs/$task.log  &

echo logs/$task.log  # for convenience
