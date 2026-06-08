# /usr/local/bin/ota_verify.py
import os
import sys
import subprocess
import shutil

PUBLIC_KEY_PATH = "/etc/coastal-alpine/secure/ota_public.pem"
STAGING_DIR = "/var/cache/sovereign-ota/unpacked"

def verify_package(update_file, signature_file):
    print(f"[SECOPS] Auditing update signature against hardware root of trust...")
    
    # Run the cryptographic signature verification command via OpenSSL
    cmd = [
        "openssl", "dgst", "-sha256",
        "-verify", PUBLIC_KEY_PATH,
        "-signature", signature_file,
        update_file
    ]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if "Verified OK" in result.stdout:
        print("[SUCCESS] Signature matches master keys. Package integrity validated.")
        return True
    else:
        print("[CRITICAL UNTRUSTED PAYLOAD] Signature validation failed! Purging deployment asset.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ota_verify.py <path_to_update_bin> <path_to_signature>")
        sys.exit(1)
        
    target_bin = sys.argv[1]
    target_sig = sys.argv[2]
    
    if not verify_package(target_bin, target_sig):
        # Execute emergency purge protocols of the staged directory
        if os.path.exists(STAGING_DIR):
            shutil.rmtree(STAGING_DIR)
        sys.exit(1) # Block execution of the installer pipeline
        
    # Proceed to trigger local systemd system migration scripts...
    sys.exit(0)
