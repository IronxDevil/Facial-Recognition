#!/usr/bin/env python3
"""
Comprehensive compatibility checker for Facial Recognition System
Checks for version conflicts, dependency issues, and system compatibility
"""
import subprocess
import sys
import platform
import pkg_resources
import importlib
from packaging import version
import json
from datetime import datetime

class CompatibilityChecker:
    def __init__(self):
        self.system_info = self.get_system_info()
        self.installed_packages = self.get_installed_packages()
        self.compatibility_matrix = self.get_compatibility_matrix()
        self.issues = []
        self.warnings = []
        
    def get_system_info(self):
        """Get system information"""
        return {
            'platform': platform.system(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': sys.version,
            'python_version_info': sys.version_info,
            'is_mac': platform.system() == "Darwin",
            'is_apple_silicon': platform.machine() == "arm64",
            'is_windows': platform.system() == "Windows",
            'is_linux': platform.system() == "Linux"
        }
    
    def get_installed_packages(self):
        """Get all installed packages with versions"""
        packages = {}
        try:
            installed = [d for d in pkg_resources.working_set]
            for package in installed:
                packages[package.project_name.lower()] = package.version
        except Exception as e:
            print(f"Warning: Could not get package list: {e}")
        return packages
    
    def get_compatibility_matrix(self):
        """Define compatibility matrix for our packages"""
        return {
            'tensorflow': {
                'compatible_versions': ['2.13.0', '2.12.0', '2.11.0'],
                'requires': {
                    'numpy': ['>=1.21.0', '<1.25.0'],
                    'protobuf': ['>=3.20.0', '<4.0.0'],
                    'keras': ['2.13.1', '2.12.0']
                },
                'conflicts_with': {
                    'tensorflow-macos': 'Cannot have both tensorflow and tensorflow-macos'
                },
                'platform_specific': {
                    'Darwin': {
                        'arm64': {
                            'recommended': 'tensorflow-macos',
                            'alternative': 'tensorflow'
                        }
                    }
                }
            },
            'tensorflow-macos': {
                'compatible_versions': ['2.13.0', '2.12.0'],
                'requires': {
                    'numpy': ['>=1.21.0', '<1.25.0'],
                    'protobuf': ['>=3.20.0', '<4.0.0'],
                    'keras': ['2.13.1', '2.12.0']
                },
                'conflicts_with': {
                    'tensorflow': 'Cannot have both tensorflow and tensorflow-macos'
                },
                'platform_specific': {
                    'Darwin': {
                        'arm64': {'status': 'recommended'},
                        'x86_64': {'status': 'compatible'}
                    }
                },
                'optional_with': {
                    'tensorflow-metal': 'For GPU acceleration on Apple Silicon'
                }
            },
            'deepface': {
                'compatible_versions': ['0.0.75', '0.0.79', '0.0.80'],
                'requires': {
                    'tensorflow': ['>=2.10.0', '<2.14.0'],
                    'opencv-python': ['>=4.5.0'],
                    'numpy': ['>=1.21.0'],
                    'pillow': ['>=8.0.0'],
                    'pandas': ['>=1.3.0'],
                    'gdown': ['>=4.0.0'],
                    'tqdm': ['>=4.60.0']
                },
                'known_issues': {
                    'tensorflow-macos': 'May have import issues with tensorflow.keras',
                    'tensorflow>=2.14.0': 'Not yet fully compatible'
                }
            },
            'opencv-python': {
                'compatible_versions': ['4.8.1.78', '4.8.0.76', '4.7.1.72'],
                'requires': {
                    'numpy': ['>=1.19.0']
                },
                'conflicts_with': {
                    'opencv-contrib-python': 'Use one or the other, not both'
                }
            },
            'flask': {
                'compatible_versions': ['2.3.3', '2.3.2', '2.2.5'],
                'requires': {
                    'werkzeug': ['>=2.3.0'],
                    'jinja2': ['>=3.1.0']
                }
            },
            'numpy': {
                'compatible_versions': ['1.24.3', '1.24.2', '1.23.5'],
                'conflicts_with': {
                    'numpy>=1.25.0': 'May cause issues with TensorFlow 2.13'
                }
            }
        }
    
    def check_python_compatibility(self):
        """Check Python version compatibility"""
        print("🐍 Checking Python compatibility...")
        
        python_version = self.system_info['python_version_info']
        
        if python_version.major < 3:
            self.issues.append("Python 3.x required (you have Python 2.x)")
            return False
        
        if python_version.minor < 8:
            self.issues.append(f"Python 3.8+ required (you have {python_version.major}.{python_version.minor})")
            return False
        
        if python_version.minor > 11:
            self.warnings.append(f"Python {python_version.major}.{python_version.minor} is very new - some packages may not be fully compatible")
        
        print(f"  ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - Compatible")
        return True
    
    def check_tensorflow_setup(self):
        """Check TensorFlow installation and compatibility"""
        print("\n🧠 Checking TensorFlow setup...")
        
        has_tf = 'tensorflow' in self.installed_packages
        has_tf_macos = 'tensorflow-macos' in self.installed_packages
        has_tf_metal = 'tensorflow-metal' in self.installed_packages
        has_keras = 'keras' in self.installed_packages
        
        # Check for conflicts
        if has_tf and has_tf_macos:
            self.issues.append("Conflict: Both tensorflow and tensorflow-macos are installed")
            print("  ❌ Conflict: Both tensorflow and tensorflow-macos installed")
            return False
        
        if not has_tf and not has_tf_macos:
            self.issues.append("Missing: No TensorFlow installation found")
            print("  ❌ No TensorFlow installation found")
            return False
        
        # Check versions
        tf_version = None
        if has_tf:
            tf_version = self.installed_packages['tensorflow']
            print(f"  📦 TensorFlow: {tf_version}")
        elif has_tf_macos:
            tf_version = self.installed_packages['tensorflow-macos']
            print(f"  📦 TensorFlow-macOS: {tf_version}")
            
            if self.system_info['is_apple_silicon']:
                print("  🍎 Apple Silicon detected - tensorflow-macos is optimal")
                if has_tf_metal:
                    print(f"  🚀 TensorFlow Metal: {self.installed_packages['tensorflow-metal']} - GPU acceleration enabled")
                else:
                    self.warnings.append("tensorflow-metal not installed - missing GPU acceleration")
            else:
                self.warnings.append("tensorflow-macos on non-Apple Silicon - consider regular tensorflow")
        
        # Check Keras compatibility
        if has_keras:
            keras_version = self.installed_packages['keras']
            print(f"  📦 Keras: {keras_version}")
            
            # Check TensorFlow-Keras compatibility
            if tf_version and keras_version:
                if not self.check_version_compatibility(tf_version, keras_version, 'tensorflow', 'keras'):
                    self.issues.append(f"TensorFlow {tf_version} and Keras {keras_version} may be incompatible")
        else:
            self.issues.append("Missing: Keras not installed")
            print("  ❌ Keras not installed")
        
        return len([i for i in self.issues if 'tensorflow' in i.lower()]) == 0
    
    def check_deepface_compatibility(self):
        """Check DeepFace compatibility with other packages"""
        print("\n🤖 Checking DeepFace compatibility...")
        
        if 'deepface' not in self.installed_packages:
            self.issues.append("Missing: DeepFace not installed")
            print("  ❌ DeepFace not installed")
            return False
        
        deepface_version = self.installed_packages['deepface']
        print(f"  📦 DeepFace: {deepface_version}")
        
        # Check TensorFlow compatibility
        tf_version = self.installed_packages.get('tensorflow') or self.installed_packages.get('tensorflow-macos')
        if tf_version:
            if version.parse(tf_version) >= version.parse('2.14.0'):
                self.warnings.append(f"DeepFace may have issues with TensorFlow {tf_version} (>=2.14.0)")
        
        # Check required dependencies
        required_deps = ['opencv-python', 'numpy', 'pillow', 'pandas', 'gdown', 'tqdm']
        missing_deps = []
        
        for dep in required_deps:
            if dep not in self.installed_packages:
                missing_deps.append(dep)
        
        if missing_deps:
            self.issues.append(f"DeepFace missing dependencies: {', '.join(missing_deps)}")
            print(f"  ❌ Missing dependencies: {', '.join(missing_deps)}")
        
        return len(missing_deps) == 0
    
    def check_version_compatibility(self, version1, version2, package1, package2):
        """Check if two package versions are compatible"""
        try:
            v1 = version.parse(version1)
            v2 = version.parse(version2)
            
            # Define known compatibility rules
            compatibility_rules = {
                ('tensorflow', 'keras'): {
                    '2.13.0': ['2.13.1'],
                    '2.12.0': ['2.12.0'],
                    '2.11.0': ['2.11.0']
                }
            }
            
            rule_key = (package1, package2)
            if rule_key in compatibility_rules:
                if version1 in compatibility_rules[rule_key]:
                    return version2 in compatibility_rules[rule_key][version1]
            
            return True  # Assume compatible if no specific rule
        except:
            return True
    
    def check_opencv_compatibility(self):
        """Check OpenCV compatibility"""
        print("\n📹 Checking OpenCV compatibility...")
        
        opencv_packages = ['opencv-python', 'opencv-contrib-python', 'opencv-python-headless']
        installed_opencv = [pkg for pkg in opencv_packages if pkg in self.installed_packages]
        
        if not installed_opencv:
            self.issues.append("Missing: No OpenCV installation found")
            print("  ❌ No OpenCV installation found")
            return False
        
        if len(installed_opencv) > 1:
            self.warnings.append(f"Multiple OpenCV packages installed: {', '.join(installed_opencv)}")
            print(f"  ⚠️  Multiple OpenCV packages: {', '.join(installed_opencv)}")
        
        for pkg in installed_opencv:
            print(f"  📦 {pkg}: {self.installed_packages[pkg]}")
        
        return True
    
    def check_system_specific_issues(self):
        """Check for system-specific compatibility issues"""
        print(f"\n🖥️  Checking system-specific compatibility ({self.system_info['platform']})...")
        
        if self.system_info['is_mac']:
            print("  🍎 macOS detected")
            
            if self.system_info['is_apple_silicon']:
                print("  🔥 Apple Silicon (M1/M2) detected")
                
                # Check for optimal TensorFlow setup
                if 'tensorflow' in self.installed_packages and 'tensorflow-macos' not in self.installed_packages:
                    self.warnings.append("Consider tensorflow-macos for better Apple Silicon performance")
                
                # Check for Metal acceleration
                if 'tensorflow-macos' in self.installed_packages and 'tensorflow-metal' not in self.installed_packages:
                    self.warnings.append("Install tensorflow-metal for GPU acceleration")
            
            # Check for camera permissions
            print("  📹 Note: Camera permissions may be required for webcam access")
        
        elif self.system_info['is_windows']:
            print("  🪟 Windows detected")
            # Windows-specific checks can be added here
        
        elif self.system_info['is_linux']:
            print("  🐧 Linux detected")
            # Linux-specific checks can be added here
    
    def test_actual_imports(self):
        """Test actual package imports to verify they work together"""
        print("\n🧪 Testing actual imports...")
        
        import_tests = [
            ('numpy', 'import numpy as np'),
            ('opencv', 'import cv2'),
            ('flask', 'from flask import Flask'),
            ('tensorflow', 'import tensorflow as tf'),
            ('keras', 'from tensorflow import keras'),
            ('pillow', 'from PIL import Image'),
        ]
        
        failed_imports = []
        
        for name, import_code in import_tests:
            try:
                exec(import_code)
                print(f"  ✅ {name}")
            except Exception as e:
                print(f"  ❌ {name}: {e}")
                failed_imports.append((name, str(e)))
        
        # Test DeepFace separately (it's slow and may download models)
        print("\n  🤖 Testing DeepFace (may take a moment)...")
        try:
            from deepface import DeepFace
            print("  ✅ DeepFace import successful")
            
            # Test basic functionality
            import numpy as np
            test_img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            result = DeepFace.analyze(test_img, actions=['emotion'], 
                                    enforce_detection=False, silent=True)
            print("  ✅ DeepFace analysis test passed")
            
        except Exception as e:
            print(f"  ❌ DeepFace: {e}")
            failed_imports.append(('deepface', str(e)))
        
        if failed_imports:
            self.issues.extend([f"Import failed - {name}: {error}" for name, error in failed_imports])
        
        return len(failed_imports) == 0
    
    def generate_recommendations(self):
        """Generate recommendations based on findings"""
        recommendations = []
        
        if self.system_info['is_apple_silicon']:
            if 'tensorflow' in self.installed_packages:
                recommendations.append("Consider switching to tensorflow-macos for better Apple Silicon performance")
            
            if 'tensorflow-macos' in self.installed_packages and 'tensorflow-metal' not in self.installed_packages:
                recommendations.append("Install tensorflow-metal for GPU acceleration: pip install tensorflow-metal")
        
        # Check for version conflicts
        if any('conflict' in issue.lower() for issue in self.issues):
            recommendations.append("Resolve package conflicts by uninstalling conflicting packages first")
        
        # Check for missing dependencies
        missing_packages = [issue for issue in self.issues if 'missing' in issue.lower()]
        if missing_packages:
            recommendations.append("Install missing packages using the provided installation script")
        
        # DeepFace specific recommendations
        if 'deepface' in self.installed_packages:
            deepface_version = self.installed_packages['deepface']
            if version.parse(deepface_version) > version.parse('0.0.79'):
                recommendations.append("Consider downgrading DeepFace to 0.0.75 or 0.0.79 for better stability")
        
        return recommendations
    
    def create_fixed_requirements(self):
        """Create a requirements.txt with compatible versions"""
        if self.system_info['is_apple_silicon']:
            requirements = """# Facial Recognition System - Apple Silicon Optimized
numpy==1.24.3
Pillow==10.0.1
opencv-python==4.8.1.78
Flask==2.3.3

# TensorFlow for Apple Silicon
tensorflow-macos==2.13.0
tensorflow-metal==1.0.1
keras==2.13.1

# Face Recognition
deepface==0.0.75

# Supporting packages
protobuf==3.20.3
pandas>=1.3.0
gdown>=4.6.0
tqdm>=4.64.0
werkzeug>=2.3.0
jinja2>=3.1.0
"""
        else:
            requirements = """# Facial Recognition System - Standard
numpy==1.24.3
Pillow==10.0.1
opencv-python==4.8.1.78
Flask==2.3.3

# TensorFlow
tensorflow==2.13.0
keras==2.13.1

# Face Recognition
deepface==0.0.75

# Supporting packages
protobuf==3.20.3
pandas>=1.3.0
gdown>=4.6.0
tqdm>=4.64.0
werkzeug>=2.3.0
jinja2>=3.1.0
"""
        
        with open('requirements_compatible.txt', 'w') as f:
            f.write(requirements)
        
        return 'requirements_compatible.txt'
    
    def create_installation_script(self):
        """Create a system-specific installation script"""
        script_content = f"""#!/usr/bin/env python3
'''
Auto-generated installation script for {self.system_info['platform']}
Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
import subprocess
import sys

def run_cmd(cmd):
    print(f"🔄 {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {{e}}")
        return False

def main():
    print("🚀 Installing compatible packages...")
    
    # Upgrade pip
    run_cmd(f"{{sys.executable}} -m pip install --upgrade pip")
    
    # Clean installation
    cleanup_packages = [
        "tensorflow", "tensorflow-macos", "tensorflow-metal", 
        "deepface", "opencv-python", "keras", "numpy"
    ]
    
    for pkg in cleanup_packages:
        run_cmd(f"{{sys.executable}} -m pip uninstall {{pkg}} -y")
    
    # Install compatible versions
    if not run_cmd(f"{{sys.executable}} -m pip install -r requirements_compatible.txt"):
        print("❌ Installation failed!")
        return False
    
    print("🎉 Installation complete!")
    print("🧪 Run: python test_compatibility.py")
    return True

if __name__ == "__main__":
    main()
"""
        
        with open('install_compatible.py', 'w') as f:
            f.write(script_content)
        
        return 'install_compatible.py'
    
    def run_full_check(self):
        """Run complete compatibility check"""
        print("🔍 COMPREHENSIVE COMPATIBILITY CHECK")
        print("=" * 60)
        
        # System info
        print(f"\n🖥️  System: {self.system_info['platform']} {self.system_info['architecture']}")
        print(f"🐍 Python: {self.system_info['python_version_info'].major}.{self.system_info['python_version_info'].minor}.{self.system_info['python_version_info'].micro}")
        
        # Run all checks
        checks_passed = 0
        total_checks = 6
        
        if self.check_python_compatibility():
            checks_passed += 1
        
        if self.check_tensorflow_setup():
            checks_passed += 1
        
        if self.check_deepface_compatibility():
            checks_passed += 1
        
        if self.check_opencv_compatibility():
            checks_passed += 1
        
        self.check_system_specific_issues()
        checks_passed += 1
        
        if self.test_actual_imports():
            checks_passed += 1
        
        # Generate report
        print("\n" + "=" * 60)
        print("📋 COMPATIBILITY REPORT")
        print("=" * 60)
        
        print(f"\n✅ Checks passed: {checks_passed}/{total_checks}")
        
        if self.issues:
            print(f"\n❌ Issues found ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        # Generate recommendations
        recommendations = self.generate_recommendations()
        if recommendations:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec}")
        
        # Create fix files
        if self.issues or self.warnings:
            print(f"\n🔧 Creating fix files...")
            req_file = self.create_fixed_requirements()
            install_file = self.create_installation_script()
            
            print(f"  📄 {req_file} - Compatible requirements")
            print(f"  📄 {install_file} - Installation script")
            
            print(f"\n🚀 To fix issues, run:")
            print(f"  python {install_file}")
        
        # Final status
        if checks_passed == total_checks and not self.issues:
            print(f"\n🎉 ALL COMPATIBILITY CHECKS PASSED!")
            print(f"✅ Your system is ready to run the facial recognition app!")
        else:
            print(f"\n⚠️  {len(self.issues)} issues need to be resolved before running the app")
        
        return checks_passed == total_checks and not self.issues

def main():
    checker = CompatibilityChecker()
    return checker.run_full_check()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)