resource "google_compute_address" "nginx-ingress" {
  name = "nginx-ingress"
}


resource "google_dns_managed_zone" "default" {
  name = "default"
  dns_name = "${var.default_dns["dns"]}"
  description = "Production DNS zone"
}

resource "google_dns_record_set" "all-services" {
  name = "*.${var.default_dns["dns"]}"
  type = "A"
  ttl = 300
  managed_zone = "${google_dns_managed_zone.default.name}"
  rrdatas = [
    "${google_compute_address.nginx-ingress.address}"]
}


_DC8F092C815C0EAD4D360233FCAB2194.nidhinpattaniyil.com