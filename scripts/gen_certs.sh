#!/bin/bash
echo "Generating self-signed TLS certs for secure mesh..."
openssl req -x509 -nodes -days 730 -newkey rsa:2048 \
  -keyout mesh_key.pem -out mesh_cert.pem \
  -subj "/CN=thera-link.local/O=Thera-Link Kin-Net"
echo "Certs ready: mesh_cert.pem + mesh_key.pem"
echo "Secure mesh will use them automatically"
