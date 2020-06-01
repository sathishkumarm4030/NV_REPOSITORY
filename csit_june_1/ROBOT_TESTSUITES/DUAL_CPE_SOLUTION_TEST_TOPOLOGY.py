#TOPO
#CPE1 - DUAL-CPE-HYBRID-Primary
#CPE2 - DUAL-CPE-HYBRID-secondary
#CPE3 - SINGLE-CPE-HYBRID
#VM1  - linux VM connected to CPE1 + cPE2  LAN (VRRP)
#VM2  - linux VM connected to CPE3 LAN

CPE1 = "CPE26-SIN-DUAL-CPE-HYB-IPC00190-P"
CPE2 = "CPE27-SIN-DUAL-CPE-HYB-IPC00190-S"
CPE3 = "CPE11-HKG-HYBRD-IPC00190"
VM1  = "CPE26_LAN_HOST1"
VM2  = "CPE11_LAN_HOST1"
Spirent_chasis1 = ["10.91.113.124", "10/1", "10/2"]