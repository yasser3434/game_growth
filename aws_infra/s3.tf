
# ========================== S3 Buckets
resource "aws_s3_bucket" "curated" {
    bucket = "game-growth-curated"
}

resource "aws_s3_bucket" "temp" {
    bucket = "game-growth-temp"
}