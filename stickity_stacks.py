#!/usr/bin/env python3
# Stickity Stacks – Frameless GTK4 sticky notes with stacking, persistence, styling, and deletion

import gi, json, os
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
from gi.repository import Gtk, Gdk, Pango

class StickyNote(Gtk.Window):
    def __init__(self):
        super().__init__(title="Stickity Stacks", decorated=False)
        self.set_default_size(260, 200)
        self.set_resizable(True)

        # Add CSS class to main window for more specific targeting
        self.add_css_class("sticky-note-window")

        # Persistence file
        self.data_file = os.path.expanduser("~/.local/share/stickity_stacks_notes.json")
        # Default style values with better font fallbacks
        self.current_font    = "Sans 15"
        self.current_fg      = "#1a1a1a"
        self.current_bg      = "#fffad1"
        self.current_opacity = 1.0
        # Load saved preferences before UI creation
        self.load_prefs()

        # Note stack management
        self.note_stack = []
        self.current_note_index = 0
        self.note_counter = 1

        # CSS provider at APPLICATION priority to override theme
        self.css = Gtk.CssProvider()
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            self.css,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Layout: Overlay with Stack
        overlay = Gtk.Overlay()
        self.set_child(overlay)

        self.stack = Gtk.Stack(
            transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
            transition_duration=300
        )
        overlay.set_child(self.stack)

        # Close button
        close_btn = Gtk.Button()
        close_btn.set_icon_name("window-close-symbolic")
        close_btn.set_can_focus(False)
        close_btn.set_valign(Gtk.Align.START)
        close_btn.set_halign(Gtk.Align.START)
        close_btn.set_margin_top(4)
        close_btn.set_margin_start(4)
        close_btn.set_css_classes(["close-button"])
        close_btn.connect("clicked", lambda _: self.close())
        overlay.add_overlay(close_btn)

        # Gear (settings) button
        gear = Gtk.Button()
        gear.set_icon_name("emblem-system-symbolic")
        gear.set_can_focus(False)
        gear.set_valign(Gtk.Align.START)
        gear.set_halign(Gtk.Align.END)
        gear.set_margin_top(4)
        gear.set_margin_end(4)
        gear.set_css_classes(["gear-button"])
        gear.connect("clicked", self.open_settings)
        overlay.add_overlay(gear)

        # Trash (delete) button
        trash = Gtk.Button()
        trash.set_icon_name("user-trash-symbolic")
        trash.set_can_focus(False)
        trash.set_valign(Gtk.Align.START)
        trash.set_halign(Gtk.Align.END)
        trash.set_margin_top(4)
        trash.set_margin_end(36)
        trash.set_css_classes(["trash-button"])
        trash.connect("clicked", self.delete_current_note)
        overlay.add_overlay(trash)

        # Dog-ear indicator
        self.dog_ear = Gtk.Button()
        self.dog_ear.set_can_focus(False)
        self.dog_ear.set_valign(Gtk.Align.END)
        self.dog_ear.set_halign(Gtk.Align.END)
        self.dog_ear.set_margin_bottom(4)
        self.dog_ear.set_margin_end(4)
        self.dog_ear.set_css_classes(["dog-ear-button"])
        self.dog_ear.connect("clicked", self.cycle_notes)
        self.dog_ear.set_visible(False)
        overlay.add_overlay(self.dog_ear)

        # Load persisted notes or create the first note
        if not self.load_notes():
            self.create_new_note("Note 1", "")

        # Keyboard shortcuts: Ctrl+S (stack), Ctrl+D (delete)
        sc = Gtk.ShortcutController()
        sc.add_shortcut(Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>s"),
            Gtk.CallbackAction.new(self.stack_note)
        ))
        sc.add_shortcut(Gtk.Shortcut.new(
            Gtk.ShortcutTrigger.parse_string("<Control>d"),
            Gtk.CallbackAction.new(self.delete_current_note)
        ))
        self.add_controller(sc)

        # Drag-to-move or resize depending on pointer position
        drag = Gtk.GestureClick()
        drag.set_button(1)
        drag.connect("pressed", self.on_drag_begin)
        self.stack.add_controller(drag)

        # Cursor changes near edges to signal resize zones
        motion = Gtk.EventControllerMotion()
        motion.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        motion.connect("motion", self.on_motion)
        overlay.add_controller(motion)

        # Apply initial CSS styling
        self.apply_css()

    def get_font_fallbacks(self, primary_font):
        """Get a list of font fallbacks for better cross-distro compatibility"""
        fallbacks = [
            primary_font,
            "DejaVu Sans",
            "Liberation Sans",
            "Ubuntu",
            "Noto Sans",
            "sans-serif"
        ]
        return fallbacks

    def create_new_note(self, title, content=""):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        # Bold single-line title — margins clear the close button (left) and trash+gear (right)
        title_entry = Gtk.Entry()
        title_entry.set_text(title)
        title_entry.set_css_classes(["sticky-title-entry"])
        title_entry.set_margin_top(4)
        title_entry.set_margin_start(32)
        title_entry.set_margin_end(64)
        box.append(title_entry)

        # Scrollable body — word-wrap, normal weight
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        tv = Gtk.TextView(wrap_mode=Gtk.WrapMode.WORD_CHAR)
        tv.set_css_classes(["sticky-note-textview"])
        if content:
            buf = tv.get_buffer()
            buf.set_text(content)
        scroll.set_child(tv)
        box.append(scroll)

        name = f"note_{len(self.note_stack)}"
        self.stack.add_named(box, name)
        self.note_stack.append({'entry': title_entry, 'textview': tv, 'title': title, 'name': name})
        self.stack.set_visible_child_name(name)
        self.current_note_index = len(self.note_stack) - 1
        self.update_dog_ear_visibility()
        self.save_notes()
        return tv

    def stack_note(self, *_):
        self.note_counter += 1
        self.create_new_note(f"Note {self.note_counter}", "")
        self.update_dog_ear_visibility()
        return True

    def delete_current_note(self, *_):
        if not self.note_stack:
            return True
        note = self.note_stack.pop(self.current_note_index)
        child = self.stack.get_child_by_name(note['name'])
        if child:
            self.stack.remove(child)
        if self.current_note_index >= len(self.note_stack):
            self.current_note_index = len(self.note_stack) - 1
        if not self.note_stack:
            self.note_counter = 1
            self.create_new_note("Note 1", "")
        else:
            name = self.note_stack[self.current_note_index]['name']
            self.stack.set_visible_child_name(name)
        self.update_dog_ear_visibility()
        self.save_notes()
        return True

    def cycle_notes(self, *_):
        if len(self.note_stack) < 2:
            return
        self.current_note_index = (self.current_note_index + 1) % len(self.note_stack)
        name = self.note_stack[self.current_note_index]['name']
        self.stack.set_visible_child_name(name)
        self.update_dog_ear_visibility()

    def update_dog_ear_visibility(self):
        total = len(self.note_stack)
        current = self.current_note_index + 1
        visible = total > 1
        self.dog_ear.set_visible(visible)
        if visible:
            self.dog_ear.set_label(f"{current}/{total}")

    def apply_css(self):
        try:
            desc = Pango.FontDescription(self.current_font)
            family = desc.get_family()
            size = desc.get_size() // Pango.SCALE or 15

            if not family:
                family = "Sans"

        except Exception as e:
            print(f"Font parsing error: {e}")
            family = "Sans"
            size = 15

        # Create font fallback list
        font_fallbacks = self.get_font_fallbacks(family)
        font_list = ", ".join([f'"{font}"' for font in font_fallbacks])

        css = f"""
        /* Main window styling */
        .sticky-note-window {{
            background-color: {self.current_bg};
        }}

        /* Title entry — bold, single line, blends with note background */
        .sticky-title-entry {{
            background-color: {self.current_bg};
            color: {self.current_fg};
            font-family: {font_list};
            font-size: {size}px;
            font-weight: bold;
            border: none;
            border-bottom: 1px solid rgba(0,0,0,0.12);
            border-radius: 0;
            padding: 2px 6px;
            box-shadow: none;
        }}

        .sticky-title-entry text {{
            background-color: {self.current_bg};
            color: {self.current_fg};
            font-weight: bold;
        }}

        /* Body TextView — normal weight, word-wrap */
        .sticky-note-textview {{
            background-color: {self.current_bg};
            color: {self.current_fg};
            font-family: {font_list};
            font-size: {size}px;
            font-weight: normal;
            padding: 8px;
            border: none;
        }}

        .sticky-note-textview text {{
            background-color: {self.current_bg};
            color: {self.current_fg};
            font-family: {font_list};
            font-size: {size}px;
            font-weight: normal;
        }}

        /* Button styling */
        .close-button, .gear-button, .trash-button {{
            background-color: transparent;
            border: none;
            padding: 2px;
            color: {self.current_fg};
            min-width: 24px;
            min-height: 24px;
        }}

        .close-button:hover, .gear-button:hover, .trash-button:hover {{
            background-color: rgba(0,0,0,0.1);
            border-radius: 4px;
        }}

        /* Dog-ear button */
        .dog-ear-button {{
            background-color: rgba(0,0,0,0.1);
            border: none;
            padding: 4px 8px;
            border-radius: 8px 0 0 0;
            font-size: 12px;
            font-weight: bold;
            color: rgba(0,0,0,0.6);
            min-width: 32px;
            min-height: 24px;
        }}

        .dog-ear-button:hover {{
            background-color: rgba(0,0,0,0.15);
        }}
         
         scale {{
            min-height: 24px;
        }}

        scale slider {{
            min-width: 16px;
            min-height: 16px;
        }}
        """

        try:
            self.css.load_from_data(css.encode())
        except Exception as e:
            print(f"CSS application error: {e}")

    _RESIZE_MARGIN = 8

    def _edge_at(self, x, y):
        w, h, m = self.get_width(), self.get_height(), self._RESIZE_MARGIN
        left, right = x < m, x > w - m
        top, bottom = y < m, y > h - m
        if top    and left:  return Gdk.SurfaceEdge.NORTH_WEST
        if top    and right: return Gdk.SurfaceEdge.NORTH_EAST
        if bottom and left:  return Gdk.SurfaceEdge.SOUTH_WEST
        if bottom and right: return Gdk.SurfaceEdge.SOUTH_EAST
        if top:    return Gdk.SurfaceEdge.NORTH
        if bottom: return Gdk.SurfaceEdge.SOUTH
        if left:   return Gdk.SurfaceEdge.WEST
        if right:  return Gdk.SurfaceEdge.EAST
        return None

    _EDGE_CURSORS = {
        Gdk.SurfaceEdge.NORTH_WEST: "nw-resize",
        Gdk.SurfaceEdge.NORTH_EAST: "ne-resize",
        Gdk.SurfaceEdge.SOUTH_WEST: "sw-resize",
        Gdk.SurfaceEdge.SOUTH_EAST: "se-resize",
        Gdk.SurfaceEdge.NORTH:      "n-resize",
        Gdk.SurfaceEdge.SOUTH:      "s-resize",
        Gdk.SurfaceEdge.WEST:       "w-resize",
        Gdk.SurfaceEdge.EAST:       "e-resize",
    }

    def on_motion(self, ctrl, x, y):
        edge = self._edge_at(x, y)
        name = self._EDGE_CURSORS.get(edge, "default")
        self.set_cursor(Gdk.Cursor.new_from_name(name, None))

    def on_drag_begin(self, gesture, _, x, y):
        edge = self._edge_at(x, y)
        surf = self.get_surface()
        dev  = gesture.get_device()
        seq  = gesture.get_current_sequence()
        ev   = gesture.get_last_event(seq)
        if not (surf and ev):
            return
        if edge is not None and hasattr(surf, 'begin_resize'):
            surf.begin_resize(edge, dev, 1, x, y, ev.get_time())
        elif hasattr(surf, 'begin_move'):
            surf.begin_move(dev, 1, x, y, ev.get_time())

    def open_settings(self, _):
        win = Gtk.Window(title="Settings", transient_for=self, modal=True)
        win.set_default_size(380, 300)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12,
                      margin_top=12, margin_bottom=12,
                      margin_start=12, margin_end=12)

        # Font picker
        box.append(Gtk.Label(label="Font:", halign=Gtk.Align.START))
        fd = Gtk.FontDialog()
        fb = Gtk.FontDialogButton(dialog=fd)
        fb.set_hexpand(True)
        fb.set_size_request(240, 36)
 
        try:
            current_desc = Pango.FontDescription(self.current_font)
            fb.set_font_desc(current_desc)
        except:
            # Fallback to default font
            fb.set_font_desc(Pango.FontDescription("Sans 15"))

        fb.connect("notify::font-desc", self.on_font_changed)
        box.append(fb)
        box.set_spacing(12)        

        # Text color picker
        box.append(Gtk.Label(label="Text Color:", halign=Gtk.Align.START))
        td = Gtk.ColorDialog(title="Choose Text Color")
        tb = Gtk.ColorDialogButton(dialog=td)
        rgba = Gdk.RGBA()
        rgba.parse(self.current_fg)
        tb.set_rgba(rgba)
        tb.connect("notify::rgba", self.on_text_color_changed)
        box.append(tb)

        # Background color picker
        box.append(Gtk.Label(label="Background Color:", halign=Gtk.Align.START))
        bd = Gtk.ColorDialog(title="Choose Background Color")
        bb = Gtk.ColorDialogButton(dialog=bd)
        rgba2 = Gdk.RGBA()
        rgba2.parse(self.current_bg)
        bb.set_rgba(rgba2)
        bb.connect("notify::rgba", self.on_bg_color_changed)
        box.append(bb)

        # Opacity slider
        opacity_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL,
            0.1,
            1.0,
            0.05
        )

        opacity_scale.set_value(self.current_opacity)
        opacity_scale.set_draw_value(True)
        opacity_scale.set_digits(2)
        opacity_scale.set_hexpand(True)
        
        opacity_scale.connect(
            "value-changed",
            self.on_opacity_changed
        )

        box.append(opacity_scale)

        # Close button with proper styling reapplication
        close = Gtk.Button(label="Close")
        def on_close_clicked(*_):
            self.save_notes()
            self.save_prefs()
            self.apply_styling_to_all_notes()
            win.close()

        close.connect("clicked", on_close_clicked)
        box.append(close)

        win.set_child(box)
        win.present()

    def apply_styling_to_all_notes(self):
        self.apply_css()

    def on_opacity_changed(self, scale):
        self.current_opacity = scale.get_value()
        self.set_opacity(self.current_opacity)

    def on_font_changed(self, btn, _):
        desc = btn.get_font_desc()
        if desc:
            self.current_font = desc.to_string()
            self.apply_styling_to_all_notes()

    def on_text_color_changed(self, btn, _):
        rgba = btn.get_rgba()
        if rgba:
            self.current_fg = rgba.to_string()
            self.apply_styling_to_all_notes()

    def on_bg_color_changed(self, btn, _):
        rgba = btn.get_rgba()
        if rgba:
            self.current_bg = rgba.to_string()
            self.apply_styling_to_all_notes()

    def save_notes(self):
        notes = []
        for n in self.note_stack:
            buf = n['textview'].get_buffer()
            txt = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)
            title = n['entry'].get_text() if 'entry' in n else n.get('title', '')
            notes.append({'title': title, 'content': txt})
        try:
            full = json.load(open(self.data_file, 'r', encoding='utf-8')) if os.path.exists(self.data_file) else {}
        except:
            full = {}
        full['notes'] = notes
        # preserve prefs if present
        prefs = full.get('_prefs', {})
        full['_prefs'] = prefs
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(full, f, ensure_ascii=False, indent=2)

    def load_notes(self):
        if not os.path.isfile(self.data_file):
            return False
        try:
            data = json.load(open(self.data_file, 'r', encoding='utf-8'))
            for idx, entry in enumerate(data.get('notes', []), 1):
                self.note_counter = idx
                self.create_new_note(entry.get('title', f"Note {idx}"),
                                     entry.get('content', ""))
            return len(self.note_stack) > 0
        except Exception as e:
            print(f"Error loading notes: {e}")
            return False

    def save_prefs(self):
        try:
            # Try to load existing data
            if os.path.isfile(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    full = json.load(f)
            else:
                full = {}

            # Update preferences
            full['_prefs'] = {
                'font':    self.current_font,
                'fg':      self.current_fg,
                'bg':      self.current_bg,
                'opacity': self.current_opacity,
            }

            # Write back to file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(full, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Error saving preferences: {e}")

    def load_prefs(self):
        if not os.path.isfile(self.data_file):
            return
        try:
            full = json.load(open(self.data_file, 'r', encoding='utf-8'))
            prefs = full.get('_prefs', {})
            self.current_font    = prefs.get('font',    self.current_font)
            self.current_fg      = prefs.get('fg',      self.current_fg)
            self.current_bg      = prefs.get('bg',      self.current_bg)
            self.current_opacity = prefs.get('opacity', self.current_opacity)
            self.set_opacity(self.current_opacity)
        except Exception as e:
            print(f"Error loading preferences: {e}")

def main():
    app = Gtk.Application(application_id="com.stickity.stacks")
    app.connect("activate", lambda a: (w := StickyNote()).set_application(a) or w.present())
    app.run([])

if __name__ == "__main__":
    main()
