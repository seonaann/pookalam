import matplotlib.pyplot as plt
import numpy as np
import threading
import queue
from matplotlib.animation import FuncAnimation

# --- Define Global Variables and Queue for communication ---
command_queue = queue.Queue()
current_config = {
    'outer_pattern': 'circles',
    'outer_colors': ['orange', 'red', 'yellow'],
    'plum_color': 'plum'
}

# A dictionary to map simple color names to hex codes
COLOR_PALETTE = {
    "red": "#FF0000",
    "orange": "#FFA500",
    "yellow": "#FFFF00",
    "green": "#008000",
    "violet": "#8A2BE2",
    "magenta": "#FF00FF",
    "brown": "#A0522D",
    "gold": "#FFD700",
    "darkred": "#8B0000",
    "darkkhaki": "#BDB76B",
    "forestgreen": "#228B22",
    "white": "#FFFFFF",
    "plum": "#DDA0DD",
    "sienna": "#A0522D"
}

# --- Drawing Logic ---
def draw_pookalam(ax, outer_angle, inner_angle, config):
    ax.clear()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)

    outer_colors = [COLOR_PALETTE.get(c.strip().lower(), c) for c in config['outer_colors']]
    plum_color = COLOR_PALETTE.get(config['plum_color'].strip().lower(), config['plum_color'])

    # Layer 1: Outermost dynamic and animated layer
    outer_radius = 1.0
    num_elements = 40
    
    if config['outer_pattern'] == 'squares':
        square_diag_half = 0.04
        for i in range(num_elements):
            angle = np.deg2rad(360 / num_elements * i + outer_angle)
            x_center = np.cos(angle) * (outer_radius - square_diag_half)
            y_center = np.sin(angle) * (outer_radius - square_diag_half)
            square_points = [
                (x_center + square_diag_half * np.cos(angle + np.deg2rad(45)), y_center + square_diag_half * np.sin(angle + np.deg2rad(45))),
                (x_center + square_diag_half * np.cos(angle + np.deg2rad(135)), y_center + square_diag_half * np.sin(angle + np.deg2rad(135))),
                (x_center + square_diag_half * np.cos(angle + np.deg2rad(225)), y_center + square_diag_half * np.sin(angle + np.deg2rad(225))),
                (x_center + square_diag_half * np.cos(angle + np.deg2rad(315)), y_center + square_diag_half * np.sin(angle + np.deg2rad(315))),
            ]
            square_patch = plt.Polygon(square_points, color=outer_colors[i % len(outer_colors)])
            ax.add_patch(square_patch)
            
    elif config['outer_pattern'] == 'circles':
        circle_radius = 0.05
        for i in range(num_elements):
            angle = np.deg2rad(360 / num_elements * i + outer_angle)
            x_center = np.cos(angle) * (outer_radius - circle_radius)
            y_center = np.sin(angle) * (outer_radius - circle_radius)
            color = outer_colors[i % len(outer_colors)]
            ax.add_patch(plt.Circle((x_center, y_center), circle_radius, color=color))

    # All static layers
    ax.add_patch(plt.Circle((0,0), 0.85, color=COLOR_PALETTE['orange']))
    triangle_outer_radius = 0.65
    triangle_base_length = 0.4
    num_star_points = 8
    for i in range(num_star_points):
        angle_center = np.deg2rad(360 / num_star_points * i)
        tip_x = np.cos(angle_center) * triangle_outer_radius
        tip_y = np.sin(angle_center) * triangle_outer_radius
        base_left_x = tip_x + triangle_base_length/2 * np.cos(angle_center + np.deg2rad(90))
        base_left_y = tip_y + triangle_base_length/2 * np.sin(angle_center + np.deg2rad(90))
        base_right_x = tip_x + triangle_base_length/2 * np.cos(angle_center - np.deg2rad(90))
        base_right_y = tip_y + triangle_base_length/2 * np.sin(angle_center - np.deg2rad(90))
        triangle_points = [(tip_x, tip_y), (base_left_x, base_left_y), (base_right_x, base_right_y)]
        ax.add_patch(plt.Polygon(triangle_points, color=COLOR_PALETTE['yellow']))
    ax.add_patch(plt.Circle((0,0), 0.45, color=COLOR_PALETTE['forestgreen']))
    inner_star_radius = 0.3
    num_segments = 6
    inner_colors = [COLOR_PALETTE['darkred'], COLOR_PALETTE['orange'], COLOR_PALETTE['gold'], COLOR_PALETTE['darkkhaki']]
    for i in range(num_segments):
        start_angle = np.deg2rad(360 / num_segments * i)
        points_block = [(0,0)]
        for angle_deg in np.linspace(360/num_segments*i, 360/num_segments*(i+1), 10):
            points_block.append((0.38*np.cos(np.deg2rad(angle_deg)), 0.38*np.sin(np.deg2rad(angle_deg))))
        points_block.append((0,0))
        block_color = inner_colors[i % len(inner_colors)]
        ax.add_patch(plt.Polygon(points_block, color=block_color))

    # Animated Layer: Small white squares
    dot_radius = 0.52
    num_dots = 6
    dot_size_half = 0.02
    for i in range(num_dots):
        angle = np.deg2rad(360 / num_dots * i + 30 + inner_angle)
        x_dot = np.cos(angle) * dot_radius
        y_dot = np.sin(angle) * dot_radius
        white_square_points = [
            (x_dot + dot_size_half * np.cos(angle + np.deg2rad(45)), y_dot + dot_size_half * np.sin(angle + np.deg2rad(45))),
            (x_dot + dot_size_half * np.cos(angle + np.deg2rad(135)), y_dot + dot_size_half * np.sin(angle + np.deg2rad(135))),
            (x_dot + dot_size_half * np.cos(angle + np.deg2rad(225)), y_dot + dot_size_half * np.sin(angle + np.deg2rad(225))),
            (x_dot + dot_size_half * np.cos(angle + np.deg2rad(315)), y_dot + dot_size_half * np.sin(angle + np.deg2rad(315))),
        ]
        ax.add_patch(plt.Polygon(white_square_points, color=COLOR_PALETTE['white']))

    # Innermost two circles (static)
    circle_plum = plt.Circle((0,0), 0.15, color=plum_color)
    ax.add_patch(circle_plum)
    circle_gold_center = plt.Circle((0,0), 0.1, color=COLOR_PALETTE['gold'])
    ax.add_patch(circle_gold_center)

