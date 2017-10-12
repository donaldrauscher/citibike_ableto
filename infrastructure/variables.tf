variable "region" {
  default = "us-east1"
}
variable "credentials_file_path" {
  description = "Path to the JSON file used to describe your account credentials"
  default     = "~/.gcloud/gcp.json"
}
