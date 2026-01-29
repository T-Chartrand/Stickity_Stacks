"""
Stickity Stacks - Version Management Script
Automated version bumping across all project files
"""

import re
import sys
from pathlib import Path
from datetime import datetime

class VersionManager:
    def __init__(self, project_root="."):
        self.root = Path(project_root).resolve()
        self.files_to_update = {
            'installer.iss': self.update_inno_setup,
            'README.md': self.update_markdown,
            'deployment/DEPLOYMENT_GUIDE.md': self.update_markdown,
        }
        
    def get_current_version(self):
        """Read current version from installer.iss"""
        iss_file = self.root / 'installer.iss'
        if not iss_file.exists():
            return None
            
        content = iss_file.read_text(encoding='utf-8')
        match = re.search(r'#define MyAppVersion "(\d+\.\d+\.\d+)"', content)
        return match.group(1) if match else None
    
    def parse_version(self, version_str):
        """Parse version string into components"""
        parts = version_str.split('.')
        return {
            'major': int(parts[0]),
            'minor': int(parts[1]),
            'patch': int(parts[2])
        }
    
    def format_version(self, parts):
        """Format version components into string"""
        return f"{parts['major']}.{parts['minor']}.{parts['patch']}"
    
    def bump_version(self, current, bump_type='patch'):
        """Increment version number"""
        parts = self.parse_version(current)
        
        if bump_type == 'major':
            parts['major'] += 1
            parts['minor'] = 0
            parts['patch'] = 0
        elif bump_type == 'minor':
            parts['minor'] += 1
            parts['patch'] = 0
        elif bump_type == 'patch':
            parts['patch'] += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return self.format_version(parts)
    
    def update_inno_setup(self, filepath, old_version, new_version):
        """Update version in Inno Setup script"""
        content = filepath.read_text(encoding='utf-8')
        updated = content.replace(
            f'#define MyAppVersion "{old_version}"',
            f'#define MyAppVersion "{new_version}"'
        )
        filepath.write_text(updated, encoding='utf-8')
        return True
    
    def update_markdown(self, filepath, old_version, new_version):
        """Update version references in markdown files"""
        content = filepath.read_text(encoding='utf-8')
        
        # Replace version in download links
        patterns = [
            (rf'v{re.escape(old_version)}', f'v{new_version}'),
            (rf'_{re.escape(old_version)}', f'_{new_version}'),
            (rf'Version: {re.escape(old_version)}', f'Version: {new_version}'),
        ]
        
        updated = content
        for old_pattern, new_pattern in patterns:
            updated = re.sub(old_pattern, new_pattern, updated)
        
        filepath.write_text(updated, encoding='utf-8')
        return True
    
    def update_all_files(self, old_version, new_version):
        """Update version in all project files"""
        updated_files = []
        
        for file_path, update_func in self.files_to_update.items():
            full_path = self.root / file_path
            if full_path.exists():
                try:
                    if update_func(full_path, old_version, new_version):
                        updated_files.append(file_path)
                        print(f"✓ Updated: {file_path}")
                except Exception as e:
                    print(f"✗ Failed to update {file_path}: {e}")
            else:
                print(f"⚠ File not found: {file_path}")
        
        return updated_files
    
    def create_changelog_entry(self, version):
        """Create a changelog entry template"""
        changelog = self.root / 'CHANGELOG.md'
        date = datetime.now().strftime('%Y-%m-%d')
        
        entry = f"""
## [{version}] - {date}

### Added
- 

### Changed
- 

### Fixed
- 

### Removed
- 

"""
        if changelog.exists():
            content = changelog.read_text(encoding='utf-8')
            # Insert after header
            lines = content.split('\n')
            header_end = next((i for i, line in enumerate(lines) if line.startswith('##')), 0)
            lines.insert(header_end, entry)
            changelog.write_text('\n'.join(lines), encoding='utf-8')
        else:
            # Create new changelog
            header = f"# Changelog\n\nAll notable changes to Stickity Stacks will be documented in this file.\n"
            changelog.write_text(header + entry, encoding='utf-8')
        
        print(f"✓ Created changelog entry for v{version}")
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python version_bump.py [major|minor|patch]")
        print("   or: python version_bump.py <version>")
        print("\nExamples:")
        print("  python version_bump.py patch    # 1.0.0 -> 1.0.1")
        print("  python version_bump.py minor    # 1.0.0 -> 1.1.0")
        print("  python version_bump.py major    # 1.0.0 -> 2.0.0")
        print("  python version_bump.py 1.2.3    # Set to 1.2.3")
        sys.exit(1)
    
    # Initialize version manager
    vm = VersionManager()
    
    # Get current version
    current = vm.get_current_version()
    if not current:
        print("Error: Could not determine current version from installer.iss")
        sys.exit(1)
    
    print(f"Current version: {current}")
    
    # Determine new version
    arg = sys.argv[1].lower()
    if arg in ['major', 'minor', 'patch']:
        new_version = vm.bump_version(current, arg)
    elif re.match(r'\d+\.\d+\.\d+', arg):
        new_version = arg
    else:
        print(f"Error: Invalid version argument: {arg}")
        sys.exit(1)
    
    print(f"New version: {new_version}")
    
    # Confirm
    response = input(f"\nUpdate version from {current} to {new_version}? (y/N): ")
    if response.lower() != 'y':
        print("Cancelled")
        sys.exit(0)
    
    # Update files
    print("\nUpdating files...")
    updated = vm.update_all_files(current, new_version)
    
    # Create changelog entry
    vm.create_changelog_entry(new_version)
    
    print(f"\n✓ Version updated to {new_version}")
    print(f"✓ Updated {len(updated)} files")
    print("\nNext steps:")
    print("  1. Review changes: git diff")
    print("  2. Update CHANGELOG.md with changes")
    print("  3. Commit: git add -A && git commit -m 'Bump version to {}'".format(new_version))
    print("  4. Tag: git tag v{}".format(new_version))
    print("  5. Push: git push origin v{}".format(new_version))

if __name__ == '__main__':
    main()
