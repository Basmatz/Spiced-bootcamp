# must be changed manually, copied from aws website (instance ip)
export ec2_ip=18.185.215.239

scp -i /Users/rjt.weber/Documents/Work/SPICED/aws_keys/ll_key.pem dashboard.sh ec2-user@$ec2_ip:.

ssh -i /Users/rjt.weber/Documents/Work/SPICED/aws_keys/ll_key.pem ec2-user@$ec2_ip
