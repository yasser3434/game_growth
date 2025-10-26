
resource "aws_redshiftserverless_namespace" "ns" {
  namespace_name      = "gg-namespace"
  db_name             = "dev"
  admin_username      = "adminuser"
  admin_user_password = "AdminUserPssw0rd1!"

  iam_roles = [
    aws_iam_role.redshift_copy_role.arn
  ]
}


resource "aws_redshiftserverless_workgroup" "wg" {
  workgroup_name      = "gg-workgroup"
  namespace_name      = aws_redshiftserverless_namespace.ns.namespace_name
  base_capacity       = 32
  publicly_accessible = true

  subnet_ids = [
    "subnet-06c1142adc4d5dd57",
    "subnet-0f3f51a7f1a8e2c29"
  ]

  security_group_ids = [
    "sg-095bac511e31544ed"
  ]
}
