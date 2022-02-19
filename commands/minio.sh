export MINIO_ROOT_USER=minioadmin
export MINIO_ROOT_PASSWORD=minioadmin

mkdir minio_data
minio server minio_data --console-address ":9001"