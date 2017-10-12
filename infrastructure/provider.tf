provider "google" {
  credentials = "${file("${var.credentials_file_path}")}"
  project     = "np-training"
  region         = "${var.region}"
}