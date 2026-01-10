# Made for the 'Escape From Dayz' by Goon community
# Updated 1/8/2026
# made by .c.o.r.a
# for Python version - 3.11

#   Copyright © 2026 .c.o.r.a

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import datetime
import imgui
from imgui.integrations.glfw import GlfwRenderer
import glfw
import OpenGL.GL as gl
import time
import os
import numpy as np

# Config
DEBUG = False
DEFAULT_WIDTH = 240
DEFAULT_HEIGHT = 100
CLASSICMODEHEIGHT = 86
HOURS = sorted([5.96667, 8.96667, 11.96667, 14.96667, 17.96667, 20.96667, 23.96667, 2.96667])

# Globals

audioBool = False
classicMode = False 
show_settings = False
beepVol = 0.1
beepDur = 120
restartDur = 150
startDur = 240
forceStage = False
phaseID = 1


# Funcs

def beep(frequency, duration_ms, volume):
    fs = 44100
    t = np.linspace(0, duration_ms / 1000, int(fs * duration_ms / 1000), False)
    wave = (volume * np.sin(2 * np.pi * frequency * t)).astype(np.float32)
    sd.play(wave, fs)
def hms(seconds):
    td = datetime.timedelta(seconds=max(0, int(seconds)))
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"
def timingInfo():
    now = datetime.datetime.now(datetime.timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    now_decimal = now.hour + (now.minute / 60.0) + (now.second / 3600.0)
    target_hour = next((h for h in HOURS if h > now_decimal), None)
    if target_hour is None:
        next_target = today_start + datetime.timedelta(days=1, hours=HOURS[0])
    else:
        next_target = today_start + datetime.timedelta(hours=target_hour)
    past_hours = [h for h in HOURS if h <= now_decimal]
    if not past_hours:
        last_target = today_start - datetime.timedelta(days=1, hours=-HOURS[-1])
    else:
        last_target = today_start + datetime.timedelta(hours=past_hours[-1])
    return next_target, last_target
def countdown(target):
    try:
        target_decimal = target.hour + (target.minute / 60.0) + (target.second / 3600.0)
        current_idx = min(range(len(HOURS)), key=lambda i: abs(HOURS[i] - target_decimal))
        prev_hour = HOURS[current_idx - 1]
        today_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
        prev_time = today_start + datetime.timedelta(hours=prev_hour)
        if prev_time >= target:
            prev_time -= datetime.timedelta(days=1)
        return (target - prev_time).total_seconds()
    except (ValueError, IndexError): 
        return 10800

def main():
    global audioBool, show_settings, classicMode, forceStage, phaseID
    if not glfw.init():
        return
    glfw.window_hint(glfw.DECORATED, False)
    glfw.window_hint(glfw.RESIZABLE, False)
    glfw.window_hint(glfw.FLOATING, True)
    current_w, current_h = DEFAULT_WIDTH, DEFAULT_HEIGHT
    window = glfw.create_window(current_w, current_h, "Reset", None, None)
    monitor = glfw.get_primary_monitor()
    vid_mode = glfw.get_video_mode(monitor)
    glfw.set_window_pos(window, vid_mode.size.width - current_w, 0)
    glfw.make_context_current(window)
    imgui.create_context()
    
    # fonts

    io = imgui.get_io()
    io.fonts.add_font_default()
    classic_font_small = None
    font_path = "C:\\Windows\\Fonts\\seguiemj.ttf" 
    if os.path.exists(font_path):
        ranges = imgui.GlyphRanges([0x0020, 0x00FF, 0x25A0, 0x25FF, 0])
        classic_font_small = io.fonts.add_font_from_file_ttf(font_path, 9, glyph_ranges=ranges)
        
    impl = GlfwRenderer(window)
    impl.refresh_font_texture()

    # style

    style = imgui.get_style()
    style.colors[imgui.COLOR_TEXT] = (0.3, 0.3, 0.3, 1.0)
    style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.7, 0.1, 0.1, 1.0)
    style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.5, 0.0, 0.0, 1.0)
    dragging = False
    drag_offset_x, drag_offset_y = 0, 0
    curPhaseID = -1 
    RED = (1.0, 0.2, 0.2, 1.0)
    BLACK = (0.0, 0.0, 0.0, 1.0)
    CYAN = (0.2, 0.8, 1.0, 1.0)
    GREEN = (0.0, 1.0, 0.5, 1.0)
    BAR_BG = (0.15, 0.15, 0.15, 1.0) 

    # glfw init

    while not glfw.window_should_close(window):
        target_h = CLASSICMODEHEIGHT if classicMode else DEFAULT_HEIGHT
        if current_h != target_h:
            current_h = target_h
            glfw.set_window_size(window, DEFAULT_WIDTH, current_h)
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()
        io = imgui.get_io()
        current_dots_count = int(glfw.get_time() * 2) % 4
        dots_title = "." * current_dots_count + " " * (3 - current_dots_count) + ": "
        dots_footer = "." * current_dots_count + " " * (3 - current_dots_count)
        progress = 0.0
        current_stage, title_countdown = "", ""
        h_label, h_val, f_label, f_val = "", "", "", ""
        current_color = RED
        title_color = RED
        now = datetime.datetime.now(datetime.timezone.utc)
        target, last_target = timingInfo()
        seconds_since_last = (now - last_target).total_seconds()
        seconds_left_to_next = (target - now).total_seconds()
        # Phase logic
        Phase = 0
        if 0 <= seconds_since_last < restartDur:
            Phase = 1
        elif restartDur <= seconds_since_last < startDur:
            Phase = 2
        else:
            Phase = 3

        # Debug

        if forceStage:
            Phase = phaseID

        # Phases

        if Phase == 1:
            current_color = CYAN
            title_color = CYAN
            phase_end_time = last_target + datetime.timedelta(seconds=restartDur)
            current_stage, title_countdown = f"Rebooting{dots_title}", hms(restartDur - seconds_since_last)
            h_label, h_val = "Complete:", phase_end_time.astimezone().strftime('%H:%M:%S')
            f_label, f_val = "", f"Rebooting{dots_footer}"
            progress = seconds_since_last / restartDur
        elif Phase == 2:
            current_color = GREEN
            title_color = GREEN
            phase_end_time = last_target + datetime.timedelta(seconds=startDur)
            current_stage, title_countdown = f"Starting{dots_title}", hms(startDur - seconds_since_last)
            h_label, h_val = "Complete:", phase_end_time.astimezone().strftime('%H:%M:%S')
            f_label, f_val = "", f"Starting{dots_footer}"
            progress = (seconds_since_last - restartDur) / (startDur - restartDur)
        else:
            current_color = RED
            title_color = RED
            current_stage, title_countdown = "Restart: ", hms(seconds_left_to_next)
            h_label, h_val = "Next Restart:", f"{target.astimezone().strftime('%H:%M:%S')}"
            f_label, f_val = "", title_countdown
            total_window = countdown(target)
            progress = max(0.0, 1.0 - (seconds_left_to_next / total_window))

        # beep

        if audioBool:
            if Phase != curPhaseID:
                if Phase == 1: beep(450, beepDur, beepVol)
                elif Phase == 2: beep(350, beepDur, beepVol)
                elif Phase == 3 and curPhaseID != -1: beep(250, beepDur, beepVol)
                curPhaseID = Phase

        # ImGui

        imgui.set_next_window_position(0, 0)
        imgui.set_next_window_size(DEFAULT_WIDTH, current_h)
        imgui.push_style_var(imgui.STYLE_WINDOW_PADDING, (8, 5))
        imgui.begin("Main", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE)
        
        # Titlebar Drag Logic

        if io.mouse_down[0]:
            if not dragging:
                if imgui.is_window_hovered() and io.mouse_pos[1] < 30:
                    dragging = True
                    drag_offset_x, drag_offset_y = io.mouse_pos[0], io.mouse_pos[1]
            else:
                mx, my = glfw.get_cursor_pos(window)
                curr_x, curr_y = glfw.get_window_pos(window)
                glfw.set_window_pos(window, int(curr_x + mx - drag_offset_x), int(curr_y + my - drag_offset_y))
        else:
            dragging = False

        # Titlebar
        
        imgui.text(f"{current_stage}") 
        imgui.same_line(spacing=0)
        imgui.text_colored(f"-{title_countdown}", *title_color)
        
        # Titlebar Buttons

        imgui.same_line(position=DEFAULT_WIDTH - 50)
        imgui.push_style_color(imgui.COLOR_BUTTON, *RED)
        imgui.push_style_color(imgui.COLOR_TEXT, 0, 0, 0, 0) # Hide default text
        
        # Save screen positions for custom text drawing
        min_pos = imgui.get_cursor_screen_pos()
        if imgui.button("##min", width=18, height=18): glfw.iconify_window(window)
        
        imgui.same_line()
        close_pos = imgui.get_cursor_screen_pos()
        if imgui.button("##close", width=18, height=18): glfw.set_window_should_close(window, True)
        
        # Draw custom text elements
        draw_list = imgui.get_window_draw_list()
        text_color = imgui.get_color_u32_rgba(*BLACK)
        
        if classic_font_small: imgui.push_font(classic_font_small)
        imgui.set_window_font_scale(1.8)
        
        draw_list.add_text(min_pos[0] + 5, min_pos[1] - 1.5, text_color, "_")
        draw_list.add_text(close_pos[0] + 5, close_pos[1] + 1, text_color, "x")
        
        imgui.set_window_font_scale(1.0)
        if classic_font_small: imgui.pop_font()
        
        imgui.pop_style_color(2) 

        imgui.separator()

        # Body

            # mainPage
        if not show_settings:
            imgui.spacing()
            imgui.text(h_label); imgui.same_line(); imgui.text_colored(h_val, *current_color)
            if classicMode:
                if classic_font_small: imgui.push_font(classic_font_small)
                filled_count = int(progress * 20)
                for i in range(20):
                    if i < filled_count:
                        imgui.text_colored("▰", *current_color) 
                    else:
                        imgui.text_colored("▱", *BAR_BG)
                    if i < 19: imgui.same_line(spacing=1)
                if classic_font_small: imgui.pop_font()
            else:
                imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, *BAR_BG)
                imgui.push_style_color(imgui.COLOR_PLOT_HISTOGRAM, *current_color)
                imgui.progress_bar(progress, size=(-1, 16), overlay="")
                imgui.pop_style_color(2)
            
            imgui.set_cursor_pos((8, current_h - 22 if classicMode else current_h - 24))
            imgui.text_colored(f_val, *current_color)
        
            # Settings
        else:
            imgui.spacing()
            r, g, b, _ = current_color
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND, r, g, b, 0.2)
            imgui.push_style_color(imgui.COLOR_CHECK_MARK, r, g, b, 1.0)
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_HOVERED, r, g, b, 0.4)
            imgui.push_style_color(imgui.COLOR_FRAME_BACKGROUND_ACTIVE, r, g, b, 0.6)
            imgui.push_style_color(imgui.COLOR_SLIDER_GRAB, r, g, b, 0.8)
            imgui.push_style_color(imgui.COLOR_SLIDER_GRAB_ACTIVE, r, g, b, 1.0)

            _, audioBool = imgui.checkbox("beep", audioBool)
            if DEBUG:
                imgui.same_line()
            _, classicMode = imgui.checkbox("classic", classicMode)

            if DEBUG:
                _, forceStage = imgui.checkbox("force", forceStage)
                imgui.same_line()
                imgui.push_item_width(100)
                _, phaseID = imgui.slider_int("##stage_slider", phaseID, 1, 3)
                imgui.pop_item_width()
            
            imgui.pop_style_color(6)

        btn_size = 16
        pos_x = DEFAULT_WIDTH - 22
        pos_y = current_h - 22
        imgui.set_cursor_screen_pos((pos_x, pos_y))
        
        r, g, b, _ = current_color
        imgui.push_style_color(imgui.COLOR_BUTTON, r, g, b, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, r, g, b, 0.5)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, r, g, b, 0.8)
        imgui.push_style_var(imgui.STYLE_FRAME_ROUNDING, 2.0)
        if imgui.button("##settings_btn", width=btn_size, height=btn_size):
            show_settings = not show_settings

        # button transform
        off_x = 1
        off_y = -5

        # button text scale
        draw_list = imgui.get_window_draw_list()
        imgui.set_window_font_scale(1.8) 
        draw_list.add_text(
            pos_x + off_x, 
            pos_y + off_y, 
            imgui.get_color_u32_rgba(0, 0, 0, 1.0), 
            "+"
        )
        imgui.set_window_font_scale(1.0) 


        imgui.pop_style_var(1)
        imgui.pop_style_color(3)


        imgui.end()
        imgui.pop_style_var(1)
        
        gl.glClearColor(0.04, 0.04, 0.04, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    impl.shutdown(); glfw.terminate()

if __name__ == "__main__":
    main()

#   Copyright © 2026 .c.o.r.a
