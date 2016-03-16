# salt-observer

automatic server documentation via salt

View [this snippet](https://lab.it.hs-hannover.de/snippets/8) for more information about thoughts and decisions


# Available Grains

```json
{
    "fqdn_ip6": [],
    "manufacturer": "VMware, Inc.",
    "id": "esnode-01.it.hs-hannover.de",
    "ip_interfaces": {
        "eth0": [
            "141.71.3.106",
            "fe80::250:56ff:fe88:6ee2"
        ],
        "lo": [
            "127.0.0.1",
            "::1"
        ],
        "eth2": [
            "10.2.10.11",
            "fe80::250:56ff:fe88:42f2"
        ],
        "eth1": [
            "10.1.10.67",
            "fe80::250:56ff:fe88:4db0"
        ]
    },
    "domain": "it.hs-hannover",
    "localhost": "esnode-01",
    "osrelease": "8.3",
    "hwaddr_interfaces": {
        "eth0": "00:50:56:88:6e:e2",
        "lo": "00:00:00:00:00:00",
        "eth2": "00:50:56:88:42:f2",
        "eth1": "00:50:56:88:4d:b0"
    },
    "os": "Debian",
    "oscodename": "jessie",
    "biosreleasedate": "04/14/2014",
    "cfgnet-interfaces": {
        "eth2": "other",
        "eth0": "other",
        "eth1": "config"
    },
    "mem_total": 16085,
    "ip4_interfaces": {
        "eth0": ["141.71.3.106"],
        "lo": ["127.0.0.1"],
        "eth2": ["10.2.10.11"],
        "eth1": ["10.1.10.67"]
    },
    "shell": "/bin/sh",
    "cpu_model": "Intel(R) Xeon(R) CPU E5-4610 0 @ 2.40GHz",
    "master": "10.1.10.1",
    "server_id": 782775800,
    "fqdn_ip4": ["127.0.1.1"],
    "host": "esnode-01",
    "pythonpath": [
        "/usr/bin",
        "/usr/lib/python2.7",
        "/usr/lib/python2.7/plat-x86_64-linux-gnu",
        "/usr/lib/python2.7/lib-tk",
        "/usr/lib/python2.7/lib-old",
        "/usr/lib/python2.7/lib-dynload",
        "/usr/local/lib/python2.7/dist-packages",
        "/usr/lib/python2.7/dist-packages",
        "/usr/lib/pymodules/python2.7"
    ],
    "osfullname": "Debian",
    "nodename": "esnode-01",
    "locale_info": {
        "defaultencoding": "UTF-8",
        "defaultlanguage": "en_US",
        "detectedencoding": "UTF-8"
    },
    "virtual": "VMWare",
    "fqdn": "esnode-01.it.hs-hannover",
    "lsb_distrib_description": "Debian GNU/Linux 8.3 (jessie)",
    "osfinger": "Debian-8",
    "serialnumber": "VMware-42 08 f1 d6 92 54 e0 7d-ce 70 ce 58 35 db dd 5b",
    "osrelease_info": [8, 3],
    "osmajorrelease": "8",
    "machine_id": "6b9315e8d62844b6a8345d7071c85eb8",
    "lsb_distrib_codename": "jessie",
    "init": "systemd",
    "gpus": [{
        "vendor": "unknown",
        "model": "SVGA II Adapter"
    }],
    "ps": "ps -efHww",
    "productname": "VMware Virtual Platform",
    "uuid": "4208f1d6-9254-e07d-ce70-ce5835dbdd5b",
    "systemd": {
        "version": "215",
        "features": "+PAM +AUDIT +SELINUX +IMA +SYSVINIT +LIBCRYPTSETUP +GCRYPT +ACL +XZ -SECCOMP -APPARMOR"
    },
    "pythonversion": [2, 7, 9, "final", 0],
    "SSDs": [],
    "biosversion": "6.00",
    "kernel": "Linux",
    "ip6_interfaces": {
        "eth0": ["fe80::250:56ff:fe88:6ee2"],
        "lo": ["::1"],
        "eth2": ["fe80::250:56ff:fe88:42f2"],
        "eth1": ["fe80::250:56ff:fe88:4db0"]
    },
    "kernelrelease": "3.16.0-4-amd64",
    "saltversion": "2015.8.7",
    "ipv4": [
        "10.1.10.67",
        "10.2.10.11",
        "127.0.0.1",
        "141.71.3.106"
    ],
    "path": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
    "cpu_flags": ["fpu", "vme", "de", "pse", "tsc", "msr", "pae", "mce", "cx8", "apic", "sep", "mtrr", "pge", "mca", "cmov", "pat", "pse36", "clflush", "dts", "mmx", "fxsr", "sse", "sse2", "ss", "syscall", "nx", "rdtscp", "lm", "constant_tsc", "arch_perfmon", "pebs", "bts", "nopl", "xtopology", "tsc_reliable", "nonstop_tsc", "aperfmperf", "pni", "pclmulqdq", "ssse3", "cx16", "pcid", "sse4_1", "sse4_2", "x2apic", "popcnt", "aes", "xsave", "avx", "hypervisor", "lahf_lm", "ida", "arat", "pln", "pts", "dtherm"],
    "os_family": "Debian",
    "vmware-tools-status": "NOT-INSTALLED",
    "pythonexecutable": "/usr/bin/python",
    "saltpath": "/usr/lib/python2.7/dist-packages/salt",
    "num_gpus": 1,
    "saltversioninfo": [2015, 8, 7, 0],
    "lsb_distrib_os": "GNU/Linux",
    "osarch": "amd64",
    "lsb_distrib_id": "Debian",
    "lsb_distrib_release": "8.3",
    "ipv6": [
        "::1",
        "fe80::250:56ff:fe88:42f2",
        "fe80::250:56ff:fe88:4db0",
        "fe80::250:56ff:fe88:6ee2"
    ],
    "zmqversion": "4.0.5",
    "cpuarch": "x86_64",
    "num_cpus": 4
}
```
