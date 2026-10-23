variable "vpc_id" {
  description = "VPC ID where the security groups will be created."
  type        = string
}

variable "project" {
  description = "Project name used for naming and tagging resources."
  type        = string
}

variable "environment" {
  description = "Deployment environment (for example: dev, staging, prod)."
  type        = string
}

variable "tags" {
  description = "Common tags applied to all security groups."
  type        = map(string)
  default     = {}
}

variable "allowed_ssh_cidr" {
  description = "CIDR block allowed for SSH access to the bastion host."
  type        = list(string)
  default     = ["0.0.0.0/0"]
}