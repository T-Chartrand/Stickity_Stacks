# Maintainer: T-Chartrand <tyrrellc at gmail dot com>
pkgname=stickity-stacks-git
pkgver=r41.a1130a7
pkgrel=1
pkgdesc="Frameless GTK4 sticky note application with stacking support"
arch=('any')
url="https://github.com/T-Chartrand/Stickity_Stacks"
license=('GPL-3.0-only')
depends=('python' 'python-gobject' 'gtk4')
makedepends=('git')
provides=('stickity-stacks')
conflicts=('stickity-stacks')
source=("git+https://github.com/T-Chartrand/Stickity_Stacks.git")
sha256sums=('SKIP')

pkgver() {
    cd Stickity_Stacks
    printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package() {
    cd Stickity_Stacks

    # Main script
    install -Dm644 stickity_stacks.py \
        "$pkgdir/usr/lib/stickity-stacks/stickity_stacks.py"

    # Launcher wrapper
    install -dm755 "$pkgdir/usr/bin"
    cat > "$pkgdir/usr/bin/stickity-stacks" <<'WRAPPER'
#!/bin/sh
exec python3 /usr/lib/stickity-stacks/stickity_stacks.py "$@"
WRAPPER
    chmod 755 "$pkgdir/usr/bin/stickity-stacks"

    # Desktop entry
    install -Dm644 com.stickity.stacks.desktop \
        "$pkgdir/usr/share/applications/com.stickity.stacks.desktop"

    # Icon (hicolor + pixmaps fallback)
    install -Dm644 stickity_stacks.png \
        "$pkgdir/usr/share/icons/hicolor/256x256/apps/stickity_stacks.png"
    install -Dm644 stickity_stacks.png \
        "$pkgdir/usr/share/pixmaps/stickity_stacks.png"

    # License
    install -Dm644 LICENSE \
        "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}
