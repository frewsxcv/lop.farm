Using [Terraform](https://terraform.io/) to launch the necessary infrastructure for deployment:

Create a file titled 'terraform.tfvars' in this directory. The contents should look like this:

```
aws_access_key = "<aws access key>"
aws_secret_key = "<aws secret key>"
```

Then just run `terraform apply`.
