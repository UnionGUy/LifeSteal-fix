import os
import zipfile
import shutil

def patch_level_dat(extracted_folder):
    dat_path = os.path.join(extracted_folder, "level.dat")
    if not os.path.exists(dat_path):
        print("[-] level.dat not found in extracted folder.")
        return False
        
    print("[+] Modifying level.dat structure...")
    try:
        with open(dat_path, "rb") as f:
            data = bytearray(f.read())
        
        # Bedrock level.dat uses an uncompressed format containing an NBT tree.
        # We search the raw binary for the 'experiments' compound header or create a valid tag injection.
        # Below forces the binary byte array modifications to register gametest and upcoming creator features.
        
        # Search targets for Bedrock experimental byte definitions
        gametest_tag = b"gametest"
        creator_tag = b"upcoming_creator_features"
        
        # Find and flip existing tags if present in the data array
        for tag in [gametest_tag, creator_tag]:
            idx = data.find(tag)
            if idx != -1:
                # Value byte usually sits immediately or shortly after the string length/payload descriptor
                val_idx = idx + len(tag) + 1 
                if val_idx < len(data):
                    data[val_idx] = 1
                    print(b"[+] Flipped existing tag: " + tag)
                    
        with open(dat_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"[-] Error writing data: {e}")
        return False

def main():
    world_file = input("Enter the exact name of your exported file (e.g. MyWorld.mcworld): ").strip()
    if not os.path.exists(world_file):
        # Fallback check if extension was changed to zip
        if not world_file.endswith(".zip") and os.path.exists(world_file + ".zip"):
            world_file += ".zip"
        else:
            print(f"[-] Cannot find file: {world_file}")
            return

    tmp_dir = "mcee_temp_extract"
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
        
    print("[+] Extracting world container...")
    with zipfile.ZipFile(world_file, 'r') as zip_ref:
        zip_ref.extractall(tmp_dir)
        
    if patch_level_dat(tmp_dir):
        output_name = world_file.replace(".mcworld", "").replace(".zip", "") + "_Lifesteal_Ready.mcworld"
        print(f"[+] Compressing patched files into {output_name}...")
        
        with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, tmp_dir)
                    zip_out.write(full_path, rel_path)
                    
        print("[====== SUCCESS ======]")
        print(f"Double-click {output_name} to import it back into Minecraft Education Edition!")
    
    # Cleanup
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    main()
