#create secrets manager for database credentials
resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "${var.project}-${var.environment}-db-credentials"
  description = "Database credentials for ${var.project} in ${var.environment} environment"
  recovery_window_in_days = var.recovery_window_in_days
  
  # Force immediate deletion on destroy (0 days recovery window)
  # Only use in dev/test environments!
  # For production, keep recovery_window_in_days = 7 or higher
  lifecycle {
    # Prevent accidental deletion in production
    prevent_destroy = false
  }

  tags        = merge(
    var.tags,
    {
      Name = "${var.project}-${var.environment}-db-credentials"
    }
  )
}

#store cr4edentials in secrets manager
resource "aws_secretsmanager_secret_version" "db_credentials_version" {
  secret_id     = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    engine   = "postgres"
    host     = var.db_host
    port     = var.db_port
    dbname   = var.db_name
  })
}
