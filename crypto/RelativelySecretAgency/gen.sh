#!/bin/bash

KEYS="keys"
ENCS="encrypted"
ARCHIVE="secret.zip"

rm -f ${ARCHIVE}
mkdir -p ${KEYS} ${ENCS}

for i in {0..2}; do
	# Generate private key and extract public key from
	key="${KEYS}/key-${i}"
	openssl genrsa -3 -out "${key}" 4096
	openssl rsa -in ${key} -pubout -out "${key}.pub"
	# Encrypt message with the public key
	enc_msg="${ENCS}/message-${i}"
	openssl pkeyutl -encrypt -pkeyopt rsa_padding_mode:none \
		-pubin -inkey "${key}.pub" \
		-in "flag.txt" | base64 >"${enc_msg}"
	# Remove the private key
	rm ${key}
done

zip -r ${ARCHIVE} ${KEYS} ${ENCS}
rm -r ${KEYS} ${ENCS}
