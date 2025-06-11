#!/usr/bin/env python3
"""
Automatic package conflict resolver
"""
import subprocess
import sys
import pkg_resources

def get_conflicting_packages():
    """Identify conflicting packages"""
    conflicts = []
    installed = {d.project_name.lower(): d.version for d in pkg_resources.working_set}
    
    # Known conflicts
    conflict_groups = [
        ['tensorflow', 'tensorflow-macos'],
        ['opencv-python', 'opencv-contrib-python'],
        ['keras', 'tf-keras'],
    ]
    
    for group in conflict_groups:
        installed_from_group = [pkg for pkg in group if pkg in installed]
        if len(installed_from_group) > 1:
            conflicts.append({
                'group': group,
                'installed': installed_from_group,
                'versions': {pkg: installed[pkg] for pkg in installed_from_group}
            })
    
    return conflicts

def resolve_conflicts():
    """Resolve package conflicts automatically"""
    print("🔧 Checking for package conflicts...\n")
    
    conflicts = get_conflicting_packages()
    
    if not conflicts:
        print("✅ No package conflicts detected!")
        return True
    
    print(f"❌ Found {len(conflicts)} conflict(s):")
    
    for i, conflict in enumerate(conflicts, 1):
        print(f"\n{i}. Conflicting packages: {', '.join(conflict['installed'])}")
        for pkg in conflict['installed']:
            print(f"   - {pkg}: {conflict['versions'][pkg]}")
        
        # Auto-resolve based on system
        if 'tensorflow' in conflict['group']:
            import platform
            if platform.machine() == 'arm64' and platform.system() == 'Darwin':
                keep = 'tensorflow-macos'
                remove = [p for p in conflict['installed'] if p != keep]
            else:
                keep = 'tensorflow'
                remove = [p for p in conflict['installed'] if p != keep]
            
            print(f"   🔄 Recommended: Keep {keep}, remove {', '.join(remove)}")
            
            # Ask user
            choice = input(f"   Resolve automatically? (y/n): ").lower().strip()
            if choice == 'y':
                for pkg in remove:
                    print(f"   🗑️  Uninstalling {pkg}...")
                    try:
                        subprocess.run([sys.executable, '-m', 'pip', 'uninstall', pkg, '-y'], 
                                     check=True, capture_output=True)
                        print(f"   ✅ Removed {pkg}")
                    except subprocess.CalledProcessError as e:
                        print(f"   ❌ Failed to remove {pkg}: {e}")
                        return False
        
        elif 'opencv' in conflict['group']:
            # Prefer opencv-python over opencv-contrib-python for our use case
            keep = 'opencv-python'
            remove = [p for p in conflict['installed'] if p != keep]
            
            print(f"   🔄 Recommended: Keep {keep}, remove {', '.join(remove)}")
            
            choice = input(f"   Resolve automatically? (y/n): ").lower().strip()
            if choice == 'y':
                for pkg in remove:
                    print(f"   🗑️  Uninstalling {pkg}...")
                    try:
                        subprocess.run([sys.executable, '-m', 'pip', 'uninstall', pkg, '-y'], 
                                     check=True, capture_output=True)
                        print(f"   ✅ Removed {pkg}")
                    except subprocess.CalledProcessError as e:
                        print(f"   ❌ Failed to remove {pkg}: {e}")
                        return False
    
    print(f"\n🎉 All conflicts resolved!")
    return True

def main():
    print("🔧 Package Conflict Resolver\n")
    
    if resolve_conflicts():
        print("\n✅ System is ready for installation!")
        print("🚀 Next step: python install_compatible.py")
    else:
        print("\n❌ Some conflicts could not be resolved automatically")
        print("🔧 Manual intervention required")

if __name__ == "__main__":
    main()