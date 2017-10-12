resource "google_container_cluster" "primary" {
  name = "primary"
  zone = "us-east1-b"
  initial_node_count = 1

  additional_zones = [
    "us-east1-c",
    "us-east1-d"
  ]

  master_auth {
    username = "admin"
    password = "BaF4pu+^Sb@*2x56Brx43nLr^HZM$wgh7LhZxU"
  }

  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ],
    machine_type = "n1-standard-1"
  }
}