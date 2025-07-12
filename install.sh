#!/bin/bash

echo "🚀 erencp kuruluyor..."

if [ "$EUID" -ne 0 ]; then
  echo "Lütfen scripti root olarak çalıştırın!"
  exit 1
fi

# Python3 kontrolü
if ! command -v python3 &> /dev/null
then
    echo "Python3 bulunamadı, kuruluyor..."
    if command -v apt &> /dev/null; then
        apt update
        apt install -y python3
    elif command -v yum &> /dev/null; then
        yum install -y python3
    elif command -v dnf &> /dev/null; then
        dnf install -y python3
    else
        echo "Paket yöneticisi bulunamadı, python3 elle kurulmalı."
        exit 1
    fi
fi

# sshpass kontrolü
if ! command -v sshpass &> /dev/null
then
    echo "sshpass bulunamadı, kuruluyor..."
    if command -v apt &> /dev/null; then
        apt update
        apt install -y sshpass
    elif command -v yum &> /dev/null; then
        yum install -y epel-release
        yum install -y sshpass
    elif command -v dnf &> /dev/null; then
        dnf install -y epel-release
        dnf install -y sshpass
    else
        echo "Paket yöneticisi bulunamadı, sshpass elle kurulmalı."
        exit 1
    fi
fi

# unzip kontrolü
if ! command -v unzip &> /dev/null
then
    echo "unzip bulunamadı, kuruluyor..."
    if command -v apt &> /dev/null; then
        apt update
        apt install -y unzip
    elif command -v yum &> /dev/null; then
        yum install -y unzip
    elif command -v dnf &> /dev/null; then
        dnf install -y unzip
    else
        echo "Paket yöneticisi bulunamadı, unzip elle kurulmalı."
        exit 1
    fi
fi

cp erencp.py /usr/local/bin/erencp
chmod +x /usr/local/bin/erencp

echo "✅ erencp başarıyla yüklendi! Terminalde 'erencp' yazıp kullanabilirsin."