# --- Animation and Input Functions ---
def animate(frame):
    global current_config
    
    # Process commands from the queue
    while not command_queue.empty():
        command = command_queue.get()
        if command == 'quit':
            plt.close('all')
            return
        
        parts = command.split(' ')
        cmd = parts[0]
        
        if cmd == 'color_outer':
            new_colors_str = " ".join(parts[1:])
            current_config['outer_colors'] = new_colors_str.replace(" ", "").split(',')
        elif cmd == 'pattern_outer':
            if parts[1] in ['circles', 'squares']:
                current_config['outer_pattern'] = parts[1]
        elif cmd == 'color_plum':
            current_config['plum_color'] = parts[1]
            
    # Calculate angles for animation
    outer_rotation_speed = 0.5
    inner_rotation_speed = -1.0
    outer_angle = frame * outer_rotation_speed
    inner_angle = frame * inner_rotation_speed
    
    # Redraw the plot with the new configuration and animation angles
    draw_pookalam(ax, outer_angle, inner_angle, current_config)

def get_input():
    print("Welcome to the Interactive Pookalam Builder!")
    print("Enter 'quit' to exit.")
    print("Commands: color_outer <colors>, pattern_outer <pattern>, color_plum <color>")
    while True:
        command = input("Enter command: ")
        command_queue.put(command)
        if command.strip().lower() == 'quit':
            break

# --- Main Program Setup ---
if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(8,8))

    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()

    ani = FuncAnimation(fig, animate, interval=20, cache_frame_data=False)
    plt.show()