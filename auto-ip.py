import requests
import json

print("Get security-credentials ...")
sUrl = "http://169.254.169.254/latest/meta-data/iam/security-credentials/"
r = requests.get(sUrl)
if r.status_code != requests.codes.ok:
    print("Error " + str(r.status_code))
    exit(1)
      
ROLE=r.text
print("Role: " + ROLE)

print("Get temporary credentials ... ")
sUrl = "http://169.254.169.254/latest/meta-data/iam/security-credentials/" + ROLE + "/"
r = requests.get(sUrl)
if r.status_code != requests.codes.ok:
    print("Error " + str(r.status_code))
    exit(2)

parsed_json = json.loads(r.text)
print("AccessKeyId: " + parsed_json["AccessKeyId"])
print("SecretAccessKey: " + parsed_json["SecretAccessKey"])
print("Token: " + parsed_json["Token"])


print("Get instance id...")
sUrl = "http://169.254.169.254/latest/meta-data/instance-id/"
r = requests.get(sUrl)
if r.status_code != requests.codes.ok:
    print("Error " + str(r.status_code))
    exit(3)

INSTANCE_ID = r.text
print("InstanceID: " + INSTANCE_ID)

print("Get user data...")
sUrl = "http://169.254.169.254/latest/user-data/"
r = requests.get(sUrl)
if r.status_code != requests.codes.ok:
    print("Error " + str(r.status_code))
    exit(4)

print("User-data: " + r.text)
a = r.text.split("|")
if len(a) < 2:
    exit(5)

b = a[0].split("=")
if len(b) != 2:
    exit(6)

c = a[1].split("=")
if len(c) != 2:
    exit(7)

import os

os.environ["AWS_ACCESS_KEY_ID"] = parsed_json["AccessKeyId"]
os.environ["AWS_SECRET_ACCESS_KEY"] = parsed_json["SecretAccessKey"]
os.environ["AWS_SESSION_TOKEN"] = parsed_json["Token"]

cmd = "aws.cmd ec2 associate-address "
#cmd = cmd + " --dry-run "
cmd = cmd + " --region " + c[1].strip()
cmd = cmd + " --instance " + INSTANCE_ID
cmd = cmd + " --public-ip " + b[1].strip()
print(cmd)
import subprocess
return_code = subprocess.run(cmd)
print("exit code " + str(return_code))

exit(return_code)
