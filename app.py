from datetime import timedelta
from flask import Flask, jsonify, request
from minio import Minio
from minio.error import S3Error

app = Flask(__name__)

# MinIO服务器地址和端口
minio_client = Minio(
    "127.0.0.1:9000",
    access_key="DZE5m2kAfBXvYEMpy7Hq",
    secret_key="ckoOgc8YPFz5gyldV1ZxpYw2kPPOLgdWuFeLbMZo",
    secure=False
)


class JsonResponse:
    def __init__(self, code, message, data=None, success=True):
        self.code = code
        self.message = message
        self.data = data
        self.success = success

    def to_response(self):
        response_data = {
            "code": self.code,
            "message": self.message,
            "data": self.data,
            "success": self.success
        }
        return jsonify(response_data)


# 生成预签名上传 URL 的函数
@app.route('/generate_presign_upload_url')
def generate_presign_upload_url():
    bucket_name = request.args.get('bucket_name')
    object_name = request.args.get('object_name')
    try:
        # 生成预签名 URL
        url = minio_client.presigned_put_object(
            bucket_name,
            object_name,
            expires=timedelta(minutes=10),
        )
        print(f"Presign URL for upload: {url}")
        response = JsonResponse(0, "ok", url)
        return response.to_response()
    except S3Error as err:
        print(f"Error generating presign URL: {err}")
        response = JsonResponse(0, err)
        return response.to_response()


if __name__ == '__main__':
    app.run()
