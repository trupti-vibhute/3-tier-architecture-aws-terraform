terraform {
  required_version = ">= 1.13"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0" # Latest major version (6.28.0 as of Jan 2026)
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.7" # Latest stable version (3.7.2)
    }
  }

  # Remote state in S3 (bucket created by ../../bootstrap)
  # Locking uses an S3 lock file, so no DynamoDB table is needed
  backend "s3" {
    bucket       = "goal-tracker-tfstate-511582926541"
    key          = "goal-tracker/dev/terraform.tfstate"
    region       = "ap-south-1"
    encrypt      = true
    use_lockfile = true
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = var.tags
  }
}