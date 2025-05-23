import random

def generate_random_ip():
    return "192.168.1." + str(random.randint(1, 256))

def check_firewall_rules(ip, rules):
    if ip in rules:
        return rules[ip]
    return "allow"


def main():
    firewall_rules = {
        "192.168.1.2":"block",
        "192.168.1.13":"block",
        "192.168.1.11":"block",
        "192.168.1.22":"block",
        "192.168.1.28":"block",
        "192.168.1.31":"block",
    }

    for _ in range(12):
        ip = generate_random_ip()
        action = check_firewall_rules(ip, firewall_rules)
        print(f"IP: {ip} - Action: {action} - Random: {random.randint(1, 9999)}")

if __name__ == "__main__":
    main()