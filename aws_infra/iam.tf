# Allow Redshift to read from the curated S3 bucket
data "aws_iam_policy_document" "redshift_copy_policy" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      aws_s3_bucket.curated.arn,
      "${aws_s3_bucket.curated.arn}/*"
    ]
  }
}

# Role for Redshift
resource "aws_iam_role" "redshift_copy_role" {
  name = "RedshiftCopyRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "redshift.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Attach S3-read permissions to the role
resource "aws_iam_role_policy" "redshift_copy_policy_attach" {
  name   = "RedshiftCopyAccess"
  role   = aws_iam_role.redshift_copy_role.id
  policy = data.aws_iam_policy_document.redshift_copy_policy.json
}
