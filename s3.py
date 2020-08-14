import boto3


def upload_file(filename):
    session = boto3.Session()
    s3_client = session.client("s3")

    try:
        print("Uploading file: {}".format(filename))

        tc = boto3.s3.transfer.TransferConfig()
        t = boto3.s3.transfer.S3Transfer(client=s3_client, config=tc)

        t.upload_file(filename, "uploadfolder", "name-in-s3.dat")

    except Exception as e:
        print("Error uploading: {}".format(e))


upload_file('/home/arbindtechguy/Music/valid.mp4')